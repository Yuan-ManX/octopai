"""
Skill Manager
Core management logic for skill registry
"""

import uuid
import re
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import json

from .models import (
    Skill, SkillVersion, SkillMetadata, User, Organization,
    Visibility, SkillStatus
)


class SkillManager:
    """Manager for skill registry operations"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the skill manager
        
        Args:
            storage_path: Path for storing skill data, uses .octopai/skills if not provided
        """
        self.storage_path = storage_path or Path(".octopai") / "skills"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self._skills: Dict[str, Skill] = {}
        self._users: Dict[str, User] = {}
        self._organizations: Dict[str, Organization] = {}
        self._user_stars: Dict[str, set] = {}  # user_id -> set of skill_ids
        self._skill_slug_index: Dict[str, str] = {}  # full_slug -> skill_id
        
        self._load_from_storage()
    
    def _generate_slug(self, name: str) -> str:
        """Generate a URL-safe slug from name"""
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        return slug
    
    def _get_full_slug(self, namespace: str, slug: str) -> str:
        """Get full slug including namespace"""
        return f"{namespace}/{slug}"
    
    def _save_to_storage(self) -> None:
        """Save current state to storage"""
        data = {
            "skills": {k: v.to_dict() for k, v in self._skills.items()},
            "users": {k: v.to_dict() for k, v in self._users.items()},
            "organizations": {k: v.to_dict() for k, v in self._organizations.items()},
            "user_stars": {k: list(v) for k, v in self._user_stars.items()},
            "skill_slug_index": self._skill_slug_index
        }
        
        storage_file = self.storage_path / "registry.json"
        storage_file.write_text(json.dumps(data, indent=2))
    
    def _load_from_storage(self) -> None:
        """Load state from storage"""
        storage_file = self.storage_path / "registry.json"
        
        if not storage_file.exists():
            return
        
        try:
            data = json.loads(storage_file.read_text())
            
            self._skill_slug_index = data.get("skill_slug_index", {})
        except (json.JSONDecodeError, KeyError):
            pass
    
    def create_user(self, username: str, email: str, display_name: Optional[str] = None) -> User:
        """
        Create a new user
        
        Args:
            username: Unique username
            email: User email
            display_name: Optional display name
            
        Returns:
            Created User object
        """
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            display_name=display_name
        )
        
        self._users[user_id] = user
        self._user_stars[user_id] = set()
        self._save_to_storage()
        
        return user
    
    def create_organization(self, name: str, slug: str, description: Optional[str] = None) -> Organization:
        """
        Create a new organization
        
        Args:
            name: Organization name
            slug: Unique organization slug
            description: Optional description
            
        Returns:
            Created Organization object
        """
        org_id = str(uuid.uuid4())
        org = Organization(
            org_id=org_id,
            name=name,
            slug=slug,
            description=description
        )
        
        self._organizations[org_id] = org
        self._save_to_storage()
        
        return org
    
    def create_skill(
        self,
        name: str,
        description: str,
        namespace: str,
        visibility: str,
        content: str,
        metadata_dict: Dict[str, Any],
        created_by: str,
        owner_type: str = "user",
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Skill:
        """
        Create a new skill
        
        Args:
            name: Skill name
            description: Skill description
            namespace: Namespace (username or org slug)
            visibility: Visibility level
            content: Skill content
            metadata_dict: Metadata dictionary
            created_by: Creator user ID
            owner_type: "user" or "organization"
            categories: Optional categories
            tags: Optional tags
            
        Returns:
            Created Skill object
        """
        skill_id = str(uuid.uuid4())
        slug = self._generate_slug(name)
        full_slug = self._get_full_slug(namespace, slug)
        
        if full_slug in self._skill_slug_index:
            raise ValueError(f"Skill with slug {full_slug} already exists")
        
        metadata = SkillMetadata(
            name=metadata_dict.get("name", name),
            description=metadata_dict.get("description", description),
            version=metadata_dict.get("version", "1.0.0"),
            author=metadata_dict.get("author", created_by),
            category=metadata_dict.get("category"),
            tags=metadata_dict.get("tags", []),
            keywords=metadata_dict.get("keywords", []),
            license=metadata_dict.get("license"),
            homepage=metadata_dict.get("homepage"),
            repository=metadata_dict.get("repository"),
            documentation=metadata_dict.get("documentation"),
            compatibility=metadata_dict.get("compatibility"),
            requirements=metadata_dict.get("requirements")
        )
        
        version_id = str(uuid.uuid4())
        version = SkillVersion(
            version_id=version_id,
            skill_id=skill_id,
            version=metadata.version,
            metadata=metadata,
            content=content,
            changelog=metadata_dict.get("changelog", "Initial release"),
            created_by=created_by,
            is_latest=True
        )
        
        skill = Skill(
            skill_id=skill_id,
            name=name,
            slug=slug,
            description=description,
            visibility=Visibility(visibility),
            status=SkillStatus.PUBLISHED,
            owner_type=owner_type,
            owner_id=created_by if owner_type == "user" else namespace,
            namespace=namespace,
            metadata=metadata,
            latest_version=version,
            versions=[version],
            categories=categories or [],
            tags=tags or [],
            created_by=created_by
        )
        
        self._skills[skill_id] = skill
        self._skill_slug_index[full_slug] = skill_id
        self._save_to_storage()
        
        return skill
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID"""
        skill = self._skills.get(skill_id)
        if skill:
            skill.view_count += 1
            self._save_to_storage()
        return skill
    
    def get_skill_by_slug(self, namespace: str, slug: str) -> Optional[Skill]:
        """Get a skill by namespace and slug"""
        full_slug = self._get_full_slug(namespace, slug)
        skill_id = self._skill_slug_index.get(full_slug)
        return self.get_skill(skill_id) if skill_id else None
    
    def list_skills(
        self,
        namespace: Optional[str] = None,
        visibility: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Skill], int]:
        """
        List skills with filters
        
        Args:
            namespace: Filter by namespace
            visibility: Filter by visibility
            category: Filter by category
            tags: Filter by tags
            sort_by: Sort field
            sort_order: Sort order
            page: Page number
            page_size: Page size
            
        Returns:
            Tuple of (skills list, total count)
        """
        skills = list(self._skills.values())
        
        if namespace:
            skills = [s for s in skills if s.namespace == namespace]
        
        if visibility:
            skills = [s for s in skills if s.visibility.value == visibility]
        
        if category:
            skills = [s for s in skills if category in s.categories]
        
        if tags:
            skills = [s for s in skills if any(tag in s.tags for tag in tags)]
        
        skills = [s for s in skills if s.visibility == Visibility.PUBLIC]
        
        reverse = sort_order == "desc"
        skills.sort(key=lambda x: getattr(x, sort_by, x.updated_at), reverse=reverse)
        
        total = len(skills)
        start = (page - 1) * page_size
        end = start + page_size
        
        return skills[start:end], total
    
    def search_skills(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        visibility: Optional[str] = None,
        namespace: Optional[str] = None,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Skill], int]:
        """
        Search skills
        
        Args:
            query: Search query
            category: Filter by category
            tags: Filter by tags
            visibility: Filter by visibility
            namespace: Filter by namespace
            sort_by: Sort field
            sort_order: Sort order
            page: Page number
            page_size: Page size
            
        Returns:
            Tuple of (skills list, total count)
        """
        skills, _ = self.list_skills(
            namespace=namespace,
            visibility=visibility,
            category=category,
            tags=tags,
            sort_by=sort_by,
            sort_order=sort_order,
            page=1,
            page_size=1000
        )
        
        if query:
            query_lower = query.lower()
            skills = [
                s for s in skills
                if query_lower in s.name.lower()
                or query_lower in s.description.lower()
                or any(query_lower in tag.lower() for tag in s.tags)
                or any(query_lower in keyword.lower() for keyword in s.metadata.keywords)
            ]
        
        total = len(skills)
        start = (page - 1) * page_size
        end = start + page_size
        
        return skills[start:end], total
    
    def create_skill_version(
        self,
        skill_id: str,
        version: str,
        content: str,
        metadata_dict: Dict[str, Any],
        created_by: str,
        changelog: Optional[str] = None
    ) -> Optional[SkillVersion]:
        """
        Create a new version of a skill
        
        Args:
            skill_id: Skill ID
            version: Version string
            content: Skill content
            metadata_dict: Metadata dictionary
            created_by: Creator user ID
            changelog: Optional changelog
            
        Returns:
            Created SkillVersion object or None if skill not found
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        for v in skill.versions:
            if v.version == version:
                raise ValueError(f"Version {version} already exists")
        
        metadata = SkillMetadata(
            name=metadata_dict.get("name", skill.name),
            description=metadata_dict.get("description", skill.description),
            version=version,
            author=metadata_dict.get("author", created_by),
            category=metadata_dict.get("category"),
            tags=metadata_dict.get("tags", []),
            keywords=metadata_dict.get("keywords", []),
            license=metadata_dict.get("license"),
            homepage=metadata_dict.get("homepage"),
            repository=metadata_dict.get("repository"),
            documentation=metadata_dict.get("documentation"),
            compatibility=metadata_dict.get("compatibility"),
            requirements=metadata_dict.get("requirements")
        )
        
        if skill.latest_version:
            skill.latest_version.is_latest = False
        
        version_id = str(uuid.uuid4())
        new_version = SkillVersion(
            version_id=version_id,
            skill_id=skill_id,
            version=version,
            metadata=metadata,
            content=content,
            changelog=changelog,
            created_by=created_by,
            is_latest=True
        )
        
        skill.versions.append(new_version)
        skill.latest_version = new_version
        skill.metadata = metadata
        skill.updated_at = datetime.now()
        
        self._save_to_storage()
        
        return new_version
    
    def update_skill(
        self,
        skill_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        visibility: Optional[str] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Skill]:
        """Update a skill"""
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        if name is not None:
            skill.name = name
        
        if description is not None:
            skill.description = description
        
        if visibility is not None:
            skill.visibility = Visibility(visibility)
        
        if categories is not None:
            skill.categories = categories
        
        if tags is not None:
            skill.tags = tags
        
        skill.updated_at = datetime.now()
        self._save_to_storage()
        
        return skill
    
    def toggle_star(self, user_id: str, skill_id: str) -> bool:
        """
        Toggle star on a skill
        
        Args:
            user_id: User ID
            skill_id: Skill ID
            
        Returns:
            True if starred, False if unstarred
        """
        if user_id not in self._user_stars:
            self._user_stars[user_id] = set()
        
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        
        if skill_id in self._user_stars[user_id]:
            self._user_stars[user_id].remove(skill_id)
            skill.star_count = max(0, skill.star_count - 1)
            starred = False
        else:
            self._user_stars[user_id].add(skill_id)
            skill.star_count += 1
            starred = True
        
        self._save_to_storage()
        return starred
    
    def is_starred(self, user_id: str, skill_id: str) -> bool:
        """Check if user has starred a skill"""
        return skill_id in self._user_stars.get(user_id, set())
    
    def download_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Download a skill
        
        Args:
            skill_id: Skill ID
            version: Optional version, uses latest if not provided
            
        Returns:
            Tuple of (content, version) or None if not found
        """
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        skill_version = None
        if version:
            skill_version = next((v for v in skill.versions if v.version == version), None)
        else:
            skill_version = skill.latest_version
        
        if not skill_version:
            return None
        
        skill_version.download_count += 1
        skill.download_count += 1
        self._save_to_storage()
        
        return skill_version.content, skill_version.version
    
    def fork_skill(
        self,
        skill_id: str,
        new_namespace: str,
        new_name: Optional[str] = None,
        forked_by: str = ""
    ) -> Optional[Skill]:
        """
        Fork a skill
        
        Args:
            skill_id: Skill ID to fork
            new_namespace: New namespace
            new_name: Optional new name
            forked_by: User ID forking
            
        Returns:
            Forked Skill object or None if not found
        """
        original = self._skills.get(skill_id)
        if not original:
            return None
        
        original.fork_count += 1
        
        name = new_name or original.name
        
        if not original.latest_version:
            return None
        
        forked_skill = self.create_skill(
            name=name,
            description=original.description,
            namespace=new_namespace,
            visibility=original.visibility.value,
            content=original.latest_version.content,
            metadata_dict=original.latest_version.metadata.to_dict(),
            created_by=forked_by,
            owner_type=original.owner_type,
            categories=original.categories.copy(),
            tags=original.tags.copy()
        )
        
        return forked_skill
    
    def delete_skill(self, skill_id: str) -> bool:
        """Delete a skill"""
        skill = self._skills.get(skill_id)
        if not skill:
            return False
        
        full_slug = self._get_full_slug(skill.namespace, skill.slug)
        
        del self._skills[skill_id]
        if full_slug in self._skill_slug_index:
            del self._skill_slug_index[full_slug]
        
        for user_stars in self._user_stars.values():
            user_stars.discard(skill_id)
        
        self._save_to_storage()
        return True
    
    def reset(self) -> None:
        """Reset the manager state"""
        self._skills.clear()
        self._users.clear()
        self._organizations.clear()
        self._user_stars.clear()
        self._skill_slug_index.clear()
        
        storage_file = self.storage_path / "registry.json"
        if storage_file.exists():
            storage_file.unlink()
