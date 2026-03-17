"""
Octopai - Explore, Extend, Evolve AI Agent Cognition

Octopai is a revolutionary AI Agent Skills Exploration, Extension, and Evolution Framework
built on a powerful core principle: Everything Can Be a Skill.

Through intelligent learning and continuous self-evolution, Skills grow and improve
over time, significantly enhancing the cognitive capabilities of AI Agents.

Key Principles:
- Everything Can Be a Skill
- Skills Evolve Through Continuous Learning
- Elevate AI Agent Cognition
"""

__version__ = "0.1.0"
__author__ = "Octopai Team"

from octopai.core.converter import URLConverter
from octopai.core.resource_parser import (
    ResourceParser,
    parse_resource,
    parse_to_skill_resource,
    ParsedResource,
    ResourceType
)
from octopai.core.skill_factory import (
    SkillFactory,
    SkillDefinition,
    SkillMetadata,
    SkillVersion,
    SkillType,
    SkillQualityLevel,
    SkillQualityMetrics,
    SkillQualityEvaluator,
    SkillOptimizer,
    SkillTemplate,
    SkillInteractionPrototype,
    EnhancedQualityEvaluator,
    create_skill_with_template,
    generate_skill_prototype
)
from octopai.core.evolution_engine import (
    EvolutionEngine,
    EvolutionConfig,
    EvolutionObjective,
    EvolutionCandidate,
    EvolutionTrace,
    ActionableSideInfo
)
from octopai.core.skill_packager import (
    SkillPackager,
    PackageConfig
)
from octopai.core.skill_hub import (
    SkillHub,
    Skill
)
from octopai.core.experience_tracker import (
    ExperienceTracker,
    InteractionRecord,
    SkillExperience,
    InteractionType,
    InteractionOutcome
)
from octopai.core.pipeline import (
    OctopaiPipeline,
    PipelineConfig,
    PipelineResult,
    PipelineStage
)
from octopai.api import (
    Octopai,
    create_from_url,
    create_from_files,
    create_from_prompt,
    optimize_skill,
    convert,
    parse,
    hub_get,
    hub_search,
    hub_list,
    hub_stats,
    get_insights
)

__all__ = [
    "URLConverter",
    "ResourceParser",
    "parse_resource",
    "parse_to_skill_resource",
    "ParsedResource",
    "ResourceType",
    "SkillFactory",
    "SkillDefinition",
    "SkillMetadata",
    "SkillVersion",
    "SkillType",
    "SkillQualityLevel",
    "SkillQualityMetrics",
    "SkillQualityEvaluator",
    "SkillOptimizer",
    "SkillTemplate",
    "SkillInteractionPrototype",
    "EnhancedQualityEvaluator",
    "create_skill_with_template",
    "generate_skill_prototype",
    "EvolutionEngine",
    "EvolutionConfig",
    "EvolutionObjective",
    "EvolutionCandidate",
    "EvolutionTrace",
    "ActionableSideInfo",
    "SkillPackager",
    "PackageConfig",
    "SkillHub",
    "Skill",
    "ExperienceTracker",
    "InteractionRecord",
    "SkillExperience",
    "InteractionType",
    "InteractionOutcome",
    "OctopaiPipeline",
    "PipelineConfig",
    "PipelineResult",
    "PipelineStage",
    "Octopai",
    "create_from_url",
    "create_from_files",
    "create_from_prompt",
    "optimize_skill",
    "convert",
    "parse",
    "hub_get",
    "hub_search",
    "hub_list",
    "hub_stats",
    "get_insights",
    "__version__",
    "__author__",
]
