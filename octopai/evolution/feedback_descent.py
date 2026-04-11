"""
Feedback Descent Optimizer - Advanced optimization algorithm for skill evolution.

Implements a feedback-driven pairwise comparison optimization:
- Propose candidates based on current best and feedback history
- Evaluate using pairwise comparison (not scalar rewards)
- Update based on preference and rationale
- Maintain feedback history for intelligent proposals
- Early stopping when no improvement for K iterations
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum
import random
import re


class ComparisonResult(Enum):
    """Result of pairwise comparison."""
    CURRENT_BETTER = "current_better"
    CANDIDATE_BETTER = "candidate_better"
    TIE = "tie"
    UNCLEAR = "unclear"


@dataclass
class FeedbackRecord:
    """Single feedback record from evaluation.

    Attributes:
        iteration: When this feedback was recorded
        candidate_content: The candidate that was evaluated
        comparison_result: Who won the comparison
        rationale: Explanation of the decision
        confidence: Confidence in this assessment (0.0-1.0)
        metrics: Additional metrics from evaluation
    """

    iteration: int = 0
    candidate_content: str = ""
    comparison_result: ComparisonResult = ComparisonResult.TIE
    rationale: str = ""
    confidence: float = 0.5
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class Proposal:
    """A proposed improvement to the current solution.

    Attributes:
        content: Proposed content/skill
        description: What this proposal changes
        source: Where this proposal came from (e.g., "mutation", "llm", "template")
        expected_improvement: Expected improvement type
        metadata: Additional proposal metadata
    """

    content: str = ""
    description: str = ""
    source: str = "mutation"
    expected_improvement: str = "general"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationState:
    """Current state of the optimization process.

    Attributes:
        current_best: Current best content
        current_score: Score of current best
        iteration: Current iteration number
        total_iterations: Total iterations completed
        feedback_history: All feedback records
        proposals_tried: List of proposals that were tried
        improvements_made: Number of successful improvements
        stagnation_count: Iterations without improvement
        is_converged: Whether optimization has converged
    """

    current_best: str = ""
    current_score: float = 0.0
    iteration: int = 0
    total_iterations: int = 0
    feedback_history: List[FeedbackRecord] = field(default_factory=list)
    proposals_tried: List[str] = field(default_factory=list)
    improvements_made: int = 0
    stagnation_count: int = 0
    is_converged: bool = False


class FeedbackDescentOptimizer:
    """Feedback Descent optimizer for skill evolution.

    This optimizer uses pairwise comparisons instead of scalar rewards,
    making it more robust for text-based skill optimization.

    Algorithm:
    1. Start with initial content x*
    2. For each iteration:
       a. Generate proposal(s) based on x* and feedback history
       b. Evaluate pairwise: compare(x*, candidate)
       c. Record feedback with rationale
       d. If candidate is better: update x* = candidate
       e. If no improvement for K iterations: stop

    Usage:
        ```python
        optimizer = FeedbackDescentOptimizer(
            proposer=my_proposer_func,
            evaluator=my_evaluator_func,
            max_iterations=20,
            stagnation_limit=5,
        )

        result = optimizer.optimize(initial_content)
        print(f"Best score: {result.current_score}")
        print(f"Iterations: {result.total_iterations}")
        ```
    """

    def __init__(
        self,
        proposer: Callable[[str, List[FeedbackRecord]], Proposal],
        evaluator: Callable[[str, str], Tuple[ComparisonResult, str, float]],
        max_iterations: int = 20,
        stagnation_limit: int = 5,
        improvement_threshold: float = 0.5,
        verbose: bool = True,
    ):
        """Initialize the optimizer.

        Args:
            proposer: Function that generates proposals given current best and feedback
            evaluator: Function that compares two candidates (returns result, rationale, confidence)
            max_iterations: Maximum iterations before stopping
            stagnation_limit: Stop after this many iterations without improvement
            improvement_threshold: Minimum confidence to consider as improvement
            verbose: Whether to print progress information
        """
        self.proposer = proposer
        self.evaluator = evaluator
        self.max_iterations = max_iterations
        self.stagnation_limit = stagnation_limit
        self.improvement_threshold = improvement_threshold
        self.verbose = verbose

    def optimize(self, initial_content: str) -> OptimizationState:
        """Run the optimization loop.

        Args:
            initial_content: Starting content to optimize

        Returns:
            Final OptimizationState with results
        """
        state = OptimizationState(
            current_best=initial_content,
            current_score=0.5,  # Initial placeholder score
        )

        if self.verbose:
            print(f"🚀 Starting Feedback Descent Optimization")
            print(f"   Max iterations: {self.max_iterations}")
            print(f"   Stagnation limit: {self.stagnation_limit}")
            print()

        for i in range(1, self.max_iterations + 1):
            state.iteration = i
            state.total_iterations += 1

            if self.verbose:
                print(f"{'='*50}")
                print(f"📊 Iteration {i}/{self.max_iterations}")
                print(f"{'='*50}")

            # Step 1: Generate proposal
            try:
                proposal = self.proposer(state.current_best, state.feedback_history)

                if not proposal or not proposal.content:
                    if self.verbose:
                        print("⚠️  No valid proposal generated")
                    state.stagnation_count += 1
                    continue

                if proposal.content in state.proposals_tried:
                    if self.verbose:
                        print("⚠️  Proposal already tried, skipping")
                    state.stagnation_count += 1
                    continue

            except Exception as e:
                if self.verbose:
                    print(f"❌ Proposal generation failed: {e}")
                state.stagnation_count += 1
                continue

            # Step 2: Evaluate pairwise
            try:
                result, rationale, confidence = self.evaluator(
                    state.current_best,
                    proposal.content,
                )
            except Exception as e:
                if self.verbose:
                    print(f"❌ Evaluation failed: {e}")
                state.stagnation_count += 1
                continue

            # Step 3: Record feedback
            feedback = FeedbackRecord(
                iteration=i,
                candidate_content=proposal.content,
                comparison_result=result,
                rationale=rationale,
                confidence=confidence,
                metadata={
                    'proposal_source': proposal.source,
                    'proposal_description': proposal.description,
                },
            )
            state.feedback_history.append(feedback)
            state.proposals_tried.append(proposal.content)

            if self.verbose:
                status_icon = {
                    ComparisonResult.CURRENT_BETTER: "📉",
                    ComparisonResult.CANDIDATE_BETTER: "📈",
                    ComparisonResult.TIE: "➡️",
                    ComparisonResult.UNCLEAR: "❓",
                }.get(result, "❓")

                print(f"{status_icon} Result: {result.value}")
                print(f"   Rationale: {rationale[:100]}...")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Source: {proposal.source}")

            # Step 4: Update if improved
            if result == ComparisonResult.CANDIDATE_BETTER and confidence >= self.improvement_threshold:
                state.current_best = proposal.content
                state.current_score = confidence
                state.improvements_made += 1
                state.stagnation_count = 0

                if self.verbose:
                    print(f"\n✅ IMPROVEMENT! Updated to new best (confidence: {confidence:.2f})")
            else:
                state.stagnation_count += 1

                if self.verbose:
                    print(f"\n❌ No improvement (stagnation: {state.stagnation_count}/{self.stagnation_limit})")

            # Step 5: Check convergence
            if state.stagnation_count >= self.stagnation_limit:
                state.is_converged = True
                if self.verbose:
                    print(f"\n🏁 Converged! No improvement for {state.stagnation_limit} iterations")
                break

        if not state.is_converged and self.verbose:
            print(f"\n✅ Completed {state.max_iterations} iterations")

        return state

    def get_feedback_summary(self, state: OptimizationState) -> Dict[str, Any]:
        """Generate summary of feedback history.

        Args:
            state: Optimization state with feedback history

        Returns:
            Dictionary with feedback statistics
        """
        if not state.feedback_history:
            return {"total_feedback": 0}

        total = len(state.feedback_history)
        improvements = sum(
            1 for f in state.feedback_history
            if f.comparison_result == ComparisonResult.CANDIDATE_BETTER
            and f.confidence >= self.improvement_threshold
        )

        avg_confidence = (
            sum(f.confidence for f in state.feedback_history) / total
            if total > 0 else 0
        )

        sources = {}
        for f in state.feedback_history:
            src = f.metadata.get('proposal_source', 'unknown')
            sources[src] = sources.get(src, 0) + 1

        return {
            "total_feedback": total,
            "improvements_accepted": improvements,
            "improvement_rate": improvements / total if total > 0 else 0,
            "average_confidence": round(avg_confidence, 3),
            "proposal_sources": sources,
            "convergence_status": "converged" if state.is_converged else "max_iterations_reached",
        }


def create_default_proposer(llm_client: Optional[Any] = None) -> Callable:
    """Create a default proposal function.

    Generates proposals using:
    1. Mutation-based changes (rephrase sections)
    2. Template-based additions
    3. LLM-guided improvements (if client available)

    Args:
        llm_client: Optional LLM client for intelligent proposals

    Returns:
        Configured proposer function
    """

    import random
    import re

    def proposer(current_best: str, feedback_history: List[FeedbackRecord]) -> Optional[Proposal]:
        """Generate a proposal based on current state."""
        strategies = [
            _mutation_proposal,
            _add_example_proposal,
            _restructure_proposal,
        ]

        if llm_client:
            strategies.append(lambda c, f: _llm_proposal(c, f, llm_client))

        # Weight recent failures higher
        if feedback_history:
            recent_failures = [f for f in feedback_history[-5:]
                                  if f.comparison_result == ComparisonResult.CURRENT_BETTER]
            if recent_failures and random.random() > 0.3:
                return _failure_driven_proposal(current_best, recent_failures)

        strategy = random.choice(strategies)
        return strategy(current_best, feedback_history)

    return proposer


def _mutation_proposal(content: str, feedback: List[FeedbackRecord]) -> Optional[Proposal]:
    """Generate mutation-based proposal."""
    lines = content.split('\n')
    if len(lines) < 3:
        return None

    # Pick a random section to modify
    start_idx = random.randint(0, len(lines) // 2)
    end_idx = min(start_idx + random.randint(2, 5), len(lines))

    original_section = '\n'.join(lines[start_idx:end_idx])

    # Apply simple mutations
    mutated = original_section

    # Rephrase
    if random.random() > 0.5:
        replacements = {
            'can': 'is able to',
            'use': 'utilize',
            'get': 'retrieve',
            'make': 'create',
            'show': 'display',
        }
        for old, new in replacements.items():
            mutated = mutated.replace(old, new)

    # Add detail
    if random.random() > 0.7:
        detail_phrases = [
            "\n    Note: This operation is case-sensitive.",
            "\n    Important: Ensure proper error handling.",
            "\n    Example usage shown below.",
        ]
        mutated += random.choice(detail_phrases)

    new_lines = lines[:start_idx] + [mutated] + lines[end_idx:]
    new_content = '\n'.join(new_lines)

    return Proposal(
        content=new_content,
        description=f"Modified section at line {start_idx+1}",
        source="mutation",
        expected_improvement="clarity",
    )


def _add_example_proposal(content: str, feedback: List[FeedbackRecord]) -> Optional[Proposal]:
    """Add an example section if missing."""
    if '```' in content and len(content.split('```')) >= 4:
        return None  # Already has examples

    example_templates = [
        "\n\n## Example\n```python\n# Example usage\nresult = function_name(input_data)\nprint(result)\n```\n",
        "\n\n## Example\n```javascript\n// Example usage\nconst result = functionName(inputData);\nconsole.log(result);\n```\n",
        "\n\n## Usage Example\n1. Initialize the component\n2. Configure parameters\n3. Execute the operation\n4. Handle the response\n",
    ]

    template = random.choice(example_templates)
    new_content = content + template

    return Proposal(
        content=new_content,
        description="Added practical example section",
        source="template_addition",
        expected_improvement="completeness",
    )


def _restructure_proposal(content: str, feedback: List[FeedbackRecord]) -> Optional[Proposal]:
    """Reorganize content structure."""
    if len(content) < 200:
        return None

    # Add table of contents if not present
    if '## Table of Contents' not in content[:500]:
        headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        if len(headings) >= 3:
            toc = "\n## Table of Contents\n\n"
            for h in headings[:10]:
                toc += f"- {h}\n"
            toc += "\n"

            insertion_point = content.find('\n', content.find('\n') + 1)
            if insertion_point > 0:
                new_content = content[:insertion_point] + toc + content[insertion_point:]
                return Proposal(
                    content=new_content,
                    description="Added table of contents",
                    source="restructuring",
                    expected_improvement="navigation",
                )

    return None


def _llm_proposal(content: str, feedback: List[FeedbackRecord], llm_client) -> Optional[Proposal]:
    """Use LLM to generate intelligent proposal."""
    prompt = f"""Suggest an improvement to this skill content:

