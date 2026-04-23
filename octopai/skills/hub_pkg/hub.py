"""
Data models for Octopai Skills Hub - Enterprise-grade skill repository system.

Core Features:
- Namespace-based organization (Global + Team namespaces)
- Complete skill version state machine
- Review workflow and promotion system
- Audit logging for compliance
- Semantic versioning with tags
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field


class NamespaceType(str, Enum):
    """Type of namespace - Global or Team."""
    GLOBAL = "global"
    TEAM = "team"


class NamespaceStatus(str, Enum):
    """Status of a namespace."""
    ACTIVE = "active"
    FROZEN = "frozen"
    ARCHIVED = "archived"


class NamespaceMemberRole(str, Enum):
    """Roles for namespace members."""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class SkillVisibility(str, Enum):
    """Visibility settings for skills."""
    PUBLIC = "public"
    NAMESPACE_ONLY = "namespace_only"
    PRIVATE = "private"


class SkillStatus(str, Enum):
    """Status of a skill container."""
    ACTIVE = "active"
    ARCHIVED = "archived"


class VersionStatus(str, Enum):
    """Status of a skill version."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    REJECTED = "rejected"
    YANKED = "yanked"


class ReviewStatus(str, Enum):
    """Status of a review task."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PlatformRole(str, Enum):
    """Platform-level roles for users."""
    SUPER_ADMIN = "super_admin"
    SKILL_ADMIN = "skill_admin"
    USER_ADMIN = "user_admin"
    AUDITOR = "auditor"


class NamespaceMember(BaseModel):
    """Member of a namespace with role.
    
    Attributes:
        namespace_id: ID of the namespace
        user_id: User ID of the member
        role: Role (owner/admin/member)
        created_at: When the membership was created
        updated_at: When the membership was last updated
    """
    namespace_id: str
    user_id: str
    role: NamespaceMemberRole = NamespaceMemberRole.MEMBER
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Namespace(BaseModel):
    """Namespace - organizational unit for skills.
    
    Attributes:
        id: Unique namespace identifier
        slug: URL-friendly name (e.g., "team-frontend")
        display_name: Human-readable name
        type: Namespace type (global/team)
        description: Description of the namespace
        avatar_url: Optional avatar image URL
        status: Current status
        created_by: User who created the namespace
        created_at: Creation timestamp
        updated_at: Last update timestamp
        members: List of namespace members
    """
    id: str = ""
    slug: str = ""
    display_name: str = ""
    type: NamespaceType = NamespaceType.TEAM
    description: str = ""
    avatar_url: Optional[str] = None
    status: NamespaceStatus = NamespaceStatus.ACTIVE
    created_by: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    members: List[NamespaceMember] = Field(default_factory=list)


class SkillTag(BaseModel):
    """Tag for a skill version.
    
    Attributes:
        id: Tag ID
        skill_id: Skill ID
        tag_name: Tag name (e.g., "latest", "beta")
        target_version_id: Version ID that this tag points to
        created_by: User who created the tag
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str = ""
    skill_id: str = ""
    tag_name: str = ""
    target_version_id: str = ""
    created_by: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SkillFile(BaseModel):
    """File associated with a skill version.
    
    Attributes:
        id: File ID
        skill_version_id: Version ID
        file_path: Path within the skill package
        content_type: MIME type
        size_bytes: File size in bytes
        sha256: SHA256 hash for integrity
        object_key: Storage key in object storage
        is_entry_file: Whether this is the main entry file
        created_at: Creation timestamp
    """
    id: str = ""
    skill_version_id: str = ""
    file_path: str = ""
    content_type: str = "text/plain"
    size_bytes: int = 0
    sha256: str = ""
    object_key: str = ""
    is_entry_file: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class SkillVersion(BaseModel):
    """Version of a skill with complete state machine.
    
    Attributes:
        id: Unique version identifier
        skill_id: Parent skill ID
        version: Semantic version string (e.g., "1.0.0")
        changelog: Changes in this version
        manifest_json: File manifest
        parsed_metadata_json: Parsed SKILL.md frontmatter
        status: Current status
        reject_reason: If rejected, the reason
        published_by: User who published
        published_at: When published
        created_at: Creation timestamp
        files: List of files in this version
        tags: Tags pointing to this version
    """
    id: str = ""
    skill_id: str = ""
    version: str = "1.0.0"
    changelog: str = ""
    manifest_json: Dict[str, Any] = Field(default_factory=dict)
    parsed_metadata_json: Dict[str, Any] = Field(default_factory=dict)
    status: VersionStatus = VersionStatus.DRAFT
    reject_reason: Optional[str] = None
    published_by: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    files: List[SkillFile] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Skill(BaseModel):
    """Skill container with metadata.
    
    Attributes:
        id: Unique skill identifier
        namespace_id: Namespace that contains this skill
        slug: URL-friendly name
        display_name: Human-readable name
        summary: Short summary
        owner_id: Primary maintainer
        source_skill_id: If promoted from another skill
        visibility: Visibility setting
        status: Current status
        hidden: Whether this skill is hidden
        hidden_at: When hidden
        hidden_by: Who hid it
        latest_version_id: Current published version ID
        download_count: Number of downloads
        star_count: Number of stars
        rating_avg: Average rating (1-5)
        rating_count: Number of ratings
        created_by: Creator
        created_at: Creation timestamp
        updated_by: Last updater
        updated_at: Last update timestamp
        versions: List of versions
        tags: List of tags
        category: Skill category
        topics: Topic tags
    """
    id: str = ""
    namespace_id: str = ""
    slug: str = ""
    display_name: str = ""
    summary: str = ""
    owner_id: str = ""
    source_skill_id: Optional[str] = None
    visibility: SkillVisibility = SkillVisibility.PRIVATE
    status: SkillStatus = SkillStatus.ACTIVE
    hidden: bool = False
    hidden_at: Optional[datetime] = None
    hidden_by: Optional[str] = None
    latest_version_id: Optional[str] = None
    download_count: int = 0
    star_count: int = 0
    rating_avg: float = 0.0
    rating_count: int = 0
    created_by: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str = ""
    updated_at: datetime = Field(default_factory=datetime.now)
    versions: List[SkillVersion] = Field(default_factory=list)
    tags: List[SkillTag] = Field(default_factory=list)
    category: str = "general"
    topics: List[str] = Field(default_factory=list)


