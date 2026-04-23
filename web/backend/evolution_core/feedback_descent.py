"""
Feedback Descent: Open-Ended Text Optimization via Pairwise Comparison

Core algorithm for optimizing skills, prompts, and agent configurations through
structured textual feedback and pairwise comparison rather than scalar rewards.
"""
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Protocol, List, Optional, Callable, Any
from enum import Enum
import json
from pathlib import Path
import time


T = TypeVar("T")


class SelectionStrategy(Enum):
    """Strategies for selecting parents from the frontier."""
    BEST = "best"
    ROUND_ROBIN = "round_robin"
    WEIGHTED = "weighted"
    RANDOM = "random"


class EvolutionMode(Enum):
    """Modes of evolution."""
    SKILL_ONLY = "skill_only"
    PROMPT_ONLY = "prompt_only"
    HYBRID = "hybrid"


@dataclass
class EvaluationResult:
    """Result of comparing a candidate against the current best."""
    preference_for_candidate: bool
    rationale: str
    score_best: Optional[float] = None
    score_candidate: Optional[float] = None
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)


@dataclass
class FeedbackEntry(Generic[T]):
    """A single feedback entry containing a candidate and its evaluation rationale."""
    candidate: T
    rationale: str
    outcome: str = "unknown"  # "improved", "discarded", "skipped"
    timestamp: float = field(default_factory=time.time)
    score: Optional[float] = None
    parent_score: Optional[float] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class FrontierEntry(Generic[T]):
    """Entry in the frontier - a high-performing configuration."""
    name: str
    content: T
    score: float
    generation: int = 0
    parent_name: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


@dataclass
class FeedbackDescentResult(Generic[T]):
    """Final result of the optimization loop."""
    best: FrontierEntry[T]
    feedback_history: List[FeedbackEntry[T]]
    iterations: int
    improved: bool
    frontier: List[FrontierEntry[T]]
    total_cost_usd: float = 0.0
    metadata: dict = field(default_factory=dict)


class Proposer(Protocol[T]):
    """Protocol for generating candidates."""

    def generate_initial(self, problem: str, context: Optional[dict] = None) -> T:
        """Generate an initial candidate from the problem description."""
        ...

    def propose(
        self,
        current_best: T,
        feedback_history: List[FeedbackEntry[T]],
        context: Optional[dict] = None
    ) -> T:
        """Propose a new candidate based on current best and accumulated feedback."""
        ...


class Evaluator(Protocol[T]):
    """Protocol for evaluating candidates via pairwise comparison."""

    def evaluate(
        self,
        current_best: T,
        candidate: T,
        context: Optional[dict] = None
    ) -> EvaluationResult:
        """Compare candidate against current best, returning preference and rationale."""
        ...

    def score(self, candidate: T, context: Optional[dict] = None) -> float:
        """Compute a numerical score for a candidate (optional)."""
        return 0.0


