"""
Skill Registry - Octopai's Advanced Skill Registry System

This module provides Octopai's proprietary skill registry system with
slug management, redirects, merging, soft deletion, owner management,
starring, and comprehensive search capabilities.
"""

import os
import json
import re
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path


class SkillRegistryStatus(Enum):
    """Status of a skill in the registry"""
    ACTIVE = "active"
    DELETED = "deleted"
    HIDDEN = "hidden"
    MERGED = "merged"


class RedirectType(Enum):
    """Type of redirect"""
    RENAME = "rename"
    MERGE = "merge"
    ALIAS = "alias"


@dataclass
class SkillComment:
    """Comment on a skill"""
    comment_id: str
    skill_id: str
    author: str
    content: str
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "comment_id": self.comment_id,
            "skill_id": self.skill_id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillComment':
        return cls(**data)


@dataclass
class SkillStar:
    """Star rating for a skill"""
    star_id: str
    skill_id: str
    user_id: str
    rating: float
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "star_id": self.star_id,
            "skill_id": self.skill_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillStar':
        return cls(**data)


@dataclass
class SkillRedirect:
    """Redirect from one slug to another"""
    redirect_id: str
    from_slug: str
    to_slug: str
    redirect_type: RedirectType
    created_by: str
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "redirect_id": self.redirect_id,
            "from_slug": self.from_slug,
            "to_slug": self.to_slug,
            "redirect_type": self.redirect_type.value,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillRedirect':
        data = data.copy()
        data['redirect_type'] = RedirectType(data['redirect_type'])
        return cls(**data)


@dataclass
class SkillInstallRecord:
    """Record of a skill installation"""
    install_id: str
    skill_id: str
    slug: str
    version: str
    installed_by: str
    installed_at: str
    is_local: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "install_id": self.install_id,
            "skill_id": self.skill_id,
            "slug": self.slug,
            "version": self.version,
            "installed_by": self.installed_by,
            "installed_at": self.installed_at,
            "is_local": self.is_local
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillInstallRecord':
        return cls(**data)


@dataclass
class RegistrySkillMetadata:
    """Extended metadata for registry skills"""
    slug: str
    skill_id: str
    name: str
    description: str
    version: str
    author: str
    owner_id: str
    tags: List[str] = field(default_factory=list)
    category: Optional[str] = None
    status: SkillRegistryStatus = SkillRegistryStatus.ACTIVE
    visibility: str = "public"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    install_count: int = 0
    star_count: int = 0
    average_rating: float = 0.0
    license: str = "MIT"
    changelog: List[Dict[str, Any]] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "slug": self.slug,
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "owner_id": self.owner_id,
            "tags": self.tags,
            "category": self.category,
            "status": self.status.value,
            "visibility": self.visibility,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "install_count": self.install_count,
            "star_count": self.star_count,
            "average_rating": self.average_rating,
            "license": self.license,
            "changelog": self.changelog,
            "custom_fields": self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegistrySkillMetadata':
        data = data.copy()
        data['status'] = SkillRegistryStatus(data['status'])
        return cls(**data)


