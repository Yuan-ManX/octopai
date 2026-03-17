"""
Octopai Integration Schemas - Data Models for Integration API

This module defines standardized data models for Octopai's integration API,
including request/response schemas and data transfer objects.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class IntegrationPipelineStage(Enum):
    """Pipeline stages for integration API"""
    PENDING = "pending"
    CREATION = "creation"
    OPTIMIZATION = "optimization"
    PACKAGING = "packaging"
    VALIDATION = "validation"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CreateSkillFromURLRequest:
    """Request schema for creating a skill from a URL"""
    url: str
    name: str
    description: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    author: Optional[str] = None
    skill_type: str = "general"
    auto_optimize: bool = True
    auto_package: bool = True
    auto_validate: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "category": self.category,
            "author": self.author,
            "skill_type": self.skill_type,
            "auto_optimize": self.auto_optimize,
            "auto_package": self.auto_package,
            "auto_validate": self.auto_validate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreateSkillFromURLRequest':
        return cls(**data)


@dataclass
class CreateSkillFromFilesRequest:
    """Request schema for creating a skill from files"""
    files: List[str]
    name: str
    description: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    author: Optional[str] = None
    skill_type: str = "general"
    auto_optimize: bool = True
    auto_package: bool = True
    auto_validate: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "files": self.files,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "category": self.category,
            "author": self.author,
            "skill_type": self.skill_type,
            "auto_optimize": self.auto_optimize,
            "auto_package": self.auto_package,
            "auto_validate": self.auto_validate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreateSkillFromFilesRequest':
        return cls(**data)


@dataclass
class CreateSkillFromPromptRequest:
    """Request schema for creating a skill from a prompt"""
    prompt: str
    name: str
    description: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    author: Optional[str] = None
    skill_type: str = "general"
    resources: Optional[List[str]] = None
    auto_optimize: bool = True
    auto_package: bool = True
    auto_validate: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "category": self.category,
            "author": self.author,
            "skill_type": self.skill_type,
            "resources": self.resources,
            "auto_optimize": self.auto_optimize,
            "auto_package": self.auto_package,
            "auto_validate": self.auto_validate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreateSkillFromPromptRequest':
        return cls(**data)


@dataclass
class OptimizeSkillRequest:
    """Request schema for optimizing an existing skill"""
    skill_dir: str
    max_iterations: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_dir": self.skill_dir,
            "max_iterations": self.max_iterations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OptimizeSkillRequest':
        return cls(**data)


@dataclass
class PipelineStatusResponse:
    """Response schema for pipeline status"""
    request_id: str
    status: IntegrationPipelineStage
    current_stage: Optional[str] = None
    progress: float = 0.0
    skill_id: Optional[str] = None
    skill_dir: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "current_stage": self.current_stage,
            "progress": self.progress,
            "skill_id": self.skill_id,
            "skill_dir": self.skill_dir,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "errors": self.errors,
            "warnings": self.warnings,
            "metrics": self.metrics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PipelineStatusResponse':
        data = data.copy()
        if 'status' in data:
            data['status'] = IntegrationPipelineStage(data['status'])
        return cls(**data)


@dataclass
class SkillInfoResponse:
    """Response schema for skill information"""
    skill_id: str
    name: str
    description: str
    skill_type: str
    tags: List[str] = field(default_factory=list)
    category: Optional[str] = None
    author: Optional[str] = None
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = None
    path: Optional[str] = None
    usage_count: int = 0
    success_rate: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "skill_type": self.skill_type,
            "tags": self.tags,
            "category": self.category,
            "author": self.author,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "path": self.path,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillInfoResponse':
        return cls(**data)


@dataclass
class ErrorResponse:
    """Response schema for errors"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorResponse':
        return cls(**data)


@dataclass
class SkillListResponse:
    """Response schema for skill list"""
    skills: List[SkillInfoResponse]
    total: int
    page: int = 1
    page_size: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skills": [s.to_dict() for s in self.skills],
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size
        }


@dataclass
class SkillSearchQuery:
    """Query schema for skill search"""
    query: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    limit: int = 10
    offset: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "tags": self.tags,
            "category": self.category,
            "limit": self.limit,
            "offset": self.offset
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillSearchQuery':
        return cls(**data)


@dataclass
class UpdateSkillMetadataRequest:
    """Request schema for updating skill metadata"""
    skill_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    author: Optional[str] = None
    keywords: Optional[List[str]] = None
    related_skills: Optional[List[str]] = None
    skill_type: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "category": self.category,
            "status": self.status,
            "visibility": self.visibility,
            "author": self.author,
            "keywords": self.keywords,
            "related_skills": self.related_skills,
            "skill_type": self.skill_type,
            "custom_fields": self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateSkillMetadataRequest':
        return cls(**data)


@dataclass
class CreateCollectionRequest:
    """Request schema for creating a skill collection"""
    name: str
    description: str
    skill_ids: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "skill_ids": self.skill_ids,
            "tags": self.tags,
            "author": self.author
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreateCollectionRequest':
        return cls(**data)


