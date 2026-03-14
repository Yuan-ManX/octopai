"""
Skill Factory - EXO's Innovative Skill Creation System

This module provides EXO's proprietary skill creation system that
transforms diverse resources into structured, AI-ready skills through
intelligent analysis and generation.
"""

import os
import hashlib
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

from exo.utils.config import Config
from exo.utils.helpers import read_file, write_file
from exo.core.converter import URLConverter
from exo.core.resource_parser import ResourceParser
import requests
import re
import uuid


class SkillType(Enum):
    """Types of skills that can be created"""
    GENERAL = "general"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"
    CREATIVE = "creative"
    RESEARCH = "research"
    CODING = "coding"


@dataclass
class SkillVersion:
    """Represents a version of a skill with complete history"""
    version: int
    content: str
    created_at: str
    author: Optional[str] = None
    change_description: Optional[str] = None
    content_hash: str = ""
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = self._compute_hash(self.content)
    
    def _compute_hash(self, content: str) -> str:
        """Compute secure hash of skill content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillVersion':
        return cls(**data)


@dataclass
class SkillMetadata:
    """Comprehensive metadata for a skill"""
    skill_id: str
    name: str
    description: str
    skill_type: SkillType = SkillType.GENERAL
    tags: List[str] = field(default_factory=list)
    category: Optional[str] = None
    author: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    license: str = "MIT"
    requirements: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['skill_type'] = self.skill_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillMetadata':
        if 'skill_type' in data and isinstance(data['skill_type'], str):
            data['skill_type'] = SkillType(data['skill_type'])
        return cls(**data)


@dataclass
class SkillDefinition:
    """Complete skill definition with content and metadata"""
    metadata: SkillMetadata
    versions: List[SkillVersion] = field(default_factory=list)
    
    @property
    def latest_version(self) -> Optional[SkillVersion]:
        """Get the most recent version"""
        if not self.versions:
            return None
        return max(self.versions, key=lambda v: v.version)
    
    def add_version(
        self,
        content: str,
        author: Optional[str] = None,
        change_description: Optional[str] = None
    ) -> SkillVersion:
        """Add a new version of the skill"""
        new_version_num = max([v.version for v in self.versions], default=0) + 1
        version = SkillVersion(
            version=new_version_num,
            content=content,
            created_at=datetime.now().isoformat(),
            author=author,
            change_description=change_description
        )
        self.versions.append(version)
        self.metadata.updated_at = datetime.now().isoformat()
        return version
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metadata': self.metadata.to_dict(),
            'versions': [v.to_dict() for v in self.versions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillDefinition':
        return cls(
            metadata=SkillMetadata.from_dict(data['metadata']),
            versions=[SkillVersion.from_dict(v) for v in data.get('versions', [])]
        )


class SkillFactory:
    """
    EXO's Skill Factory - Intelligent Skill Creation System
    
    Transforms ANYTHING into structured, high-quality skills through EXO's 
    proprietary analysis and generation pipeline. Everything Can Be a Skill!
    
    Supported input types:
    - Web URLs and websites
    - Files (PDF, DOC, XLS, images, videos, code, etc.)
    - Raw text and prompts
    - API endpoints and data streams
    - Code repositories and snippets
    - And more!
    """
    
    def __init__(self):
        self.config = Config()
    
    def create_from_url(
        self,
        url: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        additional_context: Optional[str] = None
    ) -> SkillDefinition:
        """
        Create a skill from a web URL
        
        Args:
            url: The web URL to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            additional_context: Optional additional context for skill creation
            
        Returns:
            Complete SkillDefinition ready for use
        """
        converter = URLConverter()
        content = converter.convert(url)
        
        return self._create_skill(
            source_content=content,
            source_type="url",
            source_reference=url,
            name=name,
            description=description,
            tags=tags or ["web-resource"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=additional_context
        )
    
    def create_from_files(
        self,
        file_paths: List[str],
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        additional_context: Optional[str] = None
    ) -> SkillDefinition:
        """
        Create a skill from one or more files
        
        Args:
            file_paths: List of file paths to process
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            additional_context: Optional additional context for skill creation
            
        Returns:
            Complete SkillDefinition ready for use
        """
        parser = ResourceParser()
        combined_content = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    resource = parser.parse(file_path)
                    combined_content.append(f"## File: {os.path.basename(file_path)}\n\n{resource.to_skill_resource()}")
                except Exception as e:
                    combined_content.append(f"## File: {os.path.basename(file_path)}\n\nError processing: {str(e)}")
        
        content = "\n\n---\n\n".join(combined_content)
        
        return self._create_skill(
            source_content=content,
            source_type="files",
            source_reference=",".join([os.path.basename(f) for f in file_paths]),
            name=name,
            description=description,
            tags=tags or ["file-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=additional_context
        )
    
    def create_from_prompt(
        self,
        prompt: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        resources: Optional[List[str]] = None
    ) -> SkillDefinition:
        """
        Create a skill from a descriptive prompt
        
        Args:
            prompt: Description of what the skill should do
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            resources: Optional list of resource files to include
            
        Returns:
            Complete SkillDefinition ready for use
        """
        enhanced_prompt = prompt
        
        if resources:
            parser = ResourceParser()
            resource_contents = []
            
            for res_path in resources:
                if os.path.exists(res_path):
                    try:
                        resource = parser.parse(res_path)
                        resource_contents.append(f"\n--- Resource: {os.path.basename(res_path)} ---\n{resource.to_skill_resource()}")
                    except Exception as e:
                        resource_contents.append(f"\n--- Resource: {os.path.basename(res_path)} ---\nError parsing: {str(e)}")
            
            if resource_contents:
                enhanced_prompt = f"{prompt}\n\nAdditional Resources:\n{' '.join(resource_contents)}"
        
        return self._create_skill(
            source_content=enhanced_prompt,
            source_type="prompt",
            source_reference="direct-prompt",
            name=name,
            description=description,
            tags=tags or ["prompt-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=None
        )
    
    def _create_skill(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        tags: List[str],
        category: Optional[str],
        author: Optional[str],
        skill_type: SkillType,
        additional_context: Optional[str]
    ) -> SkillDefinition:
        """Internal method to create a skill from prepared content"""
        
        skill_id = self._generate_skill_id(name)
        
        metadata = SkillMetadata(
            skill_id=skill_id,
            name=name,
            description=description,
            skill_type=skill_type,
            tags=tags,
            category=category,
            author=author
        )
        
        skill_content = self._generate_skill_content(
            source_content=source_content,
            source_type=source_type,
            source_reference=source_reference,
            name=name,
            description=description,
            skill_type=skill_type,
            additional_context=additional_context
        )
        
        definition = SkillDefinition(metadata=metadata)
        definition.add_version(
            content=skill_content,
            author=author,
            change_description=f"Initial version created from {source_type}"
        )
        
        return definition
    
    def _generate_skill_id(self, name: str) -> str:
        """Generate a unique skill ID"""
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        short_id = str(uuid.uuid4())[:8]
        return f"{slug}-{short_id}"
    
    def _generate_skill_content(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        skill_type: SkillType,
        additional_context: Optional[str]
    ) -> str:
        """Generate structured skill content using EXO's intelligent generation"""
        
        prompt = self._build_skill_generation_prompt(
            source_content=source_content,
            source_type=source_type,
            source_reference=source_reference,
            name=name,
            description=description,
            skill_type=skill_type,
            additional_context=additional_context
        )
        
        headers = {
            'Authorization': f'Bearer {self.config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "openai/gpt-5.4",
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at creating comprehensive, well-structured skills for AI Agents.
Create skills that are:
1. Clear and actionable
2. Well-organized with logical sections
3. Complete with examples and best practices
4. Easy for AI Agents to understand and use
5. Include troubleshooting guidance

Format as Markdown, ready to be used as SKILL.md content."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=90
            )
            response.raise_for_status()
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', source_content)
        except Exception as e:
            print(f"Skill generation fallback: {e}")
            return self._build_fallback_skill_content(
                source_content, name, description
            )
    
    def _build_skill_generation_prompt(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        skill_type: SkillType,
        additional_context: Optional[str]
    ) -> str:
        """Build the prompt for skill generation"""
        
        prompt_parts = [
            f"# Skill Creation Request",
            f"",
            f"## Skill Information",
            f"- **Name**: {name}",
            f"- **Description**: {description}",
            f"- **Type**: {skill_type.value}",
            f"- **Source**: {source_type} ({source_reference})",
            f"",
            f"## Source Content",
            f"",
            source_content
        ]
        
        if additional_context:
            prompt_parts.extend([
                f"",
                f"## Additional Context",
                f"",
                additional_context
            ])
        
        prompt_parts.extend([
            f"",
            f"Please create a comprehensive, well-structured skill in Markdown format.",
            f"Include:",
            f"1. Overview and Purpose",
            f"2. Usage Instructions",
            f"3. Practical Examples",
            f"4. Best Practices",
            f"5. Troubleshooting Guide",
            f"6. Any relevant configuration or setup information"
        ])
        
        return "\n".join(prompt_parts)
    
    def create_from_text(
        self,
        text: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL
    ) -> SkillDefinition:
        """
        Create a skill from raw text content
        
        Args:
            text: Raw text content to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self._create_skill(
            source_content=text,
            source_type="text",
            source_reference="raw-text",
            name=name,
            description=description,
            tags=tags or ["text-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=None
        )
    
    def create_from_code(
        self,
        code: str,
        language: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None
    ) -> SkillDefinition:
        """
        Create a skill from code
        
        Args:
            code: Source code to transform
            language: Programming language
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            
        Returns:
            Complete SkillDefinition ready for use
        """
        enhanced_content = f"## Code ({language})\n\n```{language}\n{code}\n```"
        return self._create_skill(
            source_content=enhanced_content,
            source_type="code",
            source_reference=f"{language}-code",
            name=name,
            description=description,
            tags=tags or ["code", language.lower()],
            category=category,
            author=author,
            skill_type=SkillType.CODING,
            additional_context=f"Programming language: {language}"
        )
    
    def create_from_api(
        self,
        api_endpoint: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None
    ) -> SkillDefinition:
        """
        Create a skill from an API endpoint
        
        Args:
            api_endpoint: API endpoint URL
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            
        Returns:
            Complete SkillDefinition ready for use
        """
        api_content = f"## API Endpoint\n\n- **Endpoint**: {api_endpoint}\n- **Type**: REST API"
        return self._create_skill(
            source_content=api_content,
            source_type="api",
            source_reference=api_endpoint,
            name=name,
            description=description,
            tags=tags or ["api", "integration"],
            category=category,
            author=author,
            skill_type=SkillType.AUTOMATION,
            additional_context=f"API endpoint: {api_endpoint}"
        )
    
    def create_anything(
        self,
        source: Any,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL
    ) -> SkillDefinition:
        """
        Create a skill from ANYTHING - the core of 'Everything Can Be a Skill'
        
        Args:
            source: ANY source to transform into a skill
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            
        Returns:
            Complete SkillDefinition ready for use
        """
        source_type = type(source).__name__
        source_content = self._normalize_anything_to_content(source)
        
        return self._create_skill(
            source_content=source_content,
            source_type=source_type,
            source_reference=f"auto-detected-{source_type}",
            name=name,
            description=description,
            tags=tags or ["universal", source_type.lower()],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=f"Source type: {source_type}"
        )
    
    def _normalize_anything_to_content(self, source: Any) -> str:
        """Normalize ANY source to text content"""
        if isinstance(source, str):
            return source
        elif isinstance(source, (list, tuple)):
            return "\n".join([f"- {item}" for item in source])
        elif isinstance(source, dict):
            return "\n".join([f"**{k}**: {v}" for k, v in source.items()])
        else:
            return str(source)
    
    def _build_fallback_skill_content(
        self,
        source_content: str,
        name: str,
        description: str
    ) -> str:
        """Build fallback skill content if generation fails"""
        
        return f"""# {name}

{description}

## Overview

This skill was created from source content and provides structured knowledge
for AI Agents. Created with EXO's 'Everything Can Be a Skill' philosophy.

## Source Content

{source_content}

## Usage

Use this skill to access and apply the knowledge contained within.

---

*Created by EXO Skill Factory - Everything Can Be a Skill!*
"""
