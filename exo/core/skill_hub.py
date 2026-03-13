"""
SkillHub - Skill Storage and Management System

EXO's centralized skill management system provides
centralized skill management, version control,
retrieval, and merging capabilities.
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class SkillVersion:
    """
    Represents a version of a skill with metadata
    """
    
    def __init__(
        self,
        version: int,
        content: str,
        created_at: Optional[str] = None,
        author: Optional[str] = None,
        change_description: Optional[str] = None
    ):
        self.version = version
        self.content = content
        self.created_at = created_at or datetime.now().isoformat()
        self.author = author
        self.change_description = change_description
        self.content_hash = self._compute_hash(content)
    
    def _compute_hash(self, content: str) -> str:
        """Compute hash of skill content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "version": self.version,
            "content": self.content,
            "created_at": self.created_at,
            "author": self.author,
            "change_description": self.change_description,
            "content_hash": self.content_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillVersion':
        """Create from dictionary"""
        return cls(
            version=data["version"],
            content=data["content"],
            created_at=data.get("created_at"),
            author=data.get("author"),
            change_description=data.get("change_description")
        )


class SkillMetadata:
    """
    Metadata for a skill
    """
    
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        usage_count: int = 0,
        success_rate: float = 0.0
    ):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.tags = tags or []
        self.category = category
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.usage_count = usage_count
        self.success_rate = success_rate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillMetadata':
        """Create from dictionary"""
        return cls(
            skill_id=data["skill_id"],
            name=data["name"],
            description=data["description"],
            tags=data.get("tags", []),
            category=data.get("category"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0),
            success_rate=data.get("success_rate", 0.0)
        )


