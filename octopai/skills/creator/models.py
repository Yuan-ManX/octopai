"""
Data models for skill creation system.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Supported input source types for skill creation."""
    TEXT = "text"
    CODE = "code"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    PRESENTATION = "presentation"
    TEMPLATE = "template"
    URL = "url"
    NATURAL_LANGUAGE = "natural_language"


class SkillSource(BaseModel):
    """Input source for skill creation."""
    source_type: SourceType
    content: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class SkillCreationRequest(BaseModel):
    """Request to create a new skill."""
    name: str
    description: str = ""
    sources: list[SkillSource] = Field(default_factory=list)
    category: str = "general"
    tags: list[str] = Field(default_factory=list)
    version: str = "1.0.0"
    author: str = ""
    config: dict[str, Any] = Field(default_factory=dict)


class GeneratedSkill(BaseModel):
    """Represents a generated skill."""
    id: str = ""
    name: str
    description: str
    version: str = "1.0.0"
    category: str = "general"
    tags: list[str] = Field(default_factory=list)
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_type: SourceType = SourceType.TEXT
    created_at: datetime = Field(default_factory=datetime.now)
    validation_score: float = 0.0
    status: str = "draft"

    class Config:
        use_enum_values = True


class CreationResult(BaseModel):
    """Result of skill creation operation."""
    success: bool
    skill: Optional[GeneratedSkill] = None
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    processing_time_ms: float = 0.0
    source_analysis: dict[str, Any] = Field(default_factory=dict)


class ParsedContent(BaseModel):
    """Parsed content from input source."""
    raw_text: str = ""
    structured_data: dict[str, Any] = Field(default_factory=dict)
    code_blocks: list[dict[str, str]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    quality_score: float = 0.0
