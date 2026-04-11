"""
Configuration and data models for skill evolution engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional


class EvolutionMode(str, Enum):
    """Dimension to optimize during evolution."""
    SKILL_ONLY = "skill_only"
    PROMPT_ONLY = "prompt_only"
    HYBRID = "hybrid"


class SelectionStrategy(str, Enum):
    """Strategy for selecting parent from frontier."""
    BEST = "best"
    RANDOM = "random"
    ROUND_ROBIN = "round_robin"


@dataclass
class EvolutionConfig:
    """Configuration for the evolution loop.

    Attributes:
        max_iterations: Maximum number of improvement iterations
        frontier_size: Number of top-performing variants to keep
        no_improvement_limit: Stop after this many iterations without improvement
        concurrency: Number of concurrent evaluations
        evolution_mode: Which dimension to evolve (skill/prompt/hybrid)
        selection_strategy: How to select parent from frontier
        samples_per_category: Number of samples per category to test
        categories_per_batch: Categories to sample per iteration
        reset_feedback: Reset feedback history on fresh start
        continue_mode: Continue from existing state
        cache_enabled: Enable result caching
        proposer_max_truncation_level: Max context truncation level
        proposer_single_failure_fallback: Try single failure if all fail
        consecutive_proposer_failures_limit: Max consecutive failures before stop
        target_score: Target score threshold to stop early
        mutation_rate: Probability of applying mutations (0.0-1.0)
        crossover_rate: Probability of crossover operations (0.0-1.0)
        elitism_count: Number of best variants to preserve unchanged
    """

    max_iterations: int = 10
    frontier_size: int = 5
    no_improvement_limit: int = 5
    concurrency: int = 4

    evolution_mode: EvolutionMode = EvolutionMode.SKILL_ONLY
    selection_strategy: SelectionStrategy = SelectionStrategy.BEST

    samples_per_category: int = 3
    categories_per_batch: int = 3

    reset_feedback: bool = True
    continue_mode: bool = False

    cache_enabled: bool = True
    cache_dir: Path = field(default_factory=lambda: Path(".cache/evolution"))

    proposer_max_truncation_level: int = 2
    proposer_single_failure_fallback: bool = True
    consecutive_proposer_failures_limit: int = 5

    target_score: float = 1.0
    mutation_rate: float = 0.3
    crossover_rate: float = 0.7
    elitism_count: int = 2


@dataclass
class LoopResult:
    """Result of running the evolution loop.

    Attributes:
        frontier: List of (variant_name, score) tuples sorted by score
        best_variant: Name of the best-performing variant
        best_score: Score of the best variant
        iterations_completed: Number of iterations completed
        total_cost_usd: Total cost in USD (if applicable)
        total_time_seconds: Total execution time
        improvements_made: Total number of successful improvements
        mutations_applied: Total number of mutations applied
        evaluation_results: Detailed results per iteration
    """

    frontier: list[tuple[str, float]] = field(default_factory=list)
    best_variant: str = ""
    best_score: float = 0.0
    iterations_completed: int = 0
    total_cost_usd: float = 0.0
    total_time_seconds: float = 0.0
    improvements_made: int = 0
    mutations_applied: int = 0
    evaluation_results: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SkillVariant:
    """Represents a single skill variant in the evolution process.

    Attributes:
        name: Unique identifier for this variant
        content: The skill content/markdown
        score: Current performance score
        generation: Generation number (0 = original)
        parent: Parent variant name (None for original)
        mutations: List of mutations applied to create this variant
        metadata: Additional metadata about the variant
        created_at: Timestamp when variant was created
    """

    name: str
    content: str
    score: float = 0.0
    generation: int = 0
    parent: Optional[str] = None
    mutations: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationContext:
    """Context for evaluating a skill variant.

    Attributes:
        test_cases: List of test cases (input, expected_output) tuples
        category: Category of the evaluation
        metrics: Dictionary of metric names to weights
        timeout: Timeout per test case in seconds
        max_retries: Maximum retries on failure
    """

    test_cases: list[tuple[Any, Any]] = field(default_factory=list)
    category: str = "general"
    metrics: dict[str, float] = field(default_factory=lambda: {"accuracy": 1.0})
    timeout: float = 30.0
    max_retries: int = 3


@dataclass
class MutationRecord:
    """Record of a mutation operation.

    Attributes:
        mutation_type: Type of mutation applied
        description: Human-readable description
        source_section: Section that was modified
        old_content: Content before mutation
        new_content: Content after mutation
        success: Whether mutation was successful
        timestamp: When mutation was applied
    """

    mutation_type: str
    description: str
    source_section: str
    old_content: str = ""
    new_content: str = ""
    success: bool = True
    timestamp: Optional[float] = None