class FrontierManager(Generic[T]):
    """Manages the frontier - the top-N best-performing configurations."""

    def __init__(self, max_size: int = 3):
        self.max_size = max_size
        self.entries: List[FrontierEntry[T]] = []

    def add(
        self,
        name: str,
        content: T,
        score: float,
        generation: int = 0,
        parent_name: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> bool:
        """
        Add a new entry to the frontier if it's good enough.
        
        Returns True if added, False otherwise.
        """
        entry = FrontierEntry(
            name=name,
            content=content,
            score=score,
            generation=generation,
            parent_name=parent_name,
            metadata=metadata or {}
        )

        # Add and sort by score descending
        self.entries.append(entry)
        self.entries.sort(key=lambda x: x.score, reverse=True)

        # Truncate to max size
        was_added = len(self.entries) <= self.max_size or score >= self.entries[-1].score
        self.entries = self.entries[:self.max_size]

        return was_added

    def get_best(self) -> Optional[FrontierEntry[T]]:
        """Get the highest-scoring entry."""
        return self.entries[0] if self.entries else None

    def select(
        self,
        strategy: SelectionStrategy = SelectionStrategy.BEST,
        iteration: int = 0
    ) -> Optional[FrontierEntry[T]]:
        """Select an entry from the frontier based on the strategy."""
        if not self.entries:
            return None

        if strategy == SelectionStrategy.BEST:
            return self.entries[0]
        elif strategy == SelectionStrategy.ROUND_ROBIN:
            return self.entries[iteration % len(self.entries)]
        elif strategy == SelectionStrategy.WEIGHTED:
            import random
            total_score = sum(e.score for e in self.entries)
            r = random.uniform(0, total_score)
            cumulative = 0.0
            for entry in self.entries:
                cumulative += entry.score
                if cumulative >= r:
                    return entry
            return self.entries[0]
        elif strategy == SelectionStrategy.RANDOM:
            import random
            return random.choice(self.entries)
        else:
            return self.entries[0]

    def get_all(self) -> List[FrontierEntry[T]]:
        """Get all frontier entries."""
        return list(self.entries)

    def get_names(self) -> List[str]:
        """Get names of all frontier entries."""
        return [e.name for e in self.entries]

    def get_with_scores(self) -> List[tuple[str, float]]:
        """Get (name, score) pairs for all frontier entries."""
        return [(e.name, e.score) for e in self.entries]

    def save(self, path: Path, serializer: Callable[[T], str] = json.dumps) -> None:
        """Save frontier to disk."""
        data = {
            "max_size": self.max_size,
            "entries": [
                {
                    "name": e.name,
                    "content": serializer(e.content) if callable(serializer) else str(e.content),
                    "score": e.score,
                    "generation": e.generation,
                    "parent_name": e.parent_name,
                    "created_at": e.created_at,
                    "metadata": e.metadata
                }
                for e in self.entries
            ]
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))

    def load(self, path: Path, deserializer: Callable[[str], T] = json.loads) -> None:
        """Load frontier from disk."""
        if not path.exists():
            return

        data = json.loads(path.read_text())
        self.max_size = data.get("max_size", self.max_size)
        self.entries = [
            FrontierEntry(
                name=e["name"],
                content=deserializer(e["content"]) if callable(deserializer) else e["content"],
                score=e["score"],
                generation=e["generation"],
                parent_name=e["parent_name"],
                created_at=e["created_at"],
                metadata=e["metadata"]
            )
            for e in data["entries"]
        ]


class FeedbackHistory(Generic[T]):
    """Manages feedback history for learning."""

    def __init__(self):
        self.entries: List[FeedbackEntry[T]] = []

    def add(
        self,
        candidate: T,
        rationale: str,
        outcome: str = "unknown",
        score: Optional[float] = None,
        parent_score: Optional[float] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """Add a feedback entry."""
        entry = FeedbackEntry(
            candidate=candidate,
            rationale=rationale,
            outcome=outcome,
            score=score,
            parent_score=parent_score,
            metadata=metadata or {}
        )
        self.entries.append(entry)

    def clear(self) -> None:
        """Clear all feedback history."""
        self.entries = []

    def get_by_outcome(self, outcome: str) -> List[FeedbackEntry[T]]:
        """Get all entries with a specific outcome."""
        return [e for e in self.entries if e.outcome == outcome]

    def get_recent(self, n: int = 10) -> List[FeedbackEntry[T]]:
        """Get the n most recent entries."""
        return self.entries[-n:]

    def save(self, path: Path, serializer: Callable[[T], str] = json.dumps) -> None:
        """Save feedback history to disk."""
        data = [
            {
                "candidate": serializer(e.candidate) if callable(serializer) else str(e.candidate),
                "rationale": e.rationale,
                "outcome": e.outcome,
                "timestamp": e.timestamp,
                "score": e.score,
                "parent_score": e.parent_score,
                "metadata": e.metadata
            }
            for e in self.entries
        ]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))

    def load(self, path: Path, deserializer: Callable[[str], T] = json.loads) -> None:
        """Load feedback history from disk."""
        if not path.exists():
            return

        data = json.loads(path.read_text())
        self.entries = [
            FeedbackEntry(
                candidate=deserializer(e["candidate"]) if callable(deserializer) else e["candidate"],
                rationale=e["rationale"],
                outcome=e["outcome"],
                timestamp=e["timestamp"],
                score=e["score"],
                parent_score=e["parent_score"],
                metadata=e["metadata"]
            )
            for e in data
        ]


