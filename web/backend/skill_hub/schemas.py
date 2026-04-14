"""
Skill Hub API Schemas
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SkillMetadataRequest(BaseModel):
    """Request model for skill metadata"""
    name: str = Field(..., description="Name of the skill")
    description: str = Field(..., description="Description of the skill")
    version: str = Field(default="1.0.0", description="Semantic version")
    author: str = Field(..., description="Author of the skill")
    category: Optional[str] = Field(None, description="Category of the skill")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for the skill")
    keywords: Optional[List[str]] = Field(default_factory=list, description="Search keywords")
    license: Optional[str] = Field(None, description="License type")
    homepage: Optional[str] = Field(None, description="Homepage URL")
    repository: Optional[str] = Field(None, description="Repository URL")
    documentation: Optional[str] = Field(None, description="Documentation URL")
    compatibility: Optional[Dict[str, Any]] = Field(None, description="Compatibility info")
    requirements: Optional[List[str]] = Field(None, description="Skill requirements")


class SkillCreateRequest(BaseModel):
    """Request model for creating a new skill"""
    name: str = Field(..., description="Name of the skill")
    description: str = Field(..., description="Description of the skill")
    namespace: str = Field(..., description="Namespace (username or org slug)")
    visibility: str = Field(default="public", description="Visibility: public, private, internal")
    content: str = Field(..., description="Skill content")
    metadata: SkillMetadataRequest
    categories: Optional[List[str]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)


class SkillUpdateRequest(BaseModel):
    """Request model for updating a skill"""
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class SkillVersionCreateRequest(BaseModel):
    """Request model for creating a new skill version"""
    version: str = Field(..., description="Semantic version")
    content: str = Field(..., description="Skill content")
    metadata: SkillMetadataRequest
    changelog: Optional[str] = None


class SkillResponse(BaseModel):
    """Response model for a skill"""
    skill_id: str
    name: str
    slug: str
    description: str
    visibility: str
    status: str
    owner_type: str
    owner_id: str
    namespace: str
    metadata: Dict[str, Any]
    latest_version: Optional[Dict[str, Any]] = None
    categories: List[str]
    tags: List[str]
    star_count: int
    fork_count: int
    view_count: int
    download_count: int
    created_by: str
    created_at: str
    updated_at: str


class SkillVersionResponse(BaseModel):
    """Response model for a skill version"""
    version_id: str
    skill_id: str
    version: str
    metadata: Dict[str, Any]
    content: str
    changelog: Optional[str] = None
    created_by: str
    created_at: str
    download_count: int
    is_latest: bool


class SkillListResponse(BaseModel):
    """Response model for skill list"""
    skills: List[SkillResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class SearchRequest(BaseModel):
    """Request model for skill search"""
    query: str = Field("", description="Search query")
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    visibility: Optional[str] = None
    namespace: Optional[str] = None
    sort_by: str = Field("updated_at", description="Sort field")
    sort_order: str = Field("desc", description="Sort order: asc, desc")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class StarRequest(BaseModel):
    """Request model for starring/unstarring a skill"""
    starred: bool


class ForkRequest(BaseModel):
    """Request model for forking a skill"""
    new_namespace: str
    new_name: Optional[str] = None