class SkillRegistry:
    """
    Octopai's Advanced Skill Registry System
    
    Features:
    - Slug-based skill identification with redirect support
    - Skill renaming without breaking links
    - Skill merging with canonical slugs
    - Soft delete/restore capabilities
    - Owner management and permissions
    - Star ratings and comments
    - Installation tracking
    - Versioned skill publishing
    - Search and discovery
    """
    
    def __init__(self, storage_dir: str = "./SkillRegistry"):
        self.storage_dir = Path(storage_dir)
        self.skills_dir = self.storage_dir / "skills"
        self.redirects_dir = self.storage_dir / "redirects"
        self.comments_dir = self.storage_dir / "comments"
        self.stars_dir = self.storage_dir / "stars"
        self.installs_dir = self.storage_dir / "installs"
        self.index_file = self.storage_dir / "index.json"
        self.slug_index_file = self.storage_dir / "slug_index.json"
        
        self._initialize_storage()
        
        self._skills: Dict[str, RegistrySkillMetadata] = self._load_skills()
        self._slug_to_id: Dict[str, str] = self._load_slug_index()
        self._redirects: Dict[str, SkillRedirect] = self._load_redirects()
        self._comments: Dict[str, List[SkillComment]] = self._load_comments()
        self._stars: Dict[str, List[SkillStar]] = self._load_stars()
        self._installs: Dict[str, List[SkillInstallRecord]] = self._load_installs()
    
    def _initialize_storage(self):
        """Initialize storage directories"""
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.redirects_dir.mkdir(parents=True, exist_ok=True)
        self.comments_dir.mkdir(parents=True, exist_ok=True)
        self.stars_dir.mkdir(parents=True, exist_ok=True)
        self.installs_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.index_file.exists():
            self._save_index({})
        if not self.slug_index_file.exists():
            self._save_slug_index({})
    
    def _load_skills(self) -> Dict[str, RegistrySkillMetadata]:
        """Load skills from disk"""
        skills = {}
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                    for skill_id, skill_path in index_data.items():
                        skill_file = self.storage_dir / skill_path
                        if skill_file.exists():
                            with open(skill_file, 'r', encoding='utf-8') as sf:
                                skill_data = json.load(sf)
                                skills[skill_id] = RegistrySkillMetadata.from_dict(skill_data)
            except Exception as e:
                print(f"Error loading skills: {e}")
        return skills
    
    def _save_index(self, index: Dict[str, str]):
        """Save skill index to disk"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _load_slug_index(self) -> Dict[str, str]:
        """Load slug to skill ID mapping"""
        if self.slug_index_file.exists():
            try:
                with open(self.slug_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading slug index: {e}")
        return {}
    
    def _save_slug_index(self, index: Dict[str, str]):
        """Save slug index to disk"""
        with open(self.slug_index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _load_redirects(self) -> Dict[str, SkillRedirect]:
        """Load redirects from disk"""
        redirects = {}
        for redirect_file in self.redirects_dir.glob("*.json"):
            try:
                with open(redirect_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    redirect = SkillRedirect.from_dict(data)
                    redirects[redirect.from_slug] = redirect
            except Exception as e:
                print(f"Error loading redirect {redirect_file}: {e}")
        return redirects
    
    def _save_redirect(self, redirect: SkillRedirect):
        """Save a redirect to disk"""
        filepath = self.redirects_dir / f"{redirect.redirect_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(redirect.to_dict(), f, indent=2)
    
    def _load_comments(self) -> Dict[str, List[SkillComment]]:
        """Load comments from disk"""
        comments = {}
        for comment_file in self.comments_dir.glob("*.json"):
            try:
                with open(comment_file, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)
                    skill_id = comment_file.stem
                    comments[skill_id] = [SkillComment.from_dict(d) for d in data_list]
            except Exception as e:
                print(f"Error loading comments {comment_file}: {e}")
        return comments
    
    def _save_comments(self, skill_id: str):
        """Save comments for a skill"""
        if skill_id in self._comments:
            filepath = self.comments_dir / f"{skill_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([c.to_dict() for c in self._comments[skill_id]], f, indent=2)
    
    def _load_stars(self) -> Dict[str, List[SkillStar]]:
        """Load stars from disk"""
        stars = {}
        for star_file in self.stars_dir.glob("*.json"):
            try:
                with open(star_file, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)
                    skill_id = star_file.stem
                    stars[skill_id] = [SkillStar.from_dict(d) for d in data_list]
            except Exception as e:
                print(f"Error loading stars {star_file}: {e}")
        return stars
    
    def _save_stars(self, skill_id: str):
        """Save stars for a skill"""
        if skill_id in self._stars:
            filepath = self.stars_dir / f"{skill_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([s.to_dict() for s in self._stars[skill_id]], f, indent=2)
    
    def _load_installs(self) -> Dict[str, List[SkillInstallRecord]]:
        """Load install records from disk"""
        installs = {}
        for install_file in self.installs_dir.glob("*.json"):
            try:
                with open(install_file, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)
                    skill_id = install_file.stem
                    installs[skill_id] = [SkillInstallRecord.from_dict(d) for d in data_list]
            except Exception as e:
                print(f"Error loading installs {install_file}: {e}")
        return installs
    
    def _save_installs(self, skill_id: str):
        """Save install records for a skill"""
        if skill_id in self._installs:
            filepath = self.installs_dir / f"{skill_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([i.to_dict() for i in self._installs[skill_id]], f, indent=2)
    
    def _save_skill(self, skill: RegistrySkillMetadata):
        """Save a skill to disk"""
        skill_file = self.skills_dir / f"{skill.skill_id}.json"
        with open(skill_file, 'w', encoding='utf-8') as f:
            json.dump(skill.to_dict(), f, indent=2, ensure_ascii=False)
        
        index = {s.skill_id: f"skills/{s.skill_id}.json" for s in self._skills.values()}
        self._save_index(index)
        
        self._slug_to_id[skill.slug] = skill.skill_id
        self._save_slug_index(self._slug_to_id)
    
    def _generate_id(self, prefix: str) -> str:
        """Generate a unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(os.urandom(8)).hexdigest()[:6]
        return f"{prefix}_{timestamp}_{random_suffix}"
    
    def _slugify(self, name: str) -> str:
        """Convert name to URL-safe slug"""
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        return slug
    
    def _generate_unique_slug(self, base_slug: str) -> str:
        """Generate a unique slug"""
        slug = base_slug
        counter = 1
        while slug in self._slug_to_id or slug in self._redirects:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    def publish_skill(
        self,
        name: str,
        description: str,
        version: str,
        author: str,
        owner_id: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        visibility: str = "public",
        license: str = "MIT",
        changelog_entry: Optional[str] = None
    ) -> RegistrySkillMetadata:
        """
        Publish a new skill to the registry
        
        Args:
            name: Skill name
            description: Skill description
            version: Semantic version
            author: Author name
            owner_id: Owner ID
            tags: Optional tags
            category: Optional category
            visibility: Visibility level
            license: License type
            changelog_entry: Optional changelog entry
            
        Returns:
            Created RegistrySkillMetadata
        """
        base_slug = self._slugify(name)
        slug = self._generate_unique_slug(base_slug)
        skill_id = self._generate_id("skill")
        
        changelog = []
        if changelog_entry:
            changelog.append({
                "version": version,
                "date": datetime.now().isoformat(),
                "changes": changelog_entry
            })
        
        skill = RegistrySkillMetadata(
            slug=slug,
            skill_id=skill_id,
            name=name,
            description=description,
            version=version,
            author=author,
            owner_id=owner_id,
            tags=tags or [],
            category=category,
            status=SkillRegistryStatus.ACTIVE,
            visibility=visibility,
            license=license,
            changelog=changelog
        )
        
        self._skills[skill_id] = skill
        self._save_skill(skill)
        
        return skill
    
    def get_skill_by_slug(self, slug: str) -> Optional[RegistrySkillMetadata]:
        """
        Get a skill by slug, following redirects
        
        Args:
            slug: Skill slug
            
        Returns:
            RegistrySkillMetadata or None
        """
        if slug in self._redirects:
            redirect = self._redirects[slug]
            return self.get_skill_by_slug(redirect.to_slug)
        
        if slug in self._slug_to_id:
            skill_id = self._slug_to_id[slug]
            return self._skills.get(skill_id)
        
        return None
    
    def get_skill_by_id(self, skill_id: str) -> Optional[RegistrySkillMetadata]:
        """
        Get a skill by ID
        
        Args:
            skill_id: Skill ID
            
        Returns:
            RegistrySkillMetadata or None
        """
        return self._skills.get(skill_id)
    
    def update_skill_version(
        self,
        skill_id: str,
        new_version: str,
        changelog_entry: str,
        user_id: str
    ) -> Optional[RegistrySkillMetadata]:
        """
        Update a skill's version
        
        Args:
            skill_id: Skill ID
            new_version: New version string
            changelog_entry: Description of changes
            user_id: User making the update
            
        Returns:
            Updated RegistrySkillMetadata or None
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        if skill.owner_id != user_id:
            return None
        
        skill.version = new_version
        skill.updated_at = datetime.now().isoformat()
        skill.changelog.insert(0, {
            "version": new_version,
            "date": datetime.now().isoformat(),
            "changes": changelog_entry
        })
        
        self._save_skill(skill)
        return skill
    
    def rename_skill(
        self,
        skill_id: str,
        new_name: str,
        user_id: str
    ) -> Optional[RegistrySkillMetadata]:
        """
        Rename a skill without breaking old links
        
        Args:
            skill_id: Skill ID
            new_name: New skill name
            user_id: User making the change
            
        Returns:
            Updated RegistrySkillMetadata or None
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        if skill.owner_id != user_id:
            return None
        
        old_slug = skill.slug
        new_base_slug = self._slugify(new_name)
        new_slug = self._generate_unique_slug(new_base_slug)
        
        if old_slug != new_slug:
            redirect = SkillRedirect(
                redirect_id=self._generate_id("redirect"),
                from_slug=old_slug,
                to_slug=new_slug,
                redirect_type=RedirectType.RENAME,
                created_by=user_id,
                created_at=datetime.now().isoformat()
            )
            self._redirects[old_slug] = redirect
            self._save_redirect(redirect)
            
            del self._slug_to_id[old_slug]
        
        skill.name = new_name
        skill.slug = new_slug
        skill.updated_at = datetime.now().isoformat()
        
        self._save_skill(skill)
        return skill
    
    def merge_skills(
        self,
        source_slug: str,
        target_slug: str,
        user_id: str
    ) -> bool:
        """
        Merge a source skill into a target skill
        
        Args:
            source_slug: Source skill slug (will be hidden)
            target_slug: Target skill slug (canonical)
            user_id: User performing the merge
            
        Returns:
            True if successful
        """
        source_skill = self.get_skill_by_slug(source_slug)
        target_skill = self.get_skill_by_slug(target_slug)
        
        if not source_skill or not target_skill:
            return False
        
        if source_skill.owner_id != user_id or target_skill.owner_id != user_id:
            return False
        
        source_skill.status = SkillRegistryStatus.MERGED
        self._save_skill(source_skill)
        
        redirect = SkillRedirect(
            redirect_id=self._generate_id("redirect"),
            from_slug=source_slug,
            to_slug=target_slug,
            redirect_type=RedirectType.MERGE,
            created_by=user_id,
            created_at=datetime.now().isoformat()
        )
        self._redirects[source_slug] = redirect
        self._save_redirect(redirect)
        
        return True
    
    def soft_delete_skill(
        self,
        skill_id: str,
        user_id: str
    ) -> bool:
        """
        Soft delete a skill (can be restored)
        
        Args:
            skill_id: Skill ID
            user_id: User performing the delete
            
        Returns:
            True if successful
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        
        if skill.owner_id != user_id:
            return False
        
        skill.status = SkillRegistryStatus.DELETED
        skill.updated_at = datetime.now().isoformat()
        self._save_skill(skill)
        return True
    
    def restore_skill(
        self,
        skill_id: str,
        user_id: str
    ) -> bool:
        """
        Restore a soft-deleted skill
        
        Args:
            skill_id: Skill ID
            user_id: User performing the restore
            
        Returns:
            True if successful
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        
        if skill.owner_id != user_id:
            return False
        
        skill.status = SkillRegistryStatus.ACTIVE
        skill.updated_at = datetime.now().isoformat()
        self._save_skill(skill)
        return True
    
    def star_skill(
        self,
        skill_id: str,
        user_id: str,
        rating: float
    ) -> SkillStar:
        """
        Star/rate a skill
        
        Args:
            skill_id: Skill ID
            user_id: User ID
            rating: Rating (0-5)
            
        Returns:
            Created SkillStar
        """
        star = SkillStar(
            star_id=self._generate_id("star"),
            skill_id=skill_id,
            user_id=user_id,
            rating=max(0.0, min(5.0, rating)),
            created_at=datetime.now().isoformat()
        )
        
        if skill_id not in self._stars:
            self._stars[skill_id] = []
        
        existing = [s for s in self._stars[skill_id] if s.user_id == user_id]
        for e in existing:
            self._stars[skill_id].remove(e)
        
        self._stars[skill_id].append(star)
        self._save_stars(skill_id)
        
        self._update_skill_ratings(skill_id)
        
        return star
    
    def _update_skill_ratings(self, skill_id: str):
        """Update skill's star count and average rating"""
        skill = self._skills.get(skill_id)
        if not skill:
            return
        
        stars = self._stars.get(skill_id, [])
        skill.star_count = len(stars)
        if stars:
            skill.average_rating = sum(s.rating for s in stars) / len(stars)
        
        self._save_skill(skill)
    
    def add_comment(
        self,
        skill_id: str,
        author: str,
        content: str
    ) -> SkillComment:
        """
        Add a comment to a skill
        
        Args:
            skill_id: Skill ID
            author: Author name
            content: Comment content
            
        Returns:
            Created SkillComment
        """
        comment = SkillComment(
            comment_id=self._generate_id("comment"),
            skill_id=skill_id,
            author=author,
            content=content,
            created_at=datetime.now().isoformat()
        )
        
        if skill_id not in self._comments:
            self._comments[skill_id] = []
        
        self._comments[skill_id].append(comment)
        self._save_comments(skill_id)
        
        return comment
    
    def record_install(
        self,
        skill_id: str,
        slug: str,
        version: str,
        installed_by: str,
        is_local: bool = True
    ) -> SkillInstallRecord:
        """
        Record a skill installation
        
        Args:
            skill_id: Skill ID
            slug: Skill slug
            version: Version installed
            installed_by: User who installed
            is_local: Whether it's a local install
            
        Returns:
            Created SkillInstallRecord
        """
        install = SkillInstallRecord(
            install_id=self._generate_id("install"),
            skill_id=skill_id,
            slug=slug,
            version=version,
            installed_by=installed_by,
            installed_at=datetime.now().isoformat(),
            is_local=is_local
        )
        
        if skill_id not in self._installs:
            self._installs[skill_id] = []
        
        self._installs[skill_id].append(install)
        self._save_installs(skill_id)
        
        skill = self._skills.get(skill_id)
        if skill:
            skill.install_count += 1
            self._save_skill(skill)
        
        return install
    
    def search_skills(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        sort_by: str = "popular",
        limit: int = 20
    ) -> List[RegistrySkillMetadata]:
        """
        Search for skills in the registry
        
        Args:
            query: Optional search query
            tags: Optional tag filter
            category: Optional category filter
            visibility: Optional visibility filter
            sort_by: Sort method ('popular', 'recent', 'rating', 'name')
            limit: Maximum results
            
        Returns:
            List of matching RegistrySkillMetadata
        """
        results = []
        
        for skill in self._skills.values():
            if skill.status != SkillRegistryStatus.ACTIVE:
                continue
            
            if visibility and skill.visibility != visibility:
                continue
            
            if category and skill.category != category:
                continue
            
            if tags:
                if not any(tag in skill.tags for tag in tags):
                    continue
            
            if query:
                query_lower = query.lower()
                if query_lower not in skill.name.lower() and \
                   query_lower not in skill.description.lower() and \
                   not any(query_lower in tag.lower() for tag in skill.tags):
                    continue
            
            results.append(skill)
        
        if sort_by == "popular":
            results.sort(key=lambda s: (s.install_count, s.star_count), reverse=True)
        elif sort_by == "recent":
            results.sort(key=lambda s: s.updated_at, reverse=True)
        elif sort_by == "rating":
            results.sort(key=lambda s: (s.average_rating, s.star_count), reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda s: s.name.lower())
        
        return results[:limit]
    
    def get_popular_skills(self, limit: int = 10) -> List[RegistrySkillMetadata]:
        """
        Get popular skills by install count
        
        Args:
            limit: Maximum results
            
        Returns:
            List of RegistrySkillMetadata
        """
        return self.search_skills(sort_by="popular", limit=limit)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics
        
        Returns:
            Statistics dictionary
        """
        total_skills = len(self._skills)
        active_skills = sum(1 for s in self._skills.values() if s.status == SkillRegistryStatus.ACTIVE)
        deleted_skills = sum(1 for s in self._skills.values() if s.status == SkillRegistryStatus.DELETED)
        total_installs = sum(len(installs) for installs in self._installs.values())
        total_stars = sum(len(stars) for stars in self._stars.values())
        total_comments = sum(len(comments) for comments in self._comments.values())
        total_redirects = len(self._redirects)
        
        categories = {}
        for skill in self._skills.values():
            if skill.status == SkillRegistryStatus.ACTIVE:
                cat = skill.category or "Uncategorized"
                categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_skills": total_skills,
            "active_skills": active_skills,
            "deleted_skills": deleted_skills,
            "total_installs": total_installs,
            "total_stars": total_stars,
            "total_comments": total_comments,
            "total_redirects": total_redirects,
            "categories": categories
        }