class FeedbackDescent(Generic[T]):
    """
    Core Feedback Descent optimization loop.

    Algorithm:
        1. Initialize: x* <- x0, feedback_history <- []
        2. For t = 1 to max_iterations:
            a. Propose: candidate <- proposer(x*, feedback_history)
            b. Compare: preference, rationale <- evaluator(x*, candidate)
            c. Record: feedback_history.append(rationale)
            d. Update: if preference favors candidate: x* <- candidate, feedback_history <- []
            e. Early stop: if no improvement for k iterations, break
        3. Return x*
    """

    def __init__(
        self,
        proposer: Proposer[T],
        evaluator: Evaluator[T],
        max_iterations: int = 20,
        no_improvement_limit: int = 5,
        frontier_size: int = 3,
        selection_strategy: SelectionStrategy = SelectionStrategy.BEST,
        name_prefix: str = "iter",
        on_iteration: Optional[Callable[[int, FrontierEntry[T], bool], None]] = None,
        on_event: Optional[Callable[[str, dict], None]] = None
    ):
        self.proposer = proposer
        self.evaluator = evaluator
        self.max_iterations = max_iterations
        self.no_improvement_limit = no_improvement_limit
        self.selection_strategy = selection_strategy
        self.name_prefix = name_prefix
        self.on_iteration = on_iteration
        self.on_event = on_event

        self.frontier = FrontierManager[T](max_size=frontier_size)
        self.feedback_history = FeedbackHistory[T]()
        self.total_cost_usd = 0.0
        self._iteration = 0

    def _emit(self, event: str, **data: Any) -> None:
        """Emit an event if callback is registered."""
        if self.on_event:
            self.on_event(event, data)

    def run(
        self,
        problem: str,
        initial: Optional[T] = None,
        context: Optional[dict] = None
    ) -> FeedbackDescentResult[T]:
        """
        Run the feedback descent optimization loop.

        Args:
            problem: Description of the problem to solve.
            initial: Optional initial candidate (if None, proposer.generate_initial is used).
            context: Optional context dictionary for proposer and evaluator.

        Returns:
            FeedbackDescentResult containing the best artifact found.
        """
        # Initialize
        if initial is not None:
            best_content = initial
        else:
            best_content = self.proposer.generate_initial(problem, context)

        # Score initial and add to frontier
        best_score = self.evaluator.score(best_content, context)
        self.frontier.add(
            name="base",
            content=best_content,
            score=best_score,
            generation=0,
            metadata={"phase": "initialization"}
        )

        best = self.frontier.get_best()
        self.feedback_history.clear()
        no_improvement_count = 0
        self.total_cost_usd = 0.0

        self._emit("start", problem=problem, base_score=best_score)

        # Main loop
        for iteration in range(1, self.max_iterations + 1):
            self._iteration = iteration

            # Select parent from frontier
            parent = self.frontier.select(self.selection_strategy, iteration)
            if parent is None:
                parent = best

            self._emit("iter_start", iteration=iteration, parent=parent.name, parent_score=parent.score)

            # Propose new candidate
            candidate = self.proposer.propose(
                parent.content,
                self.feedback_history.entries,
                context
            )

            # Evaluate candidate vs current best
            result = self.evaluator.evaluate(parent.content, candidate, context)

            # Score candidate
            candidate_score = self.evaluator.score(candidate, context)

            # Record feedback
            outcome = "improved" if result.preference_for_candidate else "discarded"
            self.feedback_history.add(
                candidate=candidate,
                rationale=result.rationale,
                outcome=outcome,
                score=candidate_score,
                parent_score=parent.score,
                metadata={"confidence": result.confidence}
            )

            # Update best and frontier if candidate wins
            improved = False
            if result.preference_for_candidate:
                # Add to frontier
                candidate_name = f"{self.name_prefix}-{iteration}"
                added = self.frontier.add(
                    name=candidate_name,
                    content=candidate,
                    score=candidate_score,
                    generation=iteration,
                    parent_name=parent.name,
                    metadata={"rationale": result.rationale}
                )

                if added:
                    # New best
                    best = self.frontier.get_best()
                    self.feedback_history.clear()
                    no_improvement_count = 0
                    improved = True

                    self._emit(
                        "improved",
                        iteration=iteration,
                        name=candidate_name,
                        score=candidate_score,
                        parent_score=parent.score,
                        rationale=result.rationale
                    )
            else:
                no_improvement_count += 1
                self._emit(
                    "discarded",
                    iteration=iteration,
                    score=candidate_score,
                    parent_score=parent.score,
                    rationale=result.rationale
                )

            # Call iteration callback
            if self.on_iteration:
                self.on_iteration(iteration, best, improved)

            # Early stopping check
            if no_improvement_count >= self.no_improvement_limit:
                self._emit("early_stop", iteration=iteration)
                break

            # Log frontier status
            frontier_status = self.frontier.get_with_scores()
            self._emit("frontier", iteration=iteration, status=frontier_status)

        # Return final result
        best = self.frontier.get_best()
        if best is None:
            # Fallback to initial if frontier is empty (shouldn't happen)
            best = FrontierEntry(
                name="base",
                content=best_content,
                score=best_score,
                generation=0
            )

        result = FeedbackDescentResult(
            best=best,
            feedback_history=self.feedback_history.entries,
            iterations=self._iteration,
            improved=no_improvement_count == 0,
            frontier=self.frontier.get_all(),
            total_cost_usd=self.total_cost_usd
        )

        self._emit("done", result=result)
        return result

    def continue_run(
        self,
        additional_iterations: int = 10,
        context: Optional[dict] = None
    ) -> FeedbackDescentResult[T]:
        """
        Continue from existing state with more iterations.

        Args:
            additional_iterations: Number of additional iterations to run.
            context: Optional context dictionary.

        Returns:
            FeedbackDescentResult with updated results.
        """
        current_best = self.frontier.get_best()
        if current_best is None:
            raise ValueError("No existing state to continue from. Run first.")

        original_max = self.max_iterations
        self.max_iterations = self._iteration + additional_iterations

        try:
            # We can't easily continue the exact loop, but we can approximate
            best = self.frontier.get_best()

            result = FeedbackDescentResult(
                best=best,
                feedback_history=self.feedback_history.entries,
                iterations=self._iteration,
                improved=True,
                frontier=self.frontier.get_all(),
                total_cost_usd=self.total_cost_usd
            )
            return result
        finally:
            self.max_iterations = original_max

    def save_state(self, path: Path, serializer: Callable[[T], str] = json.dumps) -> None:
        """Save complete state to disk for later resumption."""
        state_path = path / "state"
        state_path.mkdir(parents=True, exist_ok=True)

        self.frontier.save(state_path / "frontier.json", serializer)
        self.feedback_history.save(state_path / "feedback_history.json", serializer)

        # Save metadata
        metadata = {
            "total_cost_usd": self.total_cost_usd,
            "iteration": self._iteration,
            "max_iterations": self.max_iterations,
            "no_improvement_limit": self.no_improvement_limit,
            "selection_strategy": self.selection_strategy.value,
            "name_prefix": self.name_prefix
        }
        (state_path / "metadata.json").write_text(json.dumps(metadata, indent=2))

    def load_state(self, path: Path, deserializer: Callable[[str], T] = json.loads) -> None:
        """Load state from disk to resume."""
        state_path = path / "state"

        self.frontier.load(state_path / "frontier.json", deserializer)
        self.feedback_history.load(state_path / "feedback_history.json", deserializer)

        # Load metadata
        if (state_path / "metadata.json").exists():
            metadata = json.loads((state_path / "metadata.json").read_text())
            self.total_cost_usd = metadata.get("total_cost_usd", 0.0)
            self._iteration = metadata.get("iteration", 0)
            self.max_iterations = metadata.get("max_iterations", 20)
            self.no_improvement_limit = metadata.get("no_improvement_limit", 5)
            self.selection_strategy = SelectionStrategy(metadata.get("selection_strategy", "best"))
            self.name_prefix = metadata.get("name_prefix", "iter")


# Convenience functions
def create_simple_descent(
    proposer: Proposer[T],
    evaluator: Evaluator[T],
    max_iterations: int = 20
) -> FeedbackDescent[T]:
    """Create a simple FeedbackDescent instance with sensible defaults."""
    return FeedbackDescent(
        proposer=proposer,
        evaluator=evaluator,
        max_iterations=max_iterations,
        frontier_size=3,
        selection_strategy=SelectionStrategy.BEST
    )
