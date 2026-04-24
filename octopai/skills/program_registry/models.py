"""
Program Registry Models

Data models for storing and managing agent configurations, skills,
and programs with version control and frontier management.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time
import json
from pathlib import Path


class ProgramStatus(Enum):
    """Status of a program in the registry."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    PENDING = "pending"
    FAILED = "failed"


class SkillType(Enum):
    """Types of skills that can be created."""
    CODE = "code"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CREATION = "creation"
    AUTOMATION = "automation"
    CUSTOM = "custom"


@dataclass
class SkillMetadata:
    """Metadata for a skill."""
    name: str
    version: str = "1.0.0"
    author: Optional[str] = None
    license: Optional[str] = None
    category: str = "general"
    keywords: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    quality_score: float = 0.0
    usage_count: int = 0
    success_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "license": self.license,
            "category": self.category,
            "keywords": self.keywords,
            "tags": self.tags,
            "description": self.description,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "quality_score": self.quality_score,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillMetadata":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            version=data.get("version", "1.0.0"),
            author=data.get("author"),
            license=data.get("license"),
            category=data.get("category", "general"),
            keywords=data.get("keywords", []),
            tags=data.get("tags", []),
            description=data.get("description", ""),
            dependencies=data.get("dependencies", []),
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            quality_score=data.get("quality_score", 0.0),
            usage_count=data.get("usage_count", 0),
            success_rate=data.get("success_rate", 0.0),
            metadata=data.get("metadata", {})
        )


@dataclass
class Skill:
    """A skill that can be used by an agent."""
    metadata: SkillMetadata
    content: str
    path: Optional[str] = None
    is_active: bool = True
    id: Optional[str] = None

    def __post_init__(self):
        if self.id is None:
            self.id = f"{self.metadata.name.replace(' ', '_')}_{int(time.time())}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "metadata": self.metadata.to_dict(),
            "content": self.content,
            "path": self.path,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            metadata=SkillMetadata.from_dict(data["metadata"]),
            content=data["content"],
            path=data.get("path"),
            is_active=data.get("is_active", True)
        )


@dataclass
class ProgramConfig:
    """Configuration for a program (agent + skills)."""
    name: str
    system_prompt: str
    skills: List[Skill] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    output_format: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    generation: int = 0
    parent_name: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mutate(self, new_name: str) -> "ProgramConfig":
        """Create a mutated copy of this config."""
        return ProgramConfig(
            name=new_name,
            system_prompt=self.system_prompt,
            skills=list(self.skills),
            allowed_tools=list(self.allowed_tools),
            output_format=self.output_format,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            generation=self.generation + 1,
            parent_name=self.name,
            metadata=dict(self.metadata)
        )

    def with_timestamp(self) -> "ProgramConfig":
        """Update the created_at timestamp."""
        self.created_at = time.time()
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "system_prompt": self.system_prompt,
            "skills": [s.to_dict() for s in self.skills],
            "allowed_tools": self.allowed_tools,
            "output_format": self.output_format,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "generation": self.generation,
            "parent_name": self.parent_name,
            "created_at": self.created_at,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgramConfig":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            system_prompt=data["system_prompt"],
            skills=[Skill.from_dict(s) for s in data.get("skills", [])],
            allowed_tools=data.get("allowed_tools", []),
            output_format=data.get("output_format"),
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens"),
            generation=data.get("generation", 0),
            parent_name=data.get("parent_name"),
            created_at=data.get("created_at", time.time()),
            metadata=data.get("metadata", {})
        )


@dataclass
class ProgramEntry:
    """A program entry in the registry."""
    config: ProgramConfig
    score: float = 0.0
    status: ProgramStatus = ProgramStatus.ACTIVE
    evaluation_results: List[Dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_evaluated: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "config": self.config.to_dict(),
            "score": self.score,
            "status": self.status.value,
            "evaluation_results": self.evaluation_results,
            "created_at": self.created_at,
            "last_evaluated": self.last_evaluated
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgramEntry":
        """Create from dictionary."""
        return cls(
            config=ProgramConfig.from_dict(data["config"]),
            score=data.get("score", 0.0),
            status=ProgramStatus(data.get("status", "active")),
            evaluation_results=data.get("evaluation_results", []),
            created_at=data.get("created_at", time.time()),
            last_evaluated=data.get("last_evaluated")
        )


@dataclass
class Experiment:
    """An experiment configuration for AutoSkill."""
    id: str
    name: str
    description: str
    task_config: Dict[str, Any]
    dataset_config: Dict[str, Any]
    evolution_config: Dict[str, Any]
    status: str = "pending"
    results: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    logs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task_config": self.task_config,
            "dataset_config": self.dataset_config,
            "evolution_config": self.evolution_config,
            "status": self.status,
            "results": self.results,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "logs": self.logs
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experiment":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            task_config=data.get("task_config", {}),
            dataset_config=data.get("dataset_config", {}),
            evolution_config=data.get("evolution_config", {}),
            status=data.get("status", "pending"),
            results=data.get("results"),
            created_at=data.get("created_at", time.time()),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            logs=data.get("logs", [])
        )
