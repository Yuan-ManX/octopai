"""
Skill Hub Data Models
Core data structures for skill registry
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class Visibility(str, Enum):
    """Visibility levels for skills"""
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"


class SkillStatus(str, Enum):
    """Status of a skill"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


@dataclass
class User:
    """User account for skill management"""
    user_id: str
    username: str
    email: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class Organization:
    """Organization for team skill management"""
    org_id: str
    name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "org_id": self.org_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "logo_url": self.logo_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class SkillMetadata:
    """Metadata for a skill"""
    name: str
    description: str
    version: str
    author: str
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    license: Optional[str] = None
    homepage: Optional[str] = None
    repository: Optional[str] = None
    documentation: Optional[str] = None
    compatibility: Optional[Dict[str, Any]] = None
    requirements: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "category": self.category,
            "tags": self.tags,
            "keywords": self.keywords,
            "license": self.license,
            "homepage": self.homepage,
            "repository": self.repository,
            "documentation": self.documentation,
            "compatibility": self.compatibility,
            "requirements": self.requirements
        }


@dataclass
class SkillVersion:
    """A specific version of a skill"""
    version_id: str
    skill_id: str
    version: str
    metadata: SkillMetadata
    content: str
    created_by: str
    changelog: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    download_count: int = 0
    is_latest: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "version_id": self.version_id,
            "skill_id": self.skill_id,
            "version": self.version,
            "metadata": self.metadata.to_dict(),
            "content": self.content,
            "changelog": self.changelog,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "download_count": self.download_count,
            "is_latest": self.is_latest
        }


@dataclass
class Skill:
    """Main skill registry entry"""
    skill_id: str
    name: str
    slug: str
    description: str
    visibility: Visibility
    status: SkillStatus
    owner_type: str  # "user" or "organization"
    owner_id: str
    namespace: str  # username or org slug
    metadata: SkillMetadata
    created_by: str
    latest_version: Optional[SkillVersion] = None
    versions: List[SkillVersion] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    star_count: int = 0
    fork_count: int = 0
    view_count: int = 0
    download_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "visibility": self.visibility.value,
            "status": self.status.value,
            "owner_type": self.owner_type,
            "owner_id": self.owner_id,
            "namespace": self.namespace,
            "metadata": self.metadata.to_dict(),
            "latest_version": self.latest_version.to_dict() if self.latest_version else None,
            "categories": self.categories,
            "tags": self.tags,
            "star_count": self.star_count,
            "fork_count": self.fork_count,
            "view_count": self.view_count,
            "download_count": self.download_count,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