class Skill:
    """
    Represents a complete skill with metadata and versions
    """
    
    def __init__(self, metadata: SkillMetadata, versions: Optional[List[SkillVersion]] = None):
        self.metadata = metadata
        self.versions = versions or []
    
    @property
    def latest_version(self) -> Optional[SkillVersion]:
        """Get the latest version"""
        if self.versions:
            return max(self.versions, key=lambda v: v.version)
        return None
    
    def add_version(
        self,
        content: str,
        author: Optional[str] = None,
        change_description: Optional[str] = None
    ) -> SkillVersion:
        """Add a new version"""
        new_version = max([v.version for v in self.versions], default=0) + 1
        version = SkillVersion(
            version=new_version,
            content=content,
            author=author,
            change_description=change_description
        )
        self.versions.append(version)
        self.metadata.updated_at = datetime.now().isoformat()
        return version
    
    def get_version(self, version: int) -> Optional[SkillVersion]:
        """Get a specific version"""
        for v in self.versions:
            if v.version == version:
                return v
        return None
    
    def record_usage(self, success: bool = True):
        """Record skill usage"""
        self.metadata.usage_count += 1
        if success:
            total = self.metadata.usage_count
            old_rate = self.metadata.success_rate
            self.metadata.success_rate = (old_rate * (total - 1) + 1.0) / total
        self.metadata.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "metadata": self.metadata.to_dict(),
            "versions": [v.to_dict() for v in self.versions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        """Create from dictionary"""
        metadata = SkillMetadata.from_dict(data["metadata"])
        versions = [SkillVersion.from_dict(v) for v in data.get("versions", [])]
        return cls(metadata, versions)


class SkillHub:
    """
    Centralized skill storage and management system
    
    Features:
    - Persistent skill storage
    - Version control for skills
    - Skill retrieval and search
    - Skill merging capabilities
    - Usage tracking and analytics
    """
    
    def __init__(self, storage_dir: str = "./SkillHub"):
        self.storage_dir = Path(storage_dir)
        self.skills_dir = self.storage_dir / "skills"
        self.index_file = self.storage_dir / "index.json"
        
        self._initialize_storage()
        self._skills: Dict[str, Skill] = self._load_index()
    
    def _initialize_storage(self):
        """Initialize storage directories"""
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_index(self) -> Dict[str, Skill]:
        """Load skill index from disk"""
        if not self.index_file.exists():
            return {}
        
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        skills = {}
        for skill_id, skill_path in index_data.items():
            skill_file = self.storage_dir / skill_path
            if skill_file.exists():
                with open(skill_file, 'r', encoding='utf-8') as f:
                    skill_data = json.load(f)
                    skills[skill_id] = Skill.from_dict(skill_data)
        
        return skills
    
    def _save_index(self, index: Dict[str, str]):
        """Save skill index to disk"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _save_skill(self, skill: Skill):
        """Save a single skill to disk"""
        skill_file = self.skills_dir / f"{skill.metadata.skill_id}.json"
        with open(skill_file, 'w', encoding='utf-8') as f:
            json.dump(skill.to_dict(), f, indent=2, ensure_ascii=False)
        
        index = {s.metadata.skill_id: f"skills/{s.metadata.skill_id}.json" 
                 for s in self._skills.values()}
        self._save_index(index)
    
    def _generate_skill_id(self, name: str) -> str:
        """Generate a unique skill ID"""
        base_id = name.lower().replace(' ', '-').replace('_', '-')
        base_id = ''.join(c for c in base_id if c.isalnum() or c == '-')
        
        counter = 1
        skill_id = base_id
        while skill_id in self._skills:
            skill_id = f"{base_id}-{counter}"
            counter += 1
        
        return skill_id
    
    def create_skill(
        self,
        name: str,
        description: str,
        content: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None
    ) -> Skill:
        """
        Create a new skill
        
        Args:
            name: Skill name
            description: Skill description
            content: Skill content (SKILL.md format)
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            
        Returns:
            Created Skill object
        """
        skill_id = self._generate_skill_id(name)
        
        metadata = SkillMetadata(
            skill_id=skill_id,
            name=name,
            description=description,
            tags=tags or [],
            category=category
        )
        
        skill = Skill(metadata)
        skill.add_version(content, author=author, change_description="Initial version")
        
        self._skills[skill_id] = skill
        self._save_skill(skill)
        
        return skill
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID"""
        return self._skills.get(skill_id)
    
    def update_skill(
        self,
        skill_id: str,
        content: str,
        author: Optional[str] = None,
        change_description: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Update an existing skill
        
        Args:
            skill_id: Skill ID to update
            content: New skill content
            author: Optional author name
            change_description: Description of changes
            
        Returns:
            Updated Skill object or None if not found
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        skill.add_version(content, author=author, change_description=change_description)
        self._save_skill(skill)
        
        return skill
    
    def delete_skill(self, skill_id: str) -> bool:
        """Delete a skill"""
        if skill_id not in self._skills:
            return False
        
        skill_file = self.skills_dir / f"{skill_id}.json"
        if skill_file.exists():
            skill_file.unlink()
        
        del self._skills[skill_id]
        
        index = {s.metadata.skill_id: f"skills/{s.metadata.skill_id}.json" 
                 for s in self._skills.values()}
        self._save_index(index)
        
        return True
    
    def search_skills(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Skill]:
        """
        Search for skills based on query
        
        Args:
            query: Search query text
            tags: Optional tag filter
            category: Optional category filter
            limit: Maximum number of results
            
        Returns:
            List of matching skills
        """
        results = []
        query_lower = query.lower()
        
        for skill in self._skills.values():
            score = 0.0
            
            if tags:
                tag_match = len(set(tags) & set(skill.metadata.tags))
                if tag_match > 0:
                    score += tag_match * 2.0
            
            if category and skill.metadata.category == category:
                score += 3.0
            
            if query_lower in skill.metadata.name.lower():
                score += 5.0
            
            if query_lower in skill.metadata.description.lower():
                score += 3.0
            
            if any(query_lower in tag.lower() for tag in skill.metadata.tags):
                score += 2.0
            
            latest = skill.latest_version
            if latest and query_lower in latest.content.lower():
                score += 1.0
            
            if score > 0:
                results.append((score, skill))
        
        results.sort(key=lambda x: (x[0], x[1].metadata.usage_count, x[1].metadata.success_rate), reverse=True)
        return [skill for _, skill in results[:limit]]
    
    def list_skills(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Skill]:
        """
        List all skills with optional filters
        
        Args:
            category: Optional category filter
            tags: Optional tag filter
            limit: Maximum number of results
            
        Returns:
            List of skills
        """
        skills = list(self._skills.values())
        
        if category:
            skills = [s for s in skills if s.metadata.category == category]
        
        if tags:
            skills = [s for s in skills if any(tag in s.metadata.tags for tag in tags)]
        
        skills.sort(key=lambda x: (x.metadata.usage_count, x.metadata.success_rate), reverse=True)
        return skills[:limit]
    
    def record_skill_usage(self, skill_id: str, success: bool = True) -> bool:
        """Record skill usage"""
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        
        skill.record_usage(success)
        self._save_skill(skill)
        return True
    
    def merge_skills(
        self,
        skill_ids: List[str],
        new_name: str,
        new_description: str,
        author: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Merge multiple skills into a new skill
        
        Args:
            skill_ids: List of skill IDs to merge
            new_name: Name for the merged skill
            new_description: Description for the merged skill
            author: Optional author name
            
        Returns:
            Merged Skill object or None
        """
        skills = [self._skills.get(sid) for sid in skill_ids if self._skills.get(sid)]
        if len(skills) < 2:
            return None
        
        merged_content = f"# {new_name}\n\n"
        merged_content += f"{new_description}\n\n"
        merged_content += "## Merged from:\n"
        
        all_tags = set()
        for skill in skills:
            merged_content += f"- {skill.metadata.name} (v{skill.latest_version.version if skill.latest_version else 0})\n"
            all_tags.update(skill.metadata.tags)
            if skill.latest_version:
                merged_content += f"\n### {skill.metadata.name} Content:\n"
                merged_content += skill.latest_version.content + "\n"
        
        return self.create_skill(
            name=new_name,
            description=new_description,
            content=merged_content,
            tags=list(all_tags),
            category=skills[0].metadata.category,
            author=author
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get SkillHub statistics"""
        total_skills = len(self._skills)
        total_versions = sum(len(s.versions) for s in self._skills.values())
        total_usage = sum(s.metadata.usage_count for s in self._skills.values())
        avg_success_rate = (
            sum(s.metadata.success_rate for s in self._skills.values()) / total_skills
            if total_skills > 0 else 0.0
        )
        
        categories = {}
        for skill in self._skills.values():
            cat = skill.metadata.category or "Uncategorized"
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_skills": total_skills,
            "total_versions": total_versions,
            "total_usage": total_usage,
            "average_success_rate": avg_success_rate,
            "categories": categories
        }
