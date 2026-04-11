"""
Octopai Skill Specification - Advanced Skill Format Standard

This module defines Octopai's proprietary skill specification format that
enables structured, reusable, and evolvable skills with rich metadata,
dynamic loading capabilities, and comprehensive documentation.

Octopai Skill Format Features:
- YAML frontmatter for metadata
- Markdown content for instructions
- Support for scripts, resources, and dependencies
- Versioning and evolution tracking
- Compatibility with folder-based skills
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime
import hashlib


class SkillTriggerType(Enum):
    """Types of triggers that activate a skill"""
    EXPLICIT = "explicit"
    KEYWORD = "keyword"
    CONTEXT = "context"
    AUTO = "auto"


class SkillCategory(Enum):
    """Standard skill categories"""
    CREATIVE = "creative"
    DEVELOPMENT = "development"
    DOCUMENT = "document"
    ENTERPRISE = "enterprise"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"
    RESEARCH = "research"
    DESIGN = "design"
    COMMUNICATION = "communication"
    GENERAL = "general"


@dataclass
class SkillDependency:
    """Dependency for a skill"""
    name: str
    version: Optional[str] = None
    optional: bool = False
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "optional": self.optional,
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillDependency':
        return cls(**data)


@dataclass
class SkillResource:
    """Resource file included with a skill"""
    path: str
    type: str
    description: Optional[str] = None
    required: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "type": self.type,
            "description": self.description,
            "required": self.required
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillResource':
        return cls(**data)


@dataclass
class SkillScript:
    """Script that can be executed by a skill"""
    path: str
    language: str
    entrypoint: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "language": self.language,
            "entrypoint": self.entrypoint,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillScript':
        return cls(**data)


@dataclass
class SkillExample:
    """Example usage of a skill"""
    title: str
    description: str
    input: Optional[str] = None
    output: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "input": self.input,
            "output": self.output
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillExample':
        return cls(**data)


@dataclass
class SkillGuideline:
    """Guideline for using a skill"""
    guideline: str
    priority: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "guideline": self.guideline,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillGuideline':
        return cls(**data)


@dataclass
class SkillTrigger:
    """Trigger configuration for a skill"""
    type: SkillTriggerType
    keywords: List[str] = field(default_factory=list)
    context_patterns: List[str] = field(default_factory=list)
    auto_activate: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "keywords": self.keywords,
            "context_patterns": self.context_patterns,
            "auto_activate": self.auto_activate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillTrigger':
        data = data.copy()
        if "type" in data and isinstance(data["type"], str):
            data["type"] = SkillTriggerType(data["type"])
        return cls(**data)


@dataclass
class OctopaiSkillSpec:
    """
    Octopai Skill Specification - Complete skill definition
    
    This is the core specification for Octopai skills, providing
    comprehensive metadata, content, resources, and configuration
    for powerful, reusable, and evolvable skills.
    """
    name: str
    description: str
    version: str = "1.0.0"
    author: Optional[str] = None
    license: str = "MIT"
    
    category: SkillCategory = SkillCategory.GENERAL
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    
    triggers: List[SkillTrigger] = field(default_factory=list)
    
    dependencies: List[SkillDependency] = field(default_factory=list)
    resources: List[SkillResource] = field(default_factory=list)
    scripts: List[SkillScript] = field(default_factory=list)
    
    examples: List[SkillExample] = field(default_factory=list)
    guidelines: List[SkillGuideline] = field(default_factory=list)
    
    content: str = ""
    content_hash: str = ""
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = self._compute_content_hash()
    
    def _compute_content_hash(self) -> str:
        """Compute hash of skill content"""
        content_to_hash = f"{self.name}:{self.description}:{self.version}:{self.content}"
        return hashlib.sha256(content_to_hash.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "license": self.license,
            "category": self.category.value,
            "tags": self.tags,
            "keywords": self.keywords,
            "triggers": [t.to_dict() for t in self.triggers],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "resources": [r.to_dict() for r in self.resources],
            "scripts": [s.to_dict() for s in self.scripts],
            "examples": [e.to_dict() for e in self.examples],
            "guidelines": [g.to_dict() for g in self.guidelines],
            "content": self.content,
            "content_hash": self.content_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "custom_fields": self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OctopaiSkillSpec':
        """Create from dictionary representation"""
        data = data.copy()
        
        if "category" in data and isinstance(data["category"], str):
            data["category"] = SkillCategory(data["category"])
        
        if "triggers" in data:
            data["triggers"] = [SkillTrigger.from_dict(t) for t in data["triggers"]]
        
        if "dependencies" in data:
            data["dependencies"] = [SkillDependency.from_dict(d) for d in data["dependencies"]]
        
        if "resources" in data:
            data["resources"] = [SkillResource.from_dict(r) for r in data["resources"]]
        
        if "scripts" in data:
            data["scripts"] = [SkillScript.from_dict(s) for s in data["scripts"]]
        
        if "examples" in data:
            data["examples"] = [SkillExample.from_dict(e) for e in data["examples"]]
        
        if "guidelines" in data:
            data["guidelines"] = [SkillGuideline.from_dict(g) for g in data["guidelines"]]
        
        return cls(**data)
    
    def to_skill_md(self) -> str:
        """
        Export to Octopai Skill Markdown format (OCTOPAI.md)
        
        This format uses YAML frontmatter followed by Markdown content,
        similar to standard Markdown with frontmatter but enhanced for skills.
        """
        frontmatter = {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "license": self.license,
            "category": self.category.value,
            "tags": self.tags,
            "keywords": self.keywords,
        }
        
        if self.dependencies:
            frontmatter["dependencies"] = [d.to_dict() for d in self.dependencies]
        
        if self.resources:
            frontmatter["resources"] = [r.to_dict() for r in self.resources]
        
        if self.scripts:
            frontmatter["scripts"] = [s.to_dict() for s in self.scripts]
        
        if self.triggers:
            frontmatter["triggers"] = [t.to_dict() for t in self.triggers]
        
        yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        
        parts = [
            "---",
            yaml_content.rstrip(),
            "---",
            "",
            self.content
        ]
        
        if self.examples:
            parts.append("")
            parts.append("## Examples")
            for example in self.examples:
                parts.append(f"### {example.title}")
                parts.append(f"{example.description}")
                if example.input:
                    parts.append(f"**Input:**\n```\n{example.input}\n```")
                if example.output:
                    parts.append(f"**Output:**\n```\n{example.output}\n```")
                parts.append("")
        
        if self.guidelines:
            parts.append("")
            parts.append("## Guidelines")
            for guideline in self.guidelines:
                parts.append(f"- {guideline.guideline}")
        
        return "\n".join(parts)
    
    @classmethod
    def from_skill_md(cls, content: str) -> 'OctopaiSkillSpec':
        """
        Parse from Octopai Skill Markdown format (OCTOPAI.md)
        """
        lines = content.split('\n')
        
        if not lines or lines[0] != '---':
            raise ValueError("Invalid OCTOPAI.md format: missing opening ---")
        
        frontmatter_lines = []
        content_lines = []
        in_frontmatter = True
        frontmatter_ended = False
        
        for line in lines[1:]:
            if in_frontmatter:
                if line == '---':
                    in_frontmatter = False
                    frontmatter_ended = True
                else:
                    frontmatter_lines.append(line)
            else:
                content_lines.append(line)
        
        if not frontmatter_ended:
            raise ValueError("Invalid OCTOPAI.md format: missing closing ---")
        
        frontmatter = yaml.safe_load('\n'.join(frontmatter_lines)) or {}
        
        main_content = '\n'.join(content_lines).lstrip()
        
        examples = []
        guidelines = []
        
        if '## Examples' in main_content:
            parts = main_content.split('## Examples')
            main_content = parts[0]
            examples_section = parts[1] if len(parts) > 1 else ''
            
            if '## Guidelines' in examples_section:
                examples_section, guidelines_section = examples_section.split('## Guidelines')
                guidelines = cls._parse_guidelines(guidelines_section)
            
            examples = cls._parse_examples(examples_section)
        elif '## Guidelines' in main_content:
            parts = main_content.split('## Guidelines')
            main_content = parts[0]
            guidelines = cls._parse_guidelines(parts[1])
        
        frontmatter['content'] = main_content.strip()
        
        if examples:
            frontmatter['examples'] = examples
        
        if guidelines:
            frontmatter['guidelines'] = guidelines
        
        return cls.from_dict(frontmatter)
    
    @staticmethod
    def _parse_examples(section: str) -> List[SkillExample]:
        """Parse examples from markdown section"""
        examples = []
        current_example = None
        buffer = []
        
        for line in section.split('\n'):
            if line.startswith('### '):
                if current_example:
                    current_example['description'] = '\n'.join(buffer).strip()
                    examples.append(SkillExample.from_dict(current_example))
                    buffer = []
                
                current_example = {
                    'title': line[4:].strip(),
                    'description': '',
                    'input': None,
                    'output': None
                }
            elif current_example:
                buffer.append(line)
        
        if current_example:
            current_example['description'] = '\n'.join(buffer).strip()
            examples.append(SkillExample.from_dict(current_example))
        
        return examples
    
    @staticmethod
    def _parse_guidelines(section: str) -> List[SkillGuideline]:
        """Parse guidelines from markdown section"""
        guidelines = []
        
        for line in section.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                guideline = line[2:].strip()
                if guideline:
                    guidelines.append(SkillGuideline(guideline=guideline))
        
        return guidelines


class SkillFolder:
    """
    Folder-based skill container
    
    Manages skills stored in folders with:
    - OCTOPAI.md (main skill definition)
    - resources/ (resource files)
    - scripts/ (executable scripts)
    - tests/ (skill tests)
    """
    
    def __init__(self, folder_path: Union[str, Path]):
        self.folder_path = Path(folder_path)
        self._validate_folder()
    
    def _validate_folder(self):
        """Validate folder structure"""
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Skill folder not found: {self.folder_path}")
        
        skill_md_path = self.folder_path / "OCTOPAI.md"
        if not skill_md_path.exists():
            raise FileNotFoundError(f"OCTOPAI.md not found in: {self.folder_path}")
    
    def load_skill(self) -> OctopaiSkillSpec:
        """Load skill from folder"""
        skill_md_path = self.folder_path / "OCTOPAI.md"
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        skill = OctopaiSkillSpec.from_skill_md(content)
        
        resources_dir = self.folder_path / "resources"
        if resources_dir.exists():
            for resource_file in resources_dir.iterdir():
                if resource_file.is_file():
                    rel_path = str(resource_file.relative_to(self.folder_path))
                    resource = SkillResource(
                        path=rel_path,
                        type=self._guess_file_type(resource_file),
                        required=True
                    )
                    skill.resources.append(resource)
        
        scripts_dir = self.folder_path / "scripts"
        if scripts_dir.exists():
            for script_file in scripts_dir.iterdir():
                if script_file.is_file():
                    rel_path = str(script_file.relative_to(self.folder_path))
                    script = SkillScript(
                        path=rel_path,
                        language=self._guess_script_language(script_file)
                    )
                    skill.scripts.append(script)
        
        return skill
    
    def save_skill(self, skill: OctopaiSkillSpec):
        """Save skill to folder"""
        self.folder_path.mkdir(parents=True, exist_ok=True)
        
        skill_md_path = self.folder_path / "OCTOPAI.md"
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill.to_skill_md())
        
        for resource in skill.resources:
            resource_path = self.folder_path / resource.path
            resource_path.parent.mkdir(parents=True, exist_ok=True)
        
        for script in skill.scripts:
            script_path = self.folder_path / script.path
            script_path.parent.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _guess_file_type(path: Path) -> str:
        """Guess file type from extension"""
        ext = path.suffix.lower()
        type_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.csv': 'csv',
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.xlsx': 'xlsx',
            '.pptx': 'pptx',
            '.png': 'image',
            '.jpg': 'image',
            '.jpeg': 'image',
        }
        return type_map.get(ext, 'unknown')
    
    @staticmethod
    def _guess_script_language(path: Path) -> str:
        """Guess script language from extension"""
        ext = path.suffix.lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.sh': 'bash',
            '.bat': 'batch',
            '.ps1': 'powershell',
        }
        return lang_map.get(ext, 'unknown')


def create_skill_folder(
    skill: OctopaiSkillSpec,
    base_path: Union[str, Path],
    create_resources: bool = True,
    create_scripts: bool = True
) -> SkillFolder:
    """
    Create a new skill folder from a skill specification
    
    Args:
        skill: The skill specification
        base_path: Base directory to create the skill folder in
        create_resources: Whether to create resources directory
        create_scripts: Whether to create scripts directory
    
    Returns:
        SkillFolder instance for the created folder
    """
    safe_name = skill.name.lower().replace(' ', '-').replace('/', '-')
    folder_path = Path(base_path) / safe_name
    
    folder = SkillFolder(folder_path) if folder_path.exists() else None
    
    if not folder:
        folder_path.mkdir(parents=True, exist_ok=True)
        
        if create_resources:
            (folder_path / "resources").mkdir(exist_ok=True)
        
        if create_scripts:
            (folder_path / "scripts").mkdir(exist_ok=True)
        
        (folder_path / "tests").mkdir(exist_ok=True)
        
        folder = SkillFolder(folder_path)
    
    folder.save_skill(skill)
    
    return folder


__all__ = [
    'SkillTriggerType',
    'SkillCategory',
    'SkillDependency',
    'SkillResource',
    'SkillScript',
    'SkillExample',
    'SkillGuideline',
    'SkillTrigger',
    'OctopaiSkillSpec',
    'SkillFolder',
    'create_skill_folder'
]