@dataclass
class CollectionResponse:
    """Response schema for a skill collection"""
    collection_id: str
    name: str
    description: str
    skill_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    author: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "collection_id": self.collection_id,
            "name": self.name,
            "description": self.description,
            "skill_ids": self.skill_ids,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author": self.author
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CollectionResponse':
        return cls(**data)


@dataclass
class CollectionListResponse:
    """Response schema for listing collections"""
    collections: List[CollectionResponse]
    total: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "collections": [c.to_dict() for c in self.collections],
            "total": self.total
        }


@dataclass
class AddRatingRequest:
    """Request schema for adding a skill rating"""
    skill_id: str
    rating: float
    feedback: Optional[str] = None
    reviewer: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "rating": self.rating,
            "feedback": self.feedback,
            "reviewer": self.reviewer
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AddRatingRequest':
        return cls(**data)


@dataclass
class RatingResponse:
    """Response schema for a skill rating"""
    rating_id: str
    skill_id: str
    rating: float
    feedback: Optional[str] = None
    reviewer: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rating_id": self.rating_id,
            "skill_id": self.skill_id,
            "rating": self.rating,
            "feedback": self.feedback,
            "reviewer": self.reviewer,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RatingResponse':
        return cls(**data)


@dataclass
class VersionDiffRequest:
    """Request schema for computing version diff"""
    skill_id: str
    from_version: int
    to_version: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "from_version": self.from_version,
            "to_version": self.to_version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionDiffRequest':
        return cls(**data)


@dataclass
class VersionDiffResponse:
    """Response schema for version diff"""
    diff_id: str
    skill_id: str
    from_version: int
    to_version: int
    additions: List[str] = field(default_factory=list)
    deletions: List[str] = field(default_factory=list)
    modifications: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "diff_id": self.diff_id,
            "skill_id": self.skill_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "additions": self.additions,
            "deletions": self.deletions,
            "modifications": self.modifications,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionDiffResponse':
        return cls(**data)


@dataclass
class RollbackRequest:
    """Request schema for rolling back a skill"""
    skill_id: str
    version: int
    author: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "version": self.version,
            "author": self.author
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RollbackRequest':
        return cls(**data)


@dataclass
class PublishSkillRequest:
    """Request schema for publishing a skill"""
    skill_id: str
    visibility: str = "public"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "visibility": self.visibility
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PublishSkillRequest':
        return cls(**data)


@dataclass
class ContextSlotSchema:
    """Schema for a context slot"""
    slot_id: str
    name: str
    description: str
    required: bool = True
    default_skill_id: Optional[str] = None
    allowed_skill_types: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot_id": self.slot_id,
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "default_skill_id": self.default_skill_id,
            "allowed_skill_types": self.allowed_skill_types
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSlotSchema':
        return cls(**data)


@dataclass
class CreateCompositionRequest:
    """Request schema for creating a context composition"""
    name: str
    description: str
    slots: Optional[Dict[str, ContextSlotSchema]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "slots": {k: v.to_dict() for k, v in self.slots.items()} if self.slots else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreateCompositionRequest':
        slots = None
        if data.get("slots"):
            slots = {
                k: ContextSlotSchema.from_dict(v)
                for k, v in data["slots"].items()
            }
        return cls(
            name=data["name"],
            description=data["description"],
            slots=slots
        )


@dataclass
class CompositionResponse:
    """Response schema for a context composition"""
    composition_id: str
    name: str
    description: str
    slots: Dict[str, ContextSlotSchema] = field(default_factory=dict)
    bindings: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "composition_id": self.composition_id,
            "name": self.name,
            "description": self.description,
            "slots": {k: v.to_dict() for k, v in self.slots.items()},
            "bindings": self.bindings,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompositionResponse':
        slots = {
            k: ContextSlotSchema.from_dict(v)
            for k, v in data.get("slots", {}).items()
        }
        return cls(
            composition_id=data["composition_id"],
            name=data["name"],
            description=data["description"],
            slots=slots,
            bindings=data.get("bindings", {}),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class CompositionListResponse:
    """Response schema for listing compositions"""
    compositions: List[CompositionResponse]
    total: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "compositions": [c.to_dict() for c in self.compositions],
            "total": self.total
        }


@dataclass
class BindSkillRequest:
    """Request schema for binding a skill to a slot"""
    composition_id: str
    slot_id: str
    skill_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "composition_id": self.composition_id,
            "slot_id": self.slot_id,
            "skill_id": self.skill_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BindSkillRequest':
        return cls(**data)


@dataclass
class SemanticSearchQuery:
    """Query schema for enhanced semantic search"""
    query: str
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    status: Optional[str] = None
    limit: int = 20
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "tags": self.tags,
            "category": self.category,
            "status": self.status,
            "limit": self.limit
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SemanticSearchQuery':
        return cls(**data)


@dataclass
class SemanticSearchResult:
    """Response schema for semantic search result"""
    skill: SkillInfoResponse
    score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill": self.skill.to_dict(),
            "score": self.score
        }


@dataclass
class SemanticSearchResponse:
    """Response schema for semantic search"""
    results: List[SemanticSearchResult]
    total: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total": self.total
        }