class ReviewTask(BaseModel):
    """Review task for a skill version.
    
    Attributes:
        id: Review task ID
        skill_version_id: Version being reviewed
        namespace_id: Namespace context
        status: Current status
        version: Optimistic lock version
        submitted_by: Submitter
        reviewed_by: Reviewer
        review_comment: Comment from reviewer
        submitted_at: When submitted
        reviewed_at: When reviewed
    """
    id: str = ""
    skill_version_id: str = ""
    namespace_id: str = ""
    status: ReviewStatus = ReviewStatus.PENDING
    version: int = 1
    submitted_by: str = ""
    reviewed_by: Optional[str] = None
    review_comment: str = ""
    submitted_at: datetime = Field(default_factory=datetime.now)
    reviewed_at: Optional[datetime] = None


class PromotionRequest(BaseModel):
    """Request to promote a team skill to global namespace.
    
    Attributes:
        id: Request ID
        source_skill_id: Original team skill
        source_version_id: Version being promoted
        target_namespace_id: Target namespace (usually global)
        target_skill_id: Created skill ID after approval
        status: Current status
        version: Optimistic lock version
        submitted_by: Submitter
        reviewed_by: Reviewer
        review_comment: Review comment
        submitted_at: When submitted
        reviewed_at: When reviewed
    """
    id: str = ""
    source_skill_id: str = ""
    source_version_id: str = ""
    target_namespace_id: str = ""
    target_skill_id: Optional[str] = None
    status: ReviewStatus = ReviewStatus.PENDING
    version: int = 1
    submitted_by: str = ""
    reviewed_by: Optional[str] = None
    review_comment: str = ""
    submitted_at: datetime = Field(default_factory=datetime.now)
    reviewed_at: Optional[datetime] = None


