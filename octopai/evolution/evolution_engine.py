"""
Core Evolution Engine - Main orchestrator for skill self-evolution.

Implements the complete evolution loop:
1. Evaluate current variants
2. Identify failures and improvement opportunities
3. Generate mutation proposals
4. Apply mutations to create new variants
5. Evaluate new variants
6. Update frontier with improvements
7. Track feedback and iterate
"""

import asyncio
import time
from typing import Any, Callable, Optional, List, Dict
from dataclasses import dataclass

from .config import (
    EvolutionConfig,
    EvolutionMode,
    SelectionStrategy,
    LoopResult,
    SkillVariant,
    EvaluationContext,
)
from .frontier import FrontierManager
from .evaluator import SkillEvaluator, BatchEvalResult
from .mutator import SkillMutator, MutationProposal, MutationResult
from .feedback import FeedbackHistory, FeedbackEntry
from .version_control import VersionManager


@dataclass
class IterationEvent:
    """Event emitted during each iteration for monitoring/visualization.

    Attributes:
        event_type: Type of event (iter_start, eval_done, proposal, etc.)
        iteration: Current iteration number
        data: Event-specific data
        timestamp: When the event occurred
    """

    event_type: str = ""
    iteration: int = 0
    data: Dict[str, Any] = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.data is None:
            self.data = {}


