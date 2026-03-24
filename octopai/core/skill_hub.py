"""
SkillHub - Skill Storage and Management System

Octopai's centralized skill management system provides
centralized skill management, version control,
retrieval, and merging capabilities. Features include
intelligent indexing, semantic search, collections,
context management, and publishing workflows.
"""

import os
import json
import hashlib
import re
import difflib
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path


class SkillStatus(Enum):
    """Status of a skill in the hub"""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class SkillVisibility(Enum):
    """Visibility level of a skill"""
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


@dataclass
class SkillDependency:
    """Dependency relationship between skills"""
    skill_id: str
    dependency_type: str = "requires"
    version_constraint: Optional[str] = None
    optional: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "dependency_type": self.dependency_type,
            "version_constraint": self.version_constraint,
            "optional": self.optional
        }


@dataclass
class SkillRating:
    """Rating and feedback for a skill"""
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


@dataclass
class SkillCollection:
    """Collection of related skills"""
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


@dataclass
class ContextSlot:
    """Slot for context composition"""
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


@dataclass
class ContextComposition:
    """Composed context of multiple skills"""
    composition_id: str
    name: str
    description: str
    slots: Dict[str, ContextSlot] = field(default_factory=dict)
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


@dataclass
class VersionDiff:
    """Difference between two skill versions"""
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


