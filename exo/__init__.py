"""
EXO - Explore, Extend, Evolve AI Agent Cognition.

EXO is a comprehensive AI Agent skills development platform designed to expand the cognitive boundaries of AI Agents.
"""

__version__ = "0.1.0"
__author__ = "EXO Team"

from exo.core.converter import URLConverter
from exo.core.creator import SkillCreator
from exo.core.evolver import SkillEvolver
from exo.core.evolution_engine import EvolutionEngine
from exo.core.resource_parser import (
    ResourceParser,
    parse_resource,
    parse_to_skill_resource,
    ParsedResource,
    ResourceType
)
from exo.core.skill_hub import (
    SkillHub,
    Skill,
    SkillVersion,
    SkillMetadata
)
from exo.api import EXO, convert, create, evolve, process, hub_create, hub_get, hub_search, hub_list, hub_stats


__all__ = [
    "URLConverter",
    "SkillCreator",
    "SkillEvolver",
    "EvolutionEngine",
    "ResourceParser",
    "parse_resource",
    "parse_to_skill_resource",
    "ParsedResource",
    "ResourceType",
    "SkillHub",
    "Skill",
    "SkillVersion",
    "SkillMetadata",
    "EXO",
    "convert",
    "create",
    "evolve",
    "process",
    "hub_create",
    "hub_get",
    "hub_search",
    "hub_list",
    "hub_stats",
    "__version__",
    "__author__",
]
