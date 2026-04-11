"""
Skill Creator Module - Multi-format Skill Generation System

Supports creating skills from various input types:
- Text/Document inputs (Markdown, PDF, DOCX)
- Code repositories (GitHub, local files)
- Audio/Video content (transcription-based)
- Presentations (PPT, Keynote)
- Natural language descriptions
- Existing skill templates

Enhanced with intelligent content analysis for optimal skill generation.
"""

from .creator import SkillCreator
from .parsers import (
    TextParser,
    CodeParser,
    DocumentParser,
    MediaParser,
    PresentationParser,
    TemplateParser,
)
from .generator import SkillGenerator
from .validators import SkillValidator
from .analyzer import IntelligentAnalyzer, ContentAnalysis, ContentType
from .models import (
    SkillCreationRequest,
    SkillSource,
    SourceType,
    GeneratedSkill,
    CreationResult,
)

__all__ = [
    "SkillCreator",
    "TextParser",
    "CodeParser",
    "DocumentParser",
    "MediaParser",
    "PresentationParser",
    "TemplateParser",
    "SkillGenerator",
    "SkillValidator",
    "IntelligentAnalyzer",
    "ContentAnalysis",
    "ContentType",
    "SkillCreationRequest",
    "SkillSource",
    "SourceType",
    "GeneratedSkill",
    "CreationResult",
]
