"""
Skill Evaluator - Evaluates skill variants and computes performance scores.
"""

import asyncio
import time
from typing import Any, Callable, Optional
from dataclasses import dataclass

from .config import EvaluationContext, SkillVariant


@dataclass
class EvalResult:
    """Result of evaluating a single test case.

    Attributes:
        input: Test case input
        expected: Expected output
        actual: Actual output from skill
        score: Score for this test case (0.0 to 1.0)
        passed: Whether the test passed (score >= threshold)
        error: Error message if evaluation failed
        execution_time: Time taken for evaluation in seconds
        metadata: Additional metadata about the evaluation
    """

    input: Any = None
    expected: Any = None
    actual: Any = None
    score: float = 0.0
    passed: bool = False
    error: str = ""
    execution_time: float = 0.0
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class BatchEvalResult:
    """Result of batch evaluation of a variant.

    Attributes:
        variant_name: Name of evaluated variant
        total_score: Average score across all test cases
        pass_rate: Fraction of tests that passed
        results: List of individual EvalResult objects
        total_time: Total execution time
        metrics_breakdown: Scores by metric category
    """

    variant_name: str = ""
    total_score: float = 0.0
    pass_rate: float = 0.0
    results: list[EvalResult] = None
    total_time: float = 0.0
    metrics_breakdown: dict[str, float] = None

    def __post_init__(self):
        if self.results is None:
            self.results = []
        if self.metrics_breakdown is None:
            self.metrics_breakdown = {}


