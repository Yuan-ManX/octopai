"""
Data models for Skills Hub repository system.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, List
from pydantic import BaseModel, Field


class RepositoryVisibility(str, Enum):
    """Visibility settings for skill repositories."""
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class RepositoryStatus(str, Enum):
    """Status of a skill repository."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class SkillVersion(BaseModel):
    """Represents a specific version of a skill.

    Attributes:
        version: Semantic version string (e.g., "1.0.0")
        content: Skill content in markdown format
        changelog: Changes in this version
        created_at: When this version was created
        created_by: User who created this version
        is_latest: Whether this is the latest version
        download_count: Number of downloads
        metadata: Additional version metadata
    """

    version: str = "1.0.0"
    content: str = ""
    changelog: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str = ""
    is_latest: bool = False
    download_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class SkillRepository(BaseModel):
    """Complete skill repository with full metadata.

    Attributes:
        id: Unique repository identifier
        name: Repository name (slug format)
        display_name: Human-readable name
        description: Short description
        long_description: Detailed markdown description
        owner: Owner username or organization
        visibility: Visibility setting (public/private/unlisted)
        status: Current status (draft/published/archived)
        category: Primary category
        tags: List of searchable tags
        versions: List of all versions
        current_version: Current active version string
        stars: Star count
        forks: Fork count
        watchers: Watcher count
        created_at: Creation timestamp
        updated_at: Last update timestamp
        published_at: Publication timestamp (if published)
        license: License type (e.g., MIT, Apache-2.0)
        language: Primary programming language
        topics: List of topic areas
        readme_content: README file content
        contributors: List of contributor usernames
        dependencies: List of required dependencies
        config: Repository configuration
        statistics: Usage and performance statistics
    """

    id: str = ""
    name: str = ""
    display_name: str = ""
    description: str = ""
    long_description: str = ""

    owner: str = ""
    visibility: RepositoryVisibility = RepositoryVisibility.PRIVATE
    status: RepositoryStatus = RepositoryStatus.DRAFT

    category: str = "general"
    tags: List[str] = Field(default_factory=list)

    versions: List[SkillVersion] = Field(default_factory=list)
    current_version: str = "1.0.0"

    stars: int = 0
    forks: int = 0
    watchers: int = 0

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = None

    license: str = "MIT"
    language: str = ""
    topics: List[str] = Field(default_factory=list)

    readme_content: str = ""
    contributors: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)

    config: dict[str, Any] = Field(default_factory=dict)
    statistics: dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class RepositoryEvent(BaseModel):
    """Event tracking for repository activities.

    Attributes:
        event_type: Type of event (create, publish, fork, star, etc.)
        repository_id: Target repository ID
        user_id: User who triggered the event
        timestamp: When the event occurred
        metadata: Additional event data
    """

    event_type: str = ""
    repository_id: str = ""
    user_id: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ForkRecord(BaseModel):
    """Record of a repository fork operation.

    Attributes:
        source_repo_id: Original repository ID
        forked_repo_id: New forked repository ID
        forked_by: User who created the fork
        forked_at: When the fork was created
        is_upstream_synced: Whether fork is synced with upstream
    """

    source_repo_id: str = ""
    forked_repo_id: str = ""
    forked_by: str = ""
    forked_at: datetime = Field(default_factory=datetime.now)
    is_upstream_synced: bool = False
