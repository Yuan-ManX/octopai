"""
EXO - Explore, Extend, Evolve AI Agent Cognition

EXO is a revolutionary AI Agent Skills Exploration, Extension, and Evolution Framework
built on a powerful core principle: Everything Can Be a Skill.

Through intelligent learning and continuous self-evolution, Skills grow and improve
over time, significantly enhancing the cognitive capabilities of AI Agents.

Key Principles:
- Everything Can Be a Skill
- Skills Evolve Through Continuous Learning
- Elevate AI Agent Cognition
"""

__version__ = "0.1.0"
__author__ = "EXO Team"

from exo.core.converter import URLConverter
from exo.core.resource_parser import (
    ResourceParser,
    parse_resource,
    parse_to_skill_resource,
    ParsedResource,
    ResourceType
)
from exo.core.skill_factory import (
    SkillFactory,
    SkillDefinition,
    SkillMetadata,
    SkillVersion,
    SkillType
)
from exo.core.evolution_engine import (
    EvolutionEngine,
    EvolutionConfig,
    EvolutionObjective,
    EvolutionCandidate,
    EvolutionTrace,
    ActionableSideInfo
)
from exo.core.skill_packager import (
    SkillPackager,
    PackageConfig
)
from exo.core.skill_hub import (
    SkillHub,
    Skill
)
from exo.core.experience_tracker import (
    ExperienceTracker,
    InteractionRecord,
    SkillExperience,
    InteractionType,
    InteractionOutcome
)
from exo.core.pipeline import (
    EXOPipeline,
    PipelineConfig,
    PipelineResult,
    PipelineStage
)
from exo.api import (
    EXO,
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
    "EXOPipeline",
    "PipelineConfig",
    "PipelineResult",
    "PipelineStage",
    "EXO",
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
