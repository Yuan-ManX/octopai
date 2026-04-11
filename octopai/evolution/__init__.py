"""
Skill Evolution Engine - Self-improving skill evolution system.

Implements a complete self-evolution loop for skills:
- Evaluation and scoring
- Mutation and variation generation
- Frontier management (top-performing variants)
- Feedback-driven improvement
- Version control and checkpointing

Advanced optimization:
- Feedback Descent algorithm for pairwise comparison optimization
- Intelligent proposal generation based on failure analysis
- LLM-guided improvement suggestions
"""

from .evolution_engine import (
    SkillEvolutionEngine,
    EvolutionConfig,
    EvolutionMode,
    SelectionStrategy,
    LoopResult,
)
from .config import (
    SkillVariant,
    EvaluationContext,
    MutationRecord,
)
from .frontier import FrontierManager
from .evaluator import SkillEvaluator, EvalResult, BatchEvalResult
from .mutator import SkillMutator, MutationProposal, MutationResult
from .feedback import FeedbackHistory, FeedbackEntry
from .version_control import VersionManager
from .feedback_descent import (
    FeedbackDescentOptimizer,
    ComparisonResult,
    FeedbackRecord as FDFeedbackRecord,
    Proposal,
    OptimizationState,
    create_default_proposer,
)

__all__ = [
    "SkillEvolutionEngine",
    "EvolutionConfig",
    "EvolutionMode",
    "SelectionStrategy",
    "LoopResult",
    "SkillVariant",
    "EvaluationContext",
    "MutationRecord",
    "FrontierManager",
    "SkillEvaluator",
    "EvalResult",
    "BatchEvalResult",
    "SkillMutator",
    "MutationProposal",
    "MutationResult",
    "FeedbackHistory",
    "FeedbackEntry",
    "VersionManager",
    # Advanced Optimization
    "FeedbackDescentOptimizer",
    "ComparisonResult",
    "FDFeedbackRecord",
    "Proposal",
    "OptimizationState",
    "create_default_proposer",
]