class SkillEvolutionEngine:
    """Main engine for skill self-evolution.

    Orchestrates the complete evolutionary optimization loop:
    - Manages frontier of top-performing variants
    - Evaluates variants against test cases
    - Proposes and applies mutations
    - Tracks feedback from outcomes
    - Supports checkpointing and resumption
    - Emits events for real-time monitoring

    Usage:
        ```python
        config = EvolutionConfig(max_iterations=10)
        engine = SkillEvolutionEngine(config)

        result = await engine.evolve(
            initial_skill=base_variant,
            eval_context=test_context,
        )
        ```
    """

    def __init__(
        self,
        config: EvolutionConfig = None,
        llm_client: Optional[Any] = None,
        on_event: Optional[Callable[[IterationEvent], None]] = None,
    ):
        """Initialize evolution engine.

        Args:
            config: Evolution configuration (uses defaults if None)
            llm_client: Optional LLM client for intelligent mutations
            on_event: Callback function for iteration events
        """
        self.config = config or EvolutionConfig()

        self.frontier = FrontierManager(max_size=self.config.frontier_size)
        self.evaluator = SkillEvaluator(llm_client=llm_client)
        self.mutator = SkillMutator(llm_client=llm_client)
        self.feedback = FeedbackHistory()
        self.version_manager = VersionManager(storage_dir=self.config.cache_dir / "versions")

        self.llm_client = llm_client
        self.on_event = on_event

        self._total_cost = 0.0
        self._mutations_applied = 0
        self._improvements_made = 0

    async def evolve(
        self,
        initial_skill: SkillVariant,
        eval_context: EvaluationContext,
        continue_from_checkpoint: bool = False,
    ) -> LoopResult:
        """Run the full evolution loop.

        Args:
            initial_skill: Starting skill variant to evolve
            eval_context: Evaluation context with test cases
            continue_from_checkpoint: Whether to resume from checkpoint

        Returns:
            LoopResult with final state and statistics
        """
        start_time = time.time()

        if continue_from_checkpoint:
            checkpoint = self.version_manager.load_checkpoint()
            if checkpoint:
                return await self._resume_evolution(checkpoint, eval_context)

        await self._initialize(initial_skill, eval_context)

        no_improvement_count = 0
        iterations_completed = 0

        for i in range(self.config.max_iterations):
            iteration_num = i + 1
            self._emit("iter_start", iteration=iteration_num, total=self.config.max_iterations)

            parent = self.frontier.select_parent(
                strategy=self.config.selection_strategy,
                iteration=i,
            )

            parent_variant = self.frontier.get(parent)
            if not parent_variant:
                break

            failures = await self._identify_failures(parent_variant, eval_context)

            if not failures:
                self._emit(
                    "all_passed",
                    iteration=iteration_num,
                    parent=parent,
                )
                continue

            proposals = self.mutator.propose_mutations(
                variant=parent_variant,
                failures=failures,
                feedback_history=self.feedback.get_recent(10),
            )

            if not proposals:
                no_improvement_count += 1
                if no_improvement_count >= self.config.no_improvement_limit:
                    break
                continue

            best_proposal = max(proposals, key=lambda p: p.confidence)

            self._emit(
                "proposal",
                iteration=iteration_num,
                parent=parent,
                proposal=best_proposal.to_dict() if hasattr(best_proposal, 'to_dict') else vars(best_proposal),
            )

            mutation_result = self.mutator.apply_mutation(parent_variant, best_proposal)

            if not mutation_result.success:
                no_improvement_count += 1
                continue

            child_name = f"gen{parent_variant.generation + 1}-iter{iteration_num}"
            child_variant = SkillVariant(
                name=child_name,
                content=mutation_result.new_content,
                generation=parent_variant.generation + 1,
                parent=parent,
                mutations=[mutation_result.record.to_dict() if mutation_result.record else {}],
            )

            self.version_manager.create_version(child_variant)

            eval_result = await self.evaluator.evaluate_async(
                variant=child_variant,
                context=eval_context,
                max_concurrent=self.config.concurrency,
            )

            child_variant.score = eval_result.total_score
            added = self.frontier.add(child_variant)

            outcome = "improved" if added else "discarded"
            self._mutations_applied += 1

            if added:
                no_improvement_count = 0
                self._improvements_made += 1
            else:
                no_improvement_count += 1

            self.feedback.append_feedback(
                variant_name=child_name,
                proposal=best_proposal.description,
                justification=best_proposal.rationale,
                outcome=outcome,
                score=child_variant.score,
                parent_score=parent_variant.score,
                active_skills=[],
                iteration=iteration_num,
            )

            self._emit(
                "eval_result",
                iteration=iteration_num,
                child_name=child_name,
                score=child_variant.score,
                parent_score=parent_variant.score,
                added=added,
                frontier=self.frontier.get_sorted(),
            )

            if no_improvement_count >= self.config.no_improvement_limit:
                self._emit("stopped", reason="no_improvement")
                break

            if child_variant.score >= self.config.target_score:
                self._emit("target_reached", score=child_variant.score)
                break

            iterations_completed = iteration_num

            self.version_manager.create_checkpoint(
                iteration=iterations_completed,
                frontier_manager=self.frontier,
                feedback_history=self.feedback,
                total_cost=self._total_cost,
                mutations_count=self._mutations_applied,
            )

        total_time = time.time() - start_time

        best = self.frontier.get_best()
        loop_result = LoopResult(
            frontier=self.frontier.get_sorted(),
            best_variant=best.name if best else "",
            best_score=best.score if best else 0.0,
            iterations_completed=iterations_completed,
            total_cost_usd=self._total_cost,
            total_time_seconds=total_time,
            improvements_made=self._improvements_made,
            mutations_applied=self._mutations_applied,
        )

        self._emit("loop_done", **loop_result.__dict__)

        return loop_result

    async def _initialize(
        self,
        initial_skill: SkillVariant,
        eval_context: EvaluationContext,
    ) -> None:
        """Initialize evolution by evaluating base skill."""
        self._emit("init", message="Evaluating base skill")

        base_eval = await self.evaluator.evaluate_async(
            variant=initial_skill,
            context=eval_context,
            max_concurrent=self.config.concurrency,
        )

        initial_skill.score = base_eval.total_score
        self.frontier.add(initial_skill)
        self.version_manager.create_version(initial_skill)

        self._emit(
            "baseline",
            name=initial_skill.name,
            score=initial_skill.score,
        )

    async def _identify_failures(
        self,
        variant: SkillVariant,
        context: EvaluationContext,
    ) -> List[Dict[str, Any]]:
        """Identify test case failures for a variant."""
        eval_result = await self.evaluator.evaluate_async(
            variant=variant,
            context=context,
            max_concurrent=self.config.concurrency,
        )

        failures = []
        for result in eval_result.results:
            if not result.passed:
                failures.append({
                    "type": self._classify_failure(result),
                    "input": str(result.input)[:100],
                    "expected": str(result.expected)[:100],
                    "actual": str(result.actual)[:100] if result.actual else "None",
                    "score": result.score,
                    "error": result.error,
                })

        return failures

    def _classify_failure(self, result) -> str:
        """Classify the type of failure."""
        if result.error:
            return "execution_error"
        if result.actual is None:
            return "no_output"
        if not str(result.expected).strip():
            return "unexpected_output"
        if result.score < 0.5:
            return "poor_quality"
        return "incorrect_output"

    async def _resume_evolution(
        self,
        checkpoint,
        eval_context: EvaluationContext,
    ) -> LoopResult:
        """Resume evolution from checkpoint."""
        self._emit("resume", checkpoint=checkpoint.iteration)

        remaining_iterations = self.config.max_iterations - checkpoint.iteration

        if remaining_iterations <= 0:
            return LoopResult(
                iterations_completed=checkpoint.iteration,
                best_score=checkpoint.best_score,
            )

        self.config.max_iterations = remaining_iterations

        latest_version = self.version_manager.get_latest_version()
        if latest_version:
            return await self.evolve(latest_version, eval_context)

        return LoopResult(iterations_completed=checkpoint.iteration)

    def _emit(self, event_type: str, **data) -> None:
        """Emit an iteration event."""
        if self.on_event:
            event = IterationEvent(event_type=event_type, data=data)
            self.on_event(event)

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the evolution engine.

        Returns:
            Dictionary with current state information
        """
        return {
            "frontier_size": len(self.frontier),
            "frontier_max_size": self.config.frontier_size,
            "best_score": self.frontier.get_best().score if self.frontier.get_best() else 0.0,
            "feedback_entries": len(self.feedback),
            "improvement_rate": self.feedback.get_improvement_rate(),
            "versions_stored": len(self.version_manager),
            "mutations_applied": self._mutations_applied,
            "improvements_made": self._improvements_made,
            "config": {
                "max_iterations": self.config.max_iterations,
                "evolution_mode": self.config.evolution_mode.value,
                "selection_strategy": self.config.selection_strategy.value,
            },
        }

    def get_report(self) -> str:
        """Generate comprehensive evolution report in markdown format.

        Returns:
            Markdown formatted report string
        """
        lines = [
            "# Skill Evolution Report",
            "",
            "## Configuration",
            f"- **Max Iterations:** {self.config.max_iterations}",
            f"- **Frontier Size:** {self.config.frontier_size}",
            f"- **Evolution Mode:** {self.config.evolution_mode.value}",
            f"- **Selection Strategy:** {self.config.selection_strategy.value}",
            "",
            "## Results",
            f"- **Total Mutations Applied:** {self._mutations_applied}",
            f"- **Successful Improvements:** {self._improvements_made}",
            f"- **Improvement Rate:** {self.feedback.get_improvement_rate():.1%}%",
            "",
            "## Frontier (Top Variants)",
            "",
        ]

        for name, score in self.frontier.get_sorted():
            lines.append(f"- **{name}:** {score:.4f}")

        lines.extend([
            "",
            "## Feedback Summary",
            "",
            self.feedback.export_to_markdown(),
            "",
            "## Version Statistics",
            "",
        ])

        stats = self.version_manager.get_statistics()
        lines.extend([
            f"- **Total Versions:** {stats['total_versions']}",
            f"- **Storage Size:** {stats['storage_size_mb']} MB",
            "",
        ])

        return "\n".join(lines)

    def reset(self) -> None:
        """Reset all evolution state."""
        self.frontier.clear()
        self.feedback.clear()
        self._total_cost = 0.0
        self._mutations_applied = 0
        self._improvements_made = 0