class SkillEvaluator:
    """Evaluates skill variants against test cases.

    Supports multiple evaluation strategies:
    - Exact match comparison
    - Similarity-based scoring
    - Custom scorer functions
    - LLM-based evaluation
    - Multi-metric evaluation with weights
    """

    def __init__(
        self,
        custom_scorer: Optional[Callable[[Any, Any], float]] = None,
        llm_client: Optional[Any] = None,
        default_threshold: float = 0.8,
    ):
        """Initialize skill evaluator.

        Args:
            custom_scorer: Custom scoring function (expected, actual) -> score
            llm_client: LLM client for AI-based evaluation
            default_threshold: Default threshold for passing (0.0-1.0)
        """
        self.custom_scorer = custom_scorer
        self.llm_client = llm_client
        self.default_threshold = default_threshold

    def evaluate(
        self,
        variant: SkillVariant,
        context: EvaluationContext,
    ) -> BatchEvalResult:
        """Evaluate a single variant against all test cases.

        Args:
            variant: Skill variant to evaluate
            context: Evaluation context with test cases and configuration

        Returns:
            BatchEvalResult with scores and details
        """
        start_time = time.time()
        results = []

        for i, (test_input, expected) in enumerate(context.test_cases):
            result = self._evaluate_single(
                variant=variant,
                test_input=test_input,
                expected=expected,
                context=context,
                index=i,
            )
            results.append(result)

        total_time = time.time() - start_time

        if not results:
            return BatchEvalResult(
                variant_name=variant.name,
                total_score=0.0,
                pass_rate=0.0,
                results=[],
                total_time=total_time,
            )

        total_score = sum(r.score for r in results) / len(results)
        pass_count = sum(1 for r in results if r.passed)
        pass_rate = pass_count / len(results)

        metrics_breakdown = self._compute_metrics(results, context.metrics)

        return BatchEvalResult(
            variant_name=variant.name,
            total_score=total_score,
            pass_rate=pass_rate,
            results=results,
            total_time=total_time,
            metrics_breakdown=metrics_breakdown,
        )

    async def evaluate_async(
        self,
        variant: SkillVariant,
        context: EvaluationContext,
        max_concurrent: int = 4,
    ) -> BatchEvalResult:
        """Evaluate variant asynchronously with concurrency control.

        Args:
            variant: Skill variant to evaluate
            context: Evaluation context
            max_concurrent: Maximum concurrent evaluations

        Returns:
            BatchEvalResult with scores and details
        """
        start_time = time.time()

        semaphore = asyncio.Semaphore(max_concurrent)

        async def eval_one(index: int, test_input: Any, expected: Any) -> EvalResult:
            async with semaphore:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    lambda: self._evaluate_single(variant, test_input, expected, context, index),
                )

        tasks = [
            eval_one(i, inp, exp)
            for i, (inp, exp) in enumerate(context.test_cases)
        ]

        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        if not results:
            return BatchEvalResult(
                variant_name=variant.name,
                total_score=0.0,
                pass_rate=0.0,
                results=[],
                total_time=total_time,
            )

        total_score = sum(r.score for r in results) / len(results)
        pass_count = sum(1 for r in results if r.passed)
        pass_rate = pass_count / len(results)
        metrics_breakdown = self._compute_metrics(results, context.metrics)

        return BatchEvalResult(
            variant_name=variant.name,
            total_score=total_score,
            pass_rate=pass_rate,
            results=results,
            total_time=total_time,
            metrics_breakdown=metrics_breakdown,
        )

    def _evaluate_single(
        self,
        variant: SkillVariant,
        test_input: Any,
        expected: Any,
        context: EvaluationContext,
        index: int,
    ) -> EvalResult:
        """Evaluate a single test case.

        Args:
            variant: Skill variant to evaluate
            test_input: Input for this test case
            expected: Expected output
            context: Evaluation context
            index: Index of this test case

        Returns:
            EvalResult for this test case
        """
        start_time = time.time()

        try:
            actual = self._execute_skill(variant, test_input, context)

            if self.custom_scorer:
                score = self.custom_scorer(expected, actual)
            else:
                score = self._default_score(expected, actual)

            passed = score >= self.default_threshold

            exec_time = time.time() - start_time

            return EvalResult(
                input=test_input,
                expected=expected,
                actual=actual,
                score=score,
                passed=passed,
                execution_time=exec_time,
                metadata={"index": index, "category": context.category},
            )

        except Exception as e:
            exec_time = time.time() - start_time
            return EvalResult(
                input=test_input,
                expected=expected,
                actual=None,
                score=0.0,
                passed=False,
                error=str(e),
                execution_time=exec_time,
                metadata={"index": index, "category": context.category},
            )

    def _execute_skill(self, variant: SkillVariant, test_input: Any, context: EvaluationContext) -> Any:
        """Execute skill on test input.

        This is a placeholder implementation. In practice, this would:
        - Parse the skill content
        - Execute it with the given input
        - Return the output

        For now, returns a simple text-based response based on content matching.
        """
        if isinstance(test_input, str) and isinstance(variant.content, str):
            if test_input.lower() in variant.content.lower():
                return test_input
            return f"Response based on skill: {variant.content[:100]}..."

        return str(test_input)

    def _default_score(self, expected: Any, actual: Any) -> float:
        """Default scoring function using string similarity.

        Args:
            expected: Expected value
            actual: Actual value

        Returns:
            Score between 0.0 and 1.0
        """
        if expected is None or actual is None:
            return 0.0

        expected_str = str(expected).strip().lower()
        actual_str = str(actual).strip().lower()

        if not expected_str or not actual_str:
            return 0.0

        if expected_str == actual_str:
            return 1.0

        if expected_str in actual_str or actual_str in expected_str:
            return 0.9

        words_expected = set(expected_str.split())
        words_actual = set(actual_str.split())

        if not words_expected:
            return 0.0

        intersection = words_expected & words_actual
        union = words_expected | words_actual

        jaccard = len(intersection) / len(union) if union else 0.0

        length_ratio = min(len(expected_str), len(actual_str)) / max(len(expected_str), len(actual_str))

        return (jaccard * 0.7 + length_ratio * 0.3)

    def _compute_metrics(
        self,
        results: list[EvalResult],
        metric_weights: dict[str, float],
    ) -> dict[str, float]:
        """Compute weighted scores by metric category.

        Args:
            results: List of evaluation results
            metric_weights: Dictionary mapping metric names to weights

        Returns:
            Dictionary of metric names to weighted scores
        """
        if not results or not metric_weights:
            return {}

        metrics = {}
        total_weight = sum(metric_weights.values())

        for metric_name, weight in metric_weights.items():
            if metric_name == "accuracy":
                score = sum(r.score for r in results) / len(results)
            elif metric_name == "pass_rate":
                score = sum(1 for r in results if r.passed) / len(results)
            elif metric_name == "speed":
                avg_time = sum(r.execution_time for r in results) / len(results)
                score = max(0.0, 1.0 - (avg_time / 10.0))
            else:
                score = sum(r.score for r in results) / len(results)

            normalized_weight = weight / total_weight if total_weight > 0 else 0
            metrics[metric_name] = score * normalized_weight

        return metrics

    def evaluate_with_llm(
        self,
        variant: SkillVariant,
        test_input: Any,
        expected: Any,
    ) -> EvalResult:
        """Evaluate using LLM-based judgment.

        Args:
            variant: Skill variant to evaluate
            test_input: Test input
            expected: Expected output

        Returns:
            EvalResult with LLM-based scoring
        """
        if not self.llm_client:
            return self._evaluate_single(
                variant, test_input, expected, EvaluationContext(), 0
            )

        try:
            prompt = f"""Evaluate this skill's performance:

**Skill Content:**
{variant.content[:1000]}

**Test Input:**
{test_input}

**Expected Output:**
{expected}

Rate the quality of this skill's response on a scale of 0.0 to 1.0.
Consider accuracy, completeness, and relevance.
Return only the numeric score."""

            response = self.llm_client.generate(prompt)
            score = float(response.strip())
            score = max(0.0, min(1.0, score))

            return EvalResult(
                input=test_input,
                expected=expected,
                actual=f"LLM-evaluated",
                score=score,
                passed=score >= self.default_threshold,
                metadata={"evaluation_method": "llm"},
            )

        except Exception as e:
            return EvalResult(
                input=test_input,
                expected=expected,
                actual=None,
                score=0.0,
                passed=False,
                error=str(e),
            )
