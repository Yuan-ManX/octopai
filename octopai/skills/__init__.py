"""
Octopai Skills Module - Comprehensive Skill Management System
Skill creation, registration, packaging, and distribution
"""

from .registry import SkillRegistry, RegistrySkillMetadata, SkillRegistryStatus
from .factory import SkillFactory, SkillDefinition, SkillMetadata, SkillVersion
from .hub import SkillHub, Skill
from .bank import SkillBank, BankedSkill, SkillPrinciple, CommonMistake, SkillType as BankSkillType
from .packager import SkillPackager, PackageConfig
from .spec import OctopaiSkillSpec as SkillSpec
from .templates import SkillTemplate, SkillTemplateLibrary as TemplateLibrary

# New modules (v4.0)
try:
    from .creator import (
        SkillCreator, TextParser, CodeParser, DocumentParser,
        MediaParser, PresentationParser, TemplateParser,
        SkillGenerator, SkillValidator,
        SkillCreationRequest, SkillSource, SourceType,
        GeneratedSkill, CreationResult,
    )
    from .hub_pkg import (  # Use alias to avoid conflict with original hub.py
        SkillRepository, RepositoryVisibility, RepositoryStatus,
        HubManager, PublishRequest, SearchResult, HubStatistics,
        PermissionManager, Role, Permission,
        MarketplaceManager, Rating, Review,
    )
except ImportError:
    pass

__all__ = [
    'SkillRegistry', 'RegistrySkillMetadata', 'SkillRegistryStatus',
    'SkillFactory', 'SkillDefinition', 'SkillMetadata', 'SkillVersion',
    'SkillHub', 'Skill',
    'SkillBank', 'BankedSkill', 'SkillPrinciple', 'CommonMistake', 'BankSkillType',
    'SkillPackager', 'PackageConfig',
    'SkillSpec',
    'SkillTemplate', 'TemplateLibrary'
]
