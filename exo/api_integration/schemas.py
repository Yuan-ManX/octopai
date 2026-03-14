"""
EXO Integration Schemas - Data Models for Integration API

This module defines standardized data models for EXO's integration API,
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
    status: WebPipelineStage
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
            data['status'] = WebPipelineStage(data['status'])
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