Current Content (first 1000 chars):
{content[:1000]}

Recent Feedback (last 3):
{[(f.rationale[:80], f.comparison_result.value) for f in feedback[-3:]] if feedback else []}

Generate ONE specific improvement suggestion. Return only the modified section or addition.
Focus on: clarity, completeness, error handling, or examples."""

    try:
        response = llm_client.generate(prompt)

        if response and len(response.strip()) > 20:
            # Append or insert the LLM's suggestion
            if random.random() > 0.5:
                new_content = content + f"\n\n## Additional Notes\n{response}\n"
            else:
                new_content = content + f"\n{response}\n"

            return Proposal(
                content=new_content,
                description=f"LLM-suggested improvement",
                source="llm_guided",
                expected_improvement="quality",
            )
    except Exception:
        pass

    return None


def _failure_driven_proposal(content: str, failures: List[FeedbackRecord]) -> Optional[Proposal]:
    """Generate proposal addressing recent failures."""
    if not failures:
        return None

    # Analyze failure patterns
    failure_rationales = [f.rationale.lower() for f in failures]

    if any(word in ' '.join(failure_rationales) for word in ['error', 'fail', 'missing']):
        # Add error handling
        error_template = """
        
## Error Handling

This skill includes comprehensive error handling:

- **Input Validation**: Validate all inputs before processing
- **Exception Catching**: Gracefully handle unexpected errors
- **Logging**: Log errors for debugging purposes
- **Fallback**: Provide fallback behavior on failure

```python
try:
    result = main_operation()
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    return default_response
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```
"""
        return Proposal(
            content=content + error_template,
            description="Added error handling based on failure analysis",
            source="failure_analysis",
            expected_improvement="robustness",
        )

    return None