class SkillStar(BaseModel):
    """Record of a user starring a skill.
    
    Attributes:
        id: Star record ID
        skill_id: Skill being starred
        user_id: User who starred
        created_at: When starred
    """
    id: str = ""
    skill_id: str = ""
    user_id: str = ""
    created_at: datetime = Field(default_factory=datetime.now)


class SkillRating(BaseModel):
    """Rating for a skill.
    
    Attributes:
        id: Rating ID
        skill_id: Skill being rated
        user_id: User who rated
        score: Rating 1-5
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str = ""
    skill_id: str = ""
    user_id: str = ""
    score: int = 5
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AuditLog(BaseModel):
    """Audit log entry for compliance.
    
    Attributes:
        id: Log entry ID
        actor_user_id: User who performed the action
        action: Action type (e.g., "create", "publish", "review")
        target_type: Type of target (e.g., "skill", "namespace")
        target_id: Target ID
        request_id: Request ID for tracing
        client_ip: Client IP address
        user_agent: User agent
        detail_json: Additional details
        created_at: When the event happened
    """
    id: str = ""
    actor_user_id: str = ""
    action: str = ""
    target_type: str = ""
    target_id: str = ""
    request_id: Optional[str] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    detail_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)


class UserAccount(BaseModel):
    """User account in Octopai.
    
    Attributes:
        id: User ID
        display_name: Display name
        email: Email address
        avatar_url: Avatar URL
        status: Account status
        platform_roles: List of platform-level roles
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str = ""
    display_name: str = ""
    email: str = ""
    avatar_url: Optional[str] = None
    status: str = "active"
    platform_roles: List[PlatformRole] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SkillSearchDocument(BaseModel):
    """Search index document for skills.
    
    Attributes:
        id: Document ID
        skill_id: Skill ID
        namespace_id: Namespace ID
        title: Searchable title
        summary: Searchable summary
        keywords: Keywords
        search_text: Full search text
        visibility: Visibility
        status: Status
        updated_at: Last update
    """
    id: str = ""
    skill_id: str = ""
    namespace_id: str = ""
    title: str = ""
    summary: str = ""
    keywords: List[str] = Field(default_factory=list)
    search_text: str = ""
    visibility: SkillVisibility = SkillVisibility.PUBLIC
    status: SkillStatus = SkillStatus.ACTIVE
    updated_at: datetime = Field(default_factory=datetime.now)


class SkillHubEvent(BaseModel):
    """Event for skill hub activities.
    
    Attributes:
        event_type: Type of event
        skill_id: Related skill ID
        namespace_id: Related namespace
        user_id: User who triggered
        timestamp: Event timestamp
        metadata: Additional metadata
    """
    event_type: str = ""
    skill_id: Optional[str] = None
    namespace_id: Optional[str] = None
    user_id: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RepositoryVisibility(str, Enum):
    """Legacy visibility setting for backward compatibility."""
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class RepositoryStatus(str, Enum):
    """Legacy repository status for backward compatibility."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class SkillRepository(BaseModel):
    """Legacy repository model for backward compatibility.
    
    Attributes:
        id: Unique repository identifier
        name: Repository name (slug format)
        display_name: Human-readable name
        description: Short description
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
    """Legacy repository event for backward compatibility."""
    event_type: str = ""
    repository_id: str = ""
    user_id: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ForkRecord(BaseModel):
    """Legacy fork record for backward compatibility."""
    source_repo_id: str = ""
    forked_repo_id: str = ""
    forked_by: str = ""
    forked_at: datetime = Field(default_factory=datetime.now)
    is_upstream_synced: bool = False