@dataclass
class SearchIndex:
    """Search index entry for efficient retrieval"""
    skill_id: str
    name_tokens: List[str] = field(default_factory=list)
    description_tokens: List[str] = field(default_factory=list)
    tag_tokens: List[str] = field(default_factory=list)
    content_tokens: List[str] = field(default_factory=list)
    category_tokens: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name_tokens": self.name_tokens,
            "description_tokens": self.description_tokens,
            "tag_tokens": self.tag_tokens,
            "content_tokens": self.content_tokens,
            "category_tokens": self.category_tokens
        }


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
    Comprehensive metadata for a skill
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
        success_rate: float = 0.0,
        status: SkillStatus = SkillStatus.DRAFT,
        visibility: SkillVisibility = SkillVisibility.PRIVATE,
        author: Optional[str] = None,
        version: str = "1.0.0",
        license: str = "MIT",
        keywords: Optional[List[str]] = None,
        dependencies: Optional[List[SkillDependency]] = None,
        related_skills: Optional[List[str]] = None,
        average_rating: float = 0.0,
        rating_count: int = 0,
        skill_type: Optional[str] = None,
        compatibility: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
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
        self.status = status
        self.visibility = visibility
        self.author = author
        self.version = version
        self.license = license
        self.keywords = keywords or []
        self.dependencies = dependencies or []
        self.related_skills = related_skills or []
        self.average_rating = average_rating
        self.rating_count = rating_count
        self.skill_type = skill_type
        self.compatibility = compatibility or []
        self.custom_fields = custom_fields or {}
    
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
            "success_rate": self.success_rate,
            "status": self.status.value,
            "visibility": self.visibility.value,
            "author": self.author,
            "version": self.version,
            "license": self.license,
            "keywords": self.keywords,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "related_skills": self.related_skills,
            "average_rating": self.average_rating,
            "rating_count": self.rating_count,
            "skill_type": self.skill_type,
            "compatibility": self.compatibility,
            "custom_fields": self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillMetadata':
        """Create from dictionary"""
        dependencies = [
            SkillDependency(**d) for d in data.get("dependencies", [])
        ]
        return cls(
            skill_id=data["skill_id"],
            name=data["name"],
            description=data["description"],
            tags=data.get("tags", []),
            category=data.get("category"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            usage_count=data.get("usage_count", 0),
            success_rate=data.get("success_rate", 0.0),
            status=SkillStatus(data.get("status", "draft")),
            visibility=SkillVisibility(data.get("visibility", "private")),
            author=data.get("author"),
            version=data.get("version", "1.0.0"),
            license=data.get("license", "MIT"),
            keywords=data.get("keywords", []),
            dependencies=dependencies,
            related_skills=data.get("related_skills", []),
            average_rating=data.get("average_rating", 0.0),
            rating_count=data.get("rating_count", 0),
            skill_type=data.get("skill_type"),
            compatibility=data.get("compatibility", []),
            custom_fields=data.get("custom_fields", {})
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
    - Comprehensive metadata management
    - Semantic search and indexing
    - Collections and tagging
    - Version diffing and rollback
    - Publishing workflows
    - Context composition
    - Ratings and feedback
    """
    
    def __init__(self, storage_dir: str = "./SkillHub"):
        self.storage_dir = Path(storage_dir)
        self.skills_dir = self.storage_dir / "skills"
        self.collections_dir = self.storage_dir / "collections"
        self.ratings_dir = self.storage_dir / "ratings"
        self.compositions_dir = self.storage_dir / "compositions"
        self.diffs_dir = self.storage_dir / "diffs"
        self.index_file = self.storage_dir / "index.json"
        self.search_index_file = self.storage_dir / "search_index.json"
        
        self._initialize_storage()
        self._skills: Dict[str, Skill] = self._load_index()
        self._collections: Dict[str, SkillCollection] = self._load_collections()
        self._ratings: Dict[str, List[SkillRating]] = self._load_ratings()
        self._compositions: Dict[str, ContextComposition] = self._load_compositions()
        self._search_index: Dict[str, SearchIndex] = self._load_search_index()
    
    def _initialize_storage(self):
        """Initialize storage directories"""
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.collections_dir.mkdir(parents=True, exist_ok=True)
        self.ratings_dir.mkdir(parents=True, exist_ok=True)
        self.compositions_dir.mkdir(parents=True, exist_ok=True)
        self.diffs_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_collections(self) -> Dict[str, SkillCollection]:
        """Load collections from disk"""
        collections = {}
        if self.collections_dir.exists():
            for filename in self.collections_dir.glob("*.json"):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        collection = SkillCollection(
                            collection_id=data["collection_id"],
                            name=data["name"],
                            description=data["description"],
                            skill_ids=data.get("skill_ids", []),
                            tags=data.get("tags", []),
                            created_at=data.get("created_at"),
                            updated_at=data.get("updated_at"),
                            author=data.get("author")
                        )
                        collections[collection.collection_id] = collection
                except Exception:
                    continue
        return collections
    
    def _save_collection(self, collection: SkillCollection):
        """Save a collection to disk"""
        filepath = self.collections_dir / f"{collection.collection_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(collection.to_dict(), f, indent=2)
    
    def _load_ratings(self) -> Dict[str, List[SkillRating]]:
        """Load ratings from disk"""
        ratings = {}
        if self.ratings_dir.exists():
            for filename in self.ratings_dir.glob("*.json"):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        skill_id = filename.stem
                        ratings[skill_id] = [
                            SkillRating(
                                rating_id=r["rating_id"],
                                skill_id=r["skill_id"],
                                rating=r["rating"],
                                feedback=r.get("feedback"),
                                reviewer=r.get("reviewer"),
                                created_at=r.get("created_at")
                            )
                            for r in data
                        ]
                except Exception:
                    continue
        return ratings
    
    def _save_ratings(self, skill_id: str):
        """Save ratings for a skill to disk"""
        if skill_id in self._ratings:
            filepath = self.ratings_dir / f"{skill_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in self._ratings[skill_id]], f, indent=2)
    
    def _load_compositions(self) -> Dict[str, ContextComposition]:
        """Load context compositions from disk"""
        compositions = {}
        if self.compositions_dir.exists():
            for filename in self.compositions_dir.glob("*.json"):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        slots = {
                            k: ContextSlot(
                                slot_id=v["slot_id"],
                                name=v["name"],
                                description=v["description"],
                                required=v.get("required", True),
                                default_skill_id=v.get("default_skill_id"),
                                allowed_skill_types=v.get("allowed_skill_types", [])
                            )
                            for k, v in data.get("slots", {}).items()
                        }
                        composition = ContextComposition(
                            composition_id=data["composition_id"],
                            name=data["name"],
                            description=data["description"],
                            slots=slots,
                            bindings=data.get("bindings", {}),
                            created_at=data.get("created_at"),
                            updated_at=data.get("updated_at")
                        )
                        compositions[composition.composition_id] = composition
                except Exception:
                    continue
        return compositions
    
    def _save_composition(self, composition: ContextComposition):
        """Save a context composition to disk"""
        filepath = self.compositions_dir / f"{composition.composition_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(composition.to_dict(), f, indent=2)
    
    def _load_search_index(self) -> Dict[str, SearchIndex]:
        """Load search index from disk"""
        if self.search_index_file.exists():
            try:
                with open(self.search_index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        skill_id: SearchIndex(
                            skill_id=idx["skill_id"],
                            name_tokens=idx.get("name_tokens", []),
                            description_tokens=idx.get("description_tokens", []),
                            tag_tokens=idx.get("tag_tokens", []),
                            content_tokens=idx.get("content_tokens", []),
                            category_tokens=idx.get("category_tokens", [])
                        )
                        for skill_id, idx in data.items()
                    }
            except Exception:
                pass
        return {}
    
    def _save_search_index(self):
        """Save search index to disk"""
        with open(self.search_index_file, 'w', encoding='utf-8') as f:
            json.dump({
                skill_id: idx.to_dict()
                for skill_id, idx in self._search_index.items()
            }, f, indent=2)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for search indexing"""
        if not text:
            return []
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return list(set(tokens))
    
    def _update_search_index(self, skill: Skill):
        """Update search index for a skill"""
        latest = skill.latest_version
        index = SearchIndex(
            skill_id=skill.metadata.skill_id,
            name_tokens=self._tokenize(skill.metadata.name),
            description_tokens=self._tokenize(skill.metadata.description),
            tag_tokens=skill.metadata.tags,
            content_tokens=self._tokenize(latest.content) if latest else [],
            category_tokens=[skill.metadata.category] if skill.metadata.category else []
        )
        self._search_index[skill.metadata.skill_id] = index
        self._save_search_index()
    
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
        author: Optional[str] = None,
        status: SkillStatus = SkillStatus.DRAFT,
        visibility: SkillVisibility = SkillVisibility.PRIVATE,
        keywords: Optional[List[str]] = None,
        dependencies: Optional[List[SkillDependency]] = None,
        skill_type: Optional[str] = None
    ) -> Skill:
        """
        Create a new skill with comprehensive metadata
        
        Args:
            name: Skill name
            description: Skill description
            content: Skill content (SKILL.md format)
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            status: Skill status
            visibility: Skill visibility
            keywords: Optional keywords for search
            dependencies: Optional skill dependencies
            skill_type: Optional skill type
            
        Returns:
            Created Skill object
        """
        skill_id = self._generate_skill_id(name)
        
        metadata = SkillMetadata(
            skill_id=skill_id,
            name=name,
            description=description,
            tags=tags or [],
            category=category,
            author=author,
            status=status,
            visibility=visibility,
            keywords=keywords or [],
            dependencies=dependencies or [],
            skill_type=skill_type
        )
        
        skill = Skill(metadata)
        skill.add_version(content, author=author, change_description="Initial version")
        
        self._skills[skill_id] = skill
        self._save_skill(skill)
        self._update_search_index(skill)
        
        return skill
    
    def update_skill_metadata(
        self,
        skill_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        status: Optional[SkillStatus] = None,
        visibility: Optional[SkillVisibility] = None,
        author: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        dependencies: Optional[List[SkillDependency]] = None,
        related_skills: Optional[List[str]] = None,
        skill_type: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Optional[Skill]:
        """
        Update skill metadata
        
        Args:
            skill_id: Skill ID to update
            name: Optional new name
            description: Optional new description
            tags: Optional new tags
            category: Optional new category
            status: Optional new status
            visibility: Optional new visibility
            author: Optional new author
            keywords: Optional new keywords
            dependencies: Optional new dependencies
            related_skills: Optional related skills
            skill_type: Optional skill type
            custom_fields: Optional custom fields
            
        Returns:
            Updated Skill object or None if not found
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        if name is not None:
            skill.metadata.name = name
        if description is not None:
            skill.metadata.description = description
        if tags is not None:
            skill.metadata.tags = tags
        if category is not None:
            skill.metadata.category = category
        if status is not None:
            skill.metadata.status = status
        if visibility is not None:
            skill.metadata.visibility = visibility
        if author is not None:
            skill.metadata.author = author
        if keywords is not None:
            skill.metadata.keywords = keywords
        if dependencies is not None:
            skill.metadata.dependencies = dependencies
        if related_skills is not None:
            skill.metadata.related_skills = related_skills
        if skill_type is not None:
            skill.metadata.skill_type = skill_type
        if custom_fields is not None:
            skill.metadata.custom_fields.update(custom_fields)
        
        skill.metadata.updated_at = datetime.now().isoformat()
        self._save_skill(skill)
        self._update_search_index(skill)
        
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

        if skill_id in self._search_index:
            del self._search_index[skill_id]
            self._save_search_index()

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
            "categories": categories,
            "total_collections": len(self._collections),
            "total_compositions": len(self._compositions)
        }
    
    def create_collection(
        self,
        name: str,
        description: str,
        skill_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> SkillCollection:
        """
        Create a new skill collection
        
        Args:
            name: Collection name
            description: Collection description
            skill_ids: Optional list of skill IDs to include
            tags: Optional tags for the collection
            author: Optional author name
            
        Returns:
            Created SkillCollection object
        """
        collection_id = f"collection-{len(self._collections) + 1}"
        collection = SkillCollection(
            collection_id=collection_id,
            name=name,
            description=description,
            skill_ids=skill_ids or [],
            tags=tags or [],
            author=author
        )
        self._collections[collection_id] = collection
        self._save_collection(collection)
        return collection
    
    def add_skill_to_collection(self, collection_id: str, skill_id: str) -> bool:
        """
        Add a skill to a collection
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID to add
            
        Returns:
            True if successful, False otherwise
        """
        collection = self._collections.get(collection_id)
        if not collection or skill_id not in self._skills:
            return False
        
        if skill_id not in collection.skill_ids:
            collection.skill_ids.append(skill_id)
            collection.updated_at = datetime.now().isoformat()
            self._save_collection(collection)
        return True
    
    def remove_skill_from_collection(self, collection_id: str, skill_id: str) -> bool:
        """
        Remove a skill from a collection
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID to remove
            
        Returns:
            True if successful, False otherwise
        """
        collection = self._collections.get(collection_id)
        if not collection:
            return False
        
        if skill_id in collection.skill_ids:
            collection.skill_ids.remove(skill_id)
            collection.updated_at = datetime.now().isoformat()
            self._save_collection(collection)
        return True
    
    def get_collection(self, collection_id: str) -> Optional[SkillCollection]:
        """Get a collection by ID"""
        return self._collections.get(collection_id)
    
    def list_collections(self) -> List[SkillCollection]:
        """List all collections"""
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection"""
        if collection_id not in self._collections:
            return False
        
        filepath = self.collections_dir / f"{collection_id}.json"
        if filepath.exists():
            filepath.unlink()
        
        del self._collections[collection_id]
        return True
    
    def add_rating(
        self,
        skill_id: str,
        rating: float,
        feedback: Optional[str] = None,
        reviewer: Optional[str] = None
    ) -> Optional[SkillRating]:
        """
        Add a rating to a skill
        
        Args:
            skill_id: Skill ID
            rating: Rating value (0-5)
            feedback: Optional feedback text
            reviewer: Optional reviewer name
            
        Returns:
            Created SkillRating object or None
        """
        if skill_id not in self._skills:
            return None
        
        rating_id = f"rating-{len(self._ratings.get(skill_id, [])) + 1}"
        rating_obj = SkillRating(
            rating_id=rating_id,
            skill_id=skill_id,
            rating=max(0.0, min(5.0, rating)),
            feedback=feedback,
            reviewer=reviewer
        )
        
        if skill_id not in self._ratings:
            self._ratings[skill_id] = []
        self._ratings[skill_id].append(rating_obj)
        
        skill = self._skills[skill_id]
        total_rating = sum(r.rating for r in self._ratings[skill_id])
        skill.metadata.average_rating = total_rating / len(self._ratings[skill_id])
        skill.metadata.rating_count = len(self._ratings[skill_id])
        
        self._save_ratings(skill_id)
        self._save_skill(skill)
        return rating_obj
    
    def get_ratings(self, skill_id: str) -> List[SkillRating]:
        """Get all ratings for a skill"""
        return self._ratings.get(skill_id, [])
    
    def compute_version_diff(
        self,
        skill_id: str,
        from_version: int,
        to_version: int
    ) -> Optional[VersionDiff]:
        """
        Compute difference between two skill versions
        
        Args:
            skill_id: Skill ID
            from_version: Source version number
            to_version: Target version number
            
        Returns:
            VersionDiff object or None
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        v1 = skill.get_version(from_version)
        v2 = skill.get_version(to_version)
        if not v1 or not v2:
            return None
        
        diff = difflib.unified_diff(
            v1.content.splitlines(),
            v2.content.splitlines(),
            fromfile=f"v{from_version}",
            tofile=f"v{to_version}",
            lineterm=''
        )
        
        additions = []
        deletions = []
        modifications = []
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                additions.append(line[1:])
            elif line.startswith('-') and not line.startswith('---'):
                deletions.append(line[1:])
        
        diff_id = f"diff-{skill_id}-{from_version}-{to_version}"
        version_diff = VersionDiff(
            diff_id=diff_id,
            skill_id=skill_id,
            from_version=from_version,
            to_version=to_version,
            additions=additions,
            deletions=deletions,
            modifications=modifications
        )
        
        diff_file = self.diffs_dir / f"{diff_id}.json"
        with open(diff_file, 'w', encoding='utf-8') as f:
            json.dump(version_diff.to_dict(), f, indent=2)
        
        return version_diff
    
    def rollback_to_version(
        self,
        skill_id: str,
        version: int,
        author: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Rollback skill to a previous version
        
        Args:
            skill_id: Skill ID
            version: Version to rollback to
            author: Optional author name
            
        Returns:
            Updated Skill object or None
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        target_version = skill.get_version(version)
        if not target_version:
            return None
        
        skill.add_version(
            target_version.content,
            author=author,
            change_description=f"Rollback to version {version}"
        )
        
        self._save_skill(skill)
        self._update_search_index(skill)
        return skill
    
    def publish_skill(
        self,
        skill_id: str,
        visibility: SkillVisibility = SkillVisibility.PUBLIC
    ) -> Optional[Skill]:
        """
        Publish a skill
        
        Args:
            skill_id: Skill ID
            visibility: Visibility level
            
        Returns:
            Updated Skill object or None
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        return self.update_skill_metadata(
            skill_id,
            status=SkillStatus.PUBLISHED,
            visibility=visibility
        )
    
    def deprecate_skill(self, skill_id: str) -> Optional[Skill]:
        """Deprecate a skill"""
        return self.update_skill_metadata(skill_id, status=SkillStatus.DEPRECATED)
    
    def archive_skill(self, skill_id: str) -> Optional[Skill]:
        """Archive a skill"""
        return self.update_skill_metadata(skill_id, status=SkillStatus.ARCHIVED)
    
    def create_composition(
        self,
        name: str,
        description: str,
        slots: Optional[Dict[str, ContextSlot]] = None
    ) -> ContextComposition:
        """
        Create a context composition
        
        Args:
            name: Composition name
            description: Composition description
            slots: Optional dictionary of slots
            
        Returns:
            Created ContextComposition object
        """
        composition_id = f"composition-{len(self._compositions) + 1}"
        composition = ContextComposition(
            composition_id=composition_id,
            name=name,
            description=description,
            slots=slots or {}
        )
        self._compositions[composition_id] = composition
        self._save_composition(composition)
        return composition
    
    def add_slot_to_composition(
        self,
        composition_id: str,
        slot: ContextSlot
    ) -> bool:
        """
        Add a slot to a composition
        
        Args:
            composition_id: Composition ID
            slot: Slot to add
            
        Returns:
            True if successful
        """
        composition = self._compositions.get(composition_id)
        if not composition:
            return False
        
        composition.slots[slot.slot_id] = slot
        composition.updated_at = datetime.now().isoformat()
        self._save_composition(composition)
        return True
    
    def bind_skill_to_slot(
        self,
        composition_id: str,
        slot_id: str,
        skill_id: str
    ) -> bool:
        """
        Bind a skill to a composition slot
        
        Args:
            composition_id: Composition ID
            slot_id: Slot ID
            skill_id: Skill ID to bind
            
        Returns:
            True if successful
        """
        composition = self._compositions.get(composition_id)
        if not composition or slot_id not in composition.slots or skill_id not in self._skills:
            return False
        
        composition.bindings[slot_id] = skill_id
        composition.updated_at = datetime.now().isoformat()
        self._save_composition(composition)
        return True
    
    def get_composition(self, composition_id: str) -> Optional[ContextComposition]:
        """Get a composition by ID"""
        return self._compositions.get(composition_id)
    
    def list_compositions(self) -> List[ContextComposition]:
        """List all compositions"""
        return list(self._compositions.values())
    
    def delete_composition(self, composition_id: str) -> bool:
        """Delete a composition"""
        if composition_id not in self._compositions:
            return False
        
        filepath = self.compositions_dir / f"{composition_id}.json"
        if filepath.exists():
            filepath.unlink()
        
        del self._compositions[composition_id]
        return True
    
    def semantic_search(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        status: Optional[SkillStatus] = None,
        limit: int = 20
    ) -> List[Tuple[Skill, float]]:
        """
        Enhanced semantic search using search index
        
        Args:
            query: Search query
            tags: Optional tag filter
            category: Optional category filter
            status: Optional status filter
            limit: Maximum results
            
        Returns:
            List of (Skill, score) tuples sorted by relevance
        """
        query_tokens = self._tokenize(query)
        results = []
        
        for skill_id, index in self._search_index.items():
            skill = self._skills.get(skill_id)
            if not skill:
                continue
            
            if status and skill.metadata.status != status:
                continue
            
            if category and skill.metadata.category != category:
                continue
            
            if tags:
                if not any(tag in skill.metadata.tags for tag in tags):
                    continue
            
            score = 0.0
            
            name_overlap = len(set(query_tokens) & set(index.name_tokens))
            score += name_overlap * 3.0
            
            desc_overlap = len(set(query_tokens) & set(index.description_tokens))
            score += desc_overlap * 2.0
            
            tag_overlap = len(set(query_tokens) & set(index.tag_tokens))
            score += tag_overlap * 2.5
            
            content_overlap = len(set(query_tokens) & set(index.content_tokens))
            score += content_overlap * 1.0
            
            category_overlap = len(set(query_tokens) & set(index.category_tokens))
            score += category_overlap * 2.0
            
            if tags:
                tag_match = len(set(tags) & set(skill.metadata.tags))
                score += tag_match * 1.5
            
            score += skill.metadata.usage_count * 0.01
            score += skill.metadata.success_rate * 0.5
            score += skill.metadata.average_rating * 0.2
            
            if score > 0:
                results.append((skill, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]


class PluginMarketplace:
    """
    Octopai Plugin Marketplace - Skill Repository System
    
    Manages skill repositories, plugin installations, and marketplace operations.
    Features include repository management, skill discovery, installation,
    and updates with version tracking.
    """
    
    def __init__(self, marketplace_dir: str = "./PluginMarketplace"):
        self.marketplace_dir = Path(marketplace_dir)
        self.repos_dir = self.marketplace_dir / "repositories"
        self.installed_dir = self.marketplace_dir / "installed"
        self.repos_index = self.marketplace_dir / "repos.json"
        self.installed_index = self.marketplace_dir / "installed.json"
        
        self._initialize_storage()
        self._repositories: Dict[str, Dict[str, Any]] = self._load_repositories()
        self._installed: Dict[str, Dict[str, Any]] = self._load_installed()
    
    def _initialize_storage(self):
        """Initialize marketplace storage directories"""
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        self.installed_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.repos_index.exists():
            self._save_repositories({})
        if not self.installed_index.exists():
            self._save_installed({})
    
    def _load_repositories(self) -> Dict[str, Dict[str, Any]]:
        """Load registered repositories"""
        if self.repos_index.exists():
            try:
                with open(self.repos_index, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_repositories(self, repos: Dict[str, Dict[str, Any]]):
        """Save registered repositories"""
        with open(self.repos_index, 'w', encoding='utf-8') as f:
            json.dump(repos, f, indent=2)
    
    def _load_installed(self) -> Dict[str, Dict[str, Any]]:
        """Load installed skills"""
        if self.installed_index.exists():
            try:
                with open(self.installed_index, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_installed(self, installed: Dict[str, Dict[str, Any]]):
        """Save installed skills index"""
        with open(self.installed_index, 'w', encoding='utf-8') as f:
            json.dump(installed, f, indent=2)
    
    def add_repository(
        self,
        repo_id: str,
        name: str,
        url: str,
        description: Optional[str] = None,
        priority: int = 0
    ) -> Dict[str, Any]:
        """
        Register a new skill repository
        
        Args:
            repo_id: Unique repository identifier
            name: Repository name
            url: Repository URL
            description: Optional description
            priority: Repository priority for search ordering
            
        Returns:
            Repository information
        """
        repo = {
            "repo_id": repo_id,
            "name": name,
            "url": url,
            "description": description,
            "priority": priority,
            "added_at": datetime.now().isoformat(),
            "last_updated": None
        }
        
        self._repositories[repo_id] = repo
        self._save_repositories(self._repositories)
        return repo
    
    def remove_repository(self, repo_id: str) -> bool:
        """Remove a registered repository"""
        if repo_id not in self._repositories:
            return False
        
        del self._repositories[repo_id]
        self._save_repositories(self._repositories)
        return True
    
    def list_repositories(self) -> List[Dict[str, Any]]:
        """List all registered repositories"""
        return list(self._repositories.values())
    
    def install_skill_from_folder(
        self,
        folder_path: Union[str, Path],
        repo_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Install a skill from a folder
        
        Args:
            folder_path: Path to the skill folder
            repo_source: Optional repository source identifier
            
        Returns:
            Installation information
        """
        from octopai.core.skill_spec import SkillFolder, OctopaiSkillSpec
        
        skill_folder = SkillFolder(folder_path)
        skill_spec = skill_folder.load_skill()
        
        skill_id = skill_spec.name.lower().replace(' ', '-')
        install_dir = self.installed_dir / skill_id
        
        if install_dir.exists():
            existing = self._installed.get(skill_id, {})
            current_version = existing.get('version', '0.0.0')
            
            if current_version == skill_spec.version:
                return {
                    "skill_id": skill_id,
                    "status": "already_installed",
                    "version": skill_spec.version
                }
        
        import shutil
        if install_dir.exists():
            shutil.rmtree(install_dir)
        
        shutil.copytree(folder_path, install_dir)
        
        install_info = {
            "skill_id": skill_id,
            "name": skill_spec.name,
            "version": skill_spec.version,
            "description": skill_spec.description,
            "author": skill_spec.author,
            "license": skill_spec.license,
            "category": skill_spec.category.value if hasattr(skill_spec.category, 'value') else str(skill_spec.category),
            "tags": skill_spec.tags,
            "keywords": skill_spec.keywords,
            "installed_at": datetime.now().isoformat(),
            "install_path": str(install_dir),
            "repo_source": repo_source
        }
        
        self._installed[skill_id] = install_info
        self._save_installed(self._installed)
        
        return {
            "skill_id": skill_id,
            "status": "installed",
            "version": skill_spec.version,
            "info": install_info
        }
    
    def uninstall_skill(self, skill_id: str) -> bool:
        """Uninstall a skill"""
        if skill_id not in self._installed:
            return False
        
        install_info = self._installed[skill_id]
        install_path = Path(install_info.get('install_path', ''))
        
        if install_path.exists():
            import shutil
            shutil.rmtree(install_path)
        
        del self._installed[skill_id]
        self._save_installed(self._installed)
        return True
    
    def list_installed_skills(self) -> List[Dict[str, Any]]:
        """List all installed skills"""
        return list(self._installed.values())
    
    def get_installed_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get an installed skill by ID"""
        return self._installed.get(skill_id)
    
    def load_installed_skill_spec(self, skill_id: str) -> Optional['OctopaiSkillSpec']:
        """Load an installed skill specification"""
        from octopai.core.skill_spec import SkillFolder
        
        install_info = self._installed.get(skill_id)
        if not install_info:
            return None
        
        install_path = Path(install_info['install_path'])
        if not install_path.exists():
            return None
        
        skill_folder = SkillFolder(install_path)
        return skill_folder.load_skill()
    
    def get_marketplace_statistics(self) -> Dict[str, Any]:
        """Get marketplace statistics"""
        return {
            "total_repositories": len(self._repositories),
            "total_installed": len(self._installed),
            "installed_by_category": self._group_by_category(),
            "repositories": list(self._repositories.keys())
        }
    
    def _group_by_category(self) -> Dict[str, int]:
        """Group installed skills by category"""
        categories = {}
        for skill in self._installed.values():
            cat = skill.get('category', 'Uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
        return categories


# Add to SkillHub for folder-based skill support
def import_skill_from_folder(
    self,
    folder_path: Union[str, Path],
    author: Optional[str] = None
) -> Skill:
    """
    Import a skill from a folder into SkillHub
    
    Args:
        folder_path: Path to the skill folder
        author: Optional author name
        
    Returns:
        Imported Skill object
    """
    from octopai.core.skill_spec import SkillFolder, OctopaiSkillSpec
    
    skill_folder = SkillFolder(folder_path)
    skill_spec = skill_folder.load_skill()
    
    content = skill_spec.to_skill_md()
    
    return self.create_skill(
        name=skill_spec.name,
        description=skill_spec.description,
        content=content,
        tags=skill_spec.tags,
        category=skill_spec.category.value if hasattr(skill_spec.category, 'value') else str(skill_spec.category),
        author=author or skill_spec.author,
        keywords=skill_spec.keywords
    )


def export_skill_to_folder(
    self,
    skill_id: str,
    output_path: Union[str, Path]
) -> Optional[Path]:
    """
    Export a skill from SkillHub to a folder
    
    Args:
        skill_id: Skill ID to export
        output_path: Output directory path
        
    Returns:
        Path to the exported folder or None
    """
    from octopai.core.skill_spec import (
        OctopaiSkillSpec, SkillCategory, create_skill_folder,
        SkillExample, SkillGuideline
    )
    
    skill = self._skills.get(skill_id)
    if not skill:
        return None
    
    latest = skill.latest_version
    if not latest:
        return None
    
    category = SkillCategory(skill.metadata.category) if skill.metadata.category else SkillCategory.GENERAL
    
    skill_spec = OctopaiSkillSpec(
        name=skill.metadata.name,
        description=skill.metadata.description,
        version=skill.metadata.version,
        author=skill.metadata.author,
        license=skill.metadata.license,
        category=category,
        tags=skill.metadata.tags,
        keywords=skill.metadata.keywords,
        content=latest.content
    )
    
    folder = create_skill_folder(skill_spec, output_path)
    return folder.folder_path


# Attach methods to SkillHub class
SkillHub.import_skill_from_folder = import_skill_from_folder
SkillHub.export_skill_to_folder = export_skill_to_folder
