"""
Program Registry Models
Data models for program configurations and metadata
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class ProgramMetadata:
    """Metadata for a program"""
    name: str
    parent: Optional[str] = None
    generation: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    score: Optional[float] = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "parent": self.parent,
            "generation": self.generation,
            "created_at": self.created_at,
            "score": self.score,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgramMetadata":
        """Create from dictionary"""
        return cls(
            name=data["name"],
            parent=data.get("parent"),
            generation=data.get("generation", 0),
            created_at=data.get("created_at", datetime.now().isoformat()),
            score=data.get("score"),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class ProgramConfig:
    """Full configuration for a program"""
    metadata: ProgramMetadata
    system_prompt: str = ""
    allowed_tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    output_format: Dict[str, Any] = field(default_factory=dict)
    
    def mutate(self, new_name: str) -> "ProgramConfig":
        """
        Create a mutated version of this config
        
        Args:
            new_name: Name for the new program
            
        Returns:
            New ProgramConfig with incremented generation
        """
        new_metadata = ProgramMetadata(
            name=new_name,
            parent=self.metadata.name,
            generation=self.metadata.generation + 1,
            tags=self.metadata.tags.copy(),
            metadata=self.metadata.metadata.copy()
        )
        
        return ProgramConfig(
            metadata=new_metadata,
            system_prompt=self.system_prompt,
            allowed_tools=self.allowed_tools.copy(),
            skills=self.skills.copy(),
            output_format=self.output_format.copy()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "metadata": self.metadata.to_dict(),
            "system_prompt": self.system_prompt,
            "allowed_tools": self.allowed_tools,
            "skills": self.skills,
            "output_format": self.output_format
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgramConfig":
        """Create from dictionary"""
        return cls(
            metadata=ProgramMetadata.from_dict(data["metadata"]),
            system_prompt=data.get("system_prompt", ""),
            allowed_tools=data.get("allowed_tools", []),
            skills=data.get("skills", []),
            output_format=data.get("output_format", {})
        )
