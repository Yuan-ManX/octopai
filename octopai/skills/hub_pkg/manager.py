"""
Octopai Skills Hub Manager - Enterprise-grade skill repository management.

Core Features:
- Namespace Management (Global + Team)
- Skill Versioning with State Machine
- Review Workflow and Promotion System
- Search and Discovery
- Audit Logging
- Star and Rating System
"""

import json
import re
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, List, Dict, Tuple
from dataclasses import dataclass

from .hub import (
    Namespace,
    NamespaceType,
    NamespaceStatus,
    NamespaceMember,
    NamespaceMemberRole,
    Skill,
    SkillVisibility,
    SkillStatus,
    SkillVersion,
    VersionStatus,
    SkillFile,
    SkillTag,
    ReviewTask,
    ReviewStatus,
    PromotionRequest,
    SkillStar,
    SkillRating,
    AuditLog,
    UserAccount,
    PlatformRole,
    SkillSearchDocument,
    SkillHubEvent,
    SkillRepository,
    RepositoryVisibility,
    RepositoryStatus,
)


@dataclass
class PublishRequest:
    """Request to publish a skill version.
    
    Attributes:
        namespace_id: Target namespace
        skill_id: Skill ID (if updating existing)
        skill_name: Name for new skill
        version: Semantic version
        content: Skill content
        changelog: Change log
        metadata: Additional metadata
    """
    namespace_id: str = ""
    skill_id: Optional[str] = None
    skill_name: str = ""
    version: str = "1.0.0"
    content: str = ""
    changelog: str = ""
    metadata: Dict[str, Any] = None


@dataclass
class SearchResult:
    """Result from a search operation.
    
    Attributes:
        skills: Matching skills
        total_count: Total matches
        query: Search query
        filters_applied: Filters used
        search_time_ms: Time in milliseconds
    """
    skills: List[Skill] = None
    total_count: int = 0
    query: str = ""
    filters_applied: Dict[str, Any] = None
    search_time_ms: float = 0.0

    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.filters_applied is None:
            self.filters_applied = {}


@dataclass
class HubStatistics:
    """Aggregated statistics for the hub.
    
    Attributes:
        total_namespaces: Namespace count
        total_skills: Skill count
        public_skills: Public skill count
        total_versions: Version count
        total_downloads: Download count
        total_stars: Star count
        pending_reviews: Pending reviews
        top_categories: Popular categories
    """
    total_namespaces: int = 0
    total_skills: int = 0
    public_skills: int = 0
    total_versions: int = 0
    total_downloads: int = 0
    total_stars: int = 0
    pending_reviews: int = 0
    top_categories: List[Tuple[str, int]] = None

    def __post_init__(self):
        if self.top_categories is None:
            self.top_categories = []


class SkillsHubManager:
    """Main manager for Octopai Skills Hub operations."""

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize Skills Hub Manager."""
        self.storage_dir = storage_dir or Path(".octopai/skills_hub")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # In-memory storage
        self.namespaces: Dict[str, Namespace] = {}
        self.skills: Dict[str, Skill] = {}
        self.versions: Dict[str, SkillVersion] = {}
        self.review_tasks: Dict[str, ReviewTask] = {}
        self.promotion_requests: Dict[str, PromotionRequest] = {}
        self.stars: Dict[str, SkillStar] = {}
        self.ratings: Dict[str, SkillRating] = {}
        self.audit_logs: List[AuditLog] = []
        self.users: Dict[str, UserAccount] = {}
        self.search_docs: Dict[str, SkillSearchDocument] = {}
        self.events: List[SkillHubEvent] = []

        # Reserved slugs
        self.reserved_slugs = {
            "admin", "api", "dashboard", "search", "auth", "me",
            "global", "system", "static", "assets", "health"
        }

        # Create default global namespace and load data
        self._initialize_global_namespace()
        self._load_data()

    def _initialize_global_namespace(self):
        """Create default global namespace."""
        if "global" not in self.namespaces:
            global_ns = Namespace(
                id="global",
                slug="global",
                display_name="Global",
                type=NamespaceType.GLOBAL,
                description="Global namespace for shared skills",
                created_by="system",
            )
            self.namespaces["global"] = global_ns

    def _generate_id(self) -> str:
        """Generate unique ID."""
        return str(uuid.uuid4())

    def _slugify(self, name: str) -> str:
        """Convert name to URL-safe slug."""
        slug = name.lower().strip()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')

    def _is_valid_slug(self, slug: str) -> bool:
        """Check if slug is valid and not reserved."""
        if not slug or len(slug) < 2 or len(slug) > 64:
            return False
        if slug in self.reserved_slugs:
            return False
        if '--' in slug:
            return False
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', slug):
            return False
        return True

    def _increment_version(self, current_version: str) -> str:
        """Increment semantic version (patch)."""
        parts = current_version.split('.')
        if len(parts) >= 3:
            patch = int(parts[-1]) + 1
            parts[-1] = str(patch)
            return '.'.join(parts)
        elif len(parts) == 2:
            return f"{parts[0]}.{parts[1]}.1"
        else:
            return f"{current_version}.1"

    def _log_audit(self, actor_user_id: str, action: str, 
                  target_type: str, target_id: str,
                  detail: Optional[Dict[str, Any]] = None,
                  request_id: Optional[str] = None,
                  client_ip: Optional[str] = None,
                  user_agent: Optional[str] = None) -> AuditLog:
        """Create audit log entry."""
        log = AuditLog(
            id=self._generate_id(),
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            request_id=request_id,
            client_ip=client_ip,
            user_agent=user_agent,
            detail_json=detail or {},
        )
        self.audit_logs.append(log)
        self._save_audit_logs()
        return log

    def _emit_event(self, event_type: str, user_id: str,
                   skill_id: Optional[str] = None,
                   namespace_id: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None):
        """Emit skill hub event."""
        event = SkillHubEvent(
            event_type=event_type,
            skill_id=skill_id,
            namespace_id=namespace_id,
            user_id=user_id,
            metadata=metadata or {},
        )
        self.events.append(event)

    # ============================================
    # Namespace Management
    # ============================================

    def create_namespace(self, name: str, owner_id: str,
                        description: str = "",
                        namespace_type: NamespaceType = NamespaceType.TEAM,
                        avatar_url: Optional[str] = None) -> Namespace:
        """Create a new namespace."""
        slug = self._slugify(name)
        
        if not self._is_valid_slug(slug):
            raise ValueError(f"Invalid namespace name: {name}")
        
        if slug in self.namespaces:
            raise ValueError(f"Namespace '{slug}' already exists")
        
        namespace_id = self._generate_id()
        
        namespace = Namespace(
            id=namespace_id,
            slug=slug,
            display_name=name,
            type=namespace_type,
            description=description,
            avatar_url=avatar_url,
            created_by=owner_id,
        )
        
        # Add owner as member
        owner_member = NamespaceMember(
            namespace_id=namespace_id,
            user_id=owner_id,
            role=NamespaceMemberRole.OWNER,
        )
        namespace.members.append(owner_member)
        
        self.namespaces[namespace_id] = self.namespaces[slug] = namespace
        
        self._log_audit(owner_id, "create_namespace", "namespace", namespace_id)
        self._emit_event("namespace_created", owner_id, namespace_id=namespace_id)
        
        self._save_namespaces()
        return namespace

    def get_namespace(self, namespace_id: str) -> Optional[Namespace]:
        """Get namespace by ID or slug."""
        return self.namespaces.get(namespace_id)

    def list_namespaces(self, user_id: Optional[str] = None,
                      namespace_type: Optional[NamespaceType] = None,
                      status: Optional[NamespaceStatus] = None) -> List[Namespace]:
        """List namespaces with filters."""
        results = list(self.namespaces.values())
        
        if namespace_type:
            results = [ns for ns in results if ns.type == namespace_type]
        
        if status:
            results = [ns for ns in results if ns.status == status]
        
        if user_id:
            results = [ns for ns in results if 
                      any(m.user_id == user_id for m in ns.members) or
                      ns.type == NamespaceType.GLOBAL]
        
        return sorted(results, key=lambda ns: ns.created_at, reverse=True)

    def update_namespace(self, namespace_id: str,
                        display_name: Optional[str] = None,
                        description: Optional[str] = None,
                        avatar_url: Optional[str] = None,
                        status: Optional[NamespaceStatus] = None,
                        updater_id: Optional[str] = None) -> Optional[Namespace]:
        """Update a namespace."""
        namespace = self.namespaces.get(namespace_id)
        if not namespace:
            return None
        
        if display_name is not None:
            namespace.display_name = display_name
        if description is not None:
            namespace.description = description
        if avatar_url is not None:
            namespace.avatar_url = avatar_url
        if status is not None:
            namespace.status = status
        
        namespace.updated_at = datetime.now()
        if updater_id:
            self._log_audit(updater_id, "update_namespace", "namespace", namespace_id)
        
        self._save_namespaces()
        return namespace

    def add_namespace_member(self, namespace_id: str,
                            user_id: str,
                            role: NamespaceMemberRole,
                            added_by: str) -> Optional[NamespaceMember]:
        """Add a member to a namespace."""
        namespace = self.namespaces.get(namespace_id)
        if not namespace:
            return None
        
        # Check if already member
        existing = next((m for m in namespace.members if m.user_id == user_id), None)
        if existing:
            existing.role = role
            existing.updated_at = datetime.now()
            member = existing
        else:
            member = NamespaceMember(
                namespace_id=namespace_id,
                user_id=user_id,
                role=role,
            )
            namespace.members.append(member)
        
        self._log_audit(added_by, "add_member", "namespace", namespace_id,
                       {"user_id": user_id, "role": role.value})
        self._save_namespaces()
        return member

    def remove_namespace_member(self, namespace_id: str,
                               user_id: str,
                               removed_by: str) -> bool:
        """Remove a member from a namespace."""
        namespace = self.namespaces.get(namespace_id)
        if not namespace:
            return False
        
        original_len = len(namespace.members)
        namespace.members = [m for m in namespace.members if m.user_id != user_id]
        
        if len(namespace.members) < original_len:
            self._log_audit(removed_by, "remove_member", "namespace", namespace_id,
                           {"user_id": user_id})
            self._save_namespaces()
            return True
        
        return False

    def get_user_namespace_role(self, namespace_id: str,
                               user_id: str) -> Optional[NamespaceMemberRole]:
        """Get a user's role in a namespace."""
        namespace = self.namespaces.get(namespace_id)
        if not namespace:
            return None
        
        member = next((m for m in namespace.members if m.user_id == user_id), None)
        return member.role if member else None

    # ============================================
    # Skill Management
    # ============================================

    def create_skill(self, namespace_id: str,
                    name: str,
                    owner_id: str,
                    summary: str = "",
                    visibility: SkillVisibility = SkillVisibility.PRIVATE,
                    category: str = "general",
                    topics: Optional[List[str]] = None) -> Skill:
        """Create a new skill container."""
        namespace = self.namespaces.get(namespace_id)
        if not namespace:
            raise ValueError(f"Namespace not found: {namespace_id}")
        
        slug = self._slugify(name)
        if not self._is_valid_slug(slug):
            raise ValueError(f"Invalid skill name: {name}")
        
        # Check for duplicate slug in namespace
        for skill in self.skills.values():
            if skill.namespace_id == namespace_id and skill.slug == slug:
                raise ValueError(f"Skill '{slug}' already exists in this namespace")
        
        skill_id = self._generate_id()
        
        skill = Skill(
            id=skill_id,
            namespace_id=namespace_id,
            slug=slug,
            display_name=name,
            summary=summary,
            owner_id=owner_id,
            visibility=visibility,
            category=category,
            topics=topics or [],
            created_by=owner_id,
            updated_by=owner_id,
        )
        
        self.skills[skill_id] = skill
        
        self._log_audit(owner_id, "create_skill", "skill", skill_id)
        self._emit_event("skill_created", owner_id, skill_id=skill_id,
                       namespace_id=namespace_id)
        
        self._save_skills()
        return skill

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get skill by ID."""
        return self.skills.get(skill_id)

    def get_skill_by_namespace_slug(self, namespace_slug: str,
                                   skill_slug: str) -> Optional[Skill]:
        """Get skill by namespace slug and skill slug."""
        namespace = self.namespaces.get(namespace_slug)
        if not namespace:
            namespace = self.namespaces.get(namespace_slug)
        
        if not namespace:
            return None
        
        for skill in self.skills.values():
            if skill.namespace_id == namespace.id and skill.slug == skill_slug:
                return skill
        
        return None

    def list_skills(self, namespace_id: Optional[str] = None,
                   visibility: Optional[SkillVisibility] = None,
                   status: Optional[SkillStatus] = None,
                   category: Optional[str] = None,
                   owner_id: Optional[str] = None,
                   limit: int = 50,
                   offset: int = 0,
                   sort_by: str = "updated_at",
                   sort_order: str = "desc") -> List[Skill]:
        """List skills with filters."""
        results = list(self.skills.values())
        
        if namespace_id:
            results = [s for s in results if s.namespace_id == namespace_id]
        
        if visibility:
            results = [s for s in results if s.visibility == visibility]
        
        if status:
            results = [s for s in results if s.status == status]
        
        if category:
            results = [s for s in results if s.category == category]
        
        if owner_id:
            results = [s for s in results if s.owner_id == owner_id]
        
        reverse = sort_order.lower() == "desc"
        results.sort(key=lambda s: getattr(s, sort_by, ""), reverse=reverse)
        
        return results[offset:offset + limit]

    def update_skill(self, skill_id: str,
                    display_name: Optional[str] = None,
                    summary: Optional[str] = None,
                    visibility: Optional[SkillVisibility] = None,
                    status: Optional[SkillStatus] = None,
                    owner_id: Optional[str] = None,
                    category: Optional[str] = None,
                    topics: Optional[List[str]] = None,
                    hidden: Optional[bool] = None,
                    updater_id: Optional[str] = None) -> Optional[Skill]:
        """Update a skill."""
        skill = self.skills.get(skill_id)
        if not skill:
            return None
        
        if display_name is not None:
            skill.display_name = display_name
        if summary is not None:
            skill.summary = summary
        if visibility is not None:
            skill.visibility = visibility
        if status is not None:
            skill.status = status
        if owner_id is not None:
            skill.owner_id = owner_id
        if category is not None:
            skill.category = category
        if topics is not None:
            skill.topics = topics
        if hidden is not None:
            skill.hidden = hidden
            skill.hidden_at = datetime.now() if hidden else None
            skill.hidden_by = updater_id if hidden else None
        
        skill.updated_at = datetime.now()
        if updater_id:
            skill.updated_by = updater_id
            self._log_audit(updater_id, "update_skill", "skill", skill_id)
        
        self._save_skills()
        return skill

    def delete_skill(self, skill_id: str, deleter_id: str) -> bool:
        """Delete a skill."""
        if skill_id not in self.skills:
            return False
        
        del self.skills[skill_id]
        
        # Remove dependent data
        self.versions = {vid: v for vid, v in self.versions.items() 
                       if v.skill_id != skill_id}
        self.review_tasks = {rtid: rt for rtid, rt in self.review_tasks.items() 
                           if rt.skill_version_id not in 
                           [v.id for v in self.versions.values() if v.skill_id == skill_id]}
        
        self._log_audit(deleter_id, "delete_skill", "skill", skill_id)
        self._save_skills()
        return True

    # ============================================
    # Version Management
    # ============================================

    def create_version(self, skill_id: str,
                      version: str,
                      content: str,
                      created_by: str,
                      changelog: str = "",
                      metadata: Optional[Dict[str, Any]] = None) -> SkillVersion:
        """Create a new skill version."""
        skill = self.skills.get(skill_id)
        if not skill:
            raise ValueError(f"Skill not found: {skill_id}")
        
        # Check for duplicate version
        for v in skill.versions:
            if v.version == version:
                raise ValueError(f"Version {version} already exists")
        
        version_id = self._generate_id()
        
        # Create entry file
        entry_file = SkillFile(
            id=self._generate_id(),
            skill_version_id=version_id,
            file_path="skill.md",
            content_type="text/plain",
            size_bytes=len(content.encode()),
            is_entry_file=True,
        )
        
        skill_version = SkillVersion(
            id=version_id,
            skill_id=skill_id,
            version=version,
            changelog=changelog,
            parsed_metadata_json=metadata or {},
            manifest_json={"files": ["skill.md"]},
            files=[entry_file],
            status=VersionStatus.DRAFT,
        )
        
        self.versions[version_id] = skill_version
        skill.versions.append(skill_version)
        
        self._log_audit(created_by, "create_version", "skill_version", version_id)
        self._emit_event("version_created", created_by, skill_id=skill_id)
        
        self._save_versions()
        return skill_version

    def submit_for_review(self, version_id: str,
                         submitter_id: str) -> Optional[SkillVersion]:
        """Submit a version for review."""
        version = self.versions.get(version_id)
        if not version:
            return None
        
        if version.status != VersionStatus.DRAFT and version.status != VersionStatus.REJECTED:
            raise ValueError("Only draft or rejected versions can be submitted")
        
        skill = self.skills.get(version.skill_id)
        if not skill:
            return None
        
        existing_review = next((rt for rt in self.review_tasks.values() 
                             if rt.skill_version_id == version_id 
                             and rt.status == ReviewStatus.PENDING), None)
        if existing_review:
            del self.review_tasks[existing_review.id]
        
        review_id = self._generate_id()
        review = ReviewTask(
            id=review_id,
            skill_version_id=version_id,
            namespace_id=skill.namespace_id,
            submitted_by=submitter_id,
        )
        
        self.review_tasks[review_id] = review
        version.status = VersionStatus.PENDING_REVIEW
        
        self._log_audit(submitter_id, "submit_review", "skill_version", version_id)
        self._emit_event("review_submitted", submitter_id, skill_id=skill.id)
        
        self._save_review_tasks()
        self._save_versions()
        return version

    def approve_version(self, review_id: str,
                       reviewer_id: str,
                       comment: str = "") -> Optional[SkillVersion]:
        """Approve a version."""
        review = self.review_tasks.get(review_id)
        if not review or review.status != ReviewStatus.PENDING:
            return None
        
        version = self.versions.get(review.skill_version_id)
        if not version:
            return None
        
        review.status = ReviewStatus.APPROVED
        review.reviewed_by = reviewer_id
        review.review_comment = comment
        review.reviewed_at = datetime.now()
        
        version.status = VersionStatus.PUBLISHED
        version.published_by = reviewer_id
        version.published_at = datetime.now()
        
        skill = self.skills.get(version.skill_id)
        if skill:
            skill.latest_version_id = version.id
            skill.updated_at = datetime.now()
            skill.updated_by = reviewer_id
        
        self._log_audit(reviewer_id, "approve_version", "review", review_id,
                       {"comment": comment})
        self._emit_event("version_published", reviewer_id, skill_id=version.skill_id)
        
        self._save_review_tasks()
        self._save_versions()
        self._save_skills()
        return version

    def reject_version(self, review_id: str,
                      reviewer_id: str,
                      reason: str) -> Optional[SkillVersion]:
        """Reject a version."""
        review = self.review_tasks.get(review_id)
        if not review or review.status != ReviewStatus.PENDING:
            return None
        
        version = self.versions.get(review.skill_version_id)
        if not version:
            return None
        
        review.status = ReviewStatus.REJECTED
        review.reviewed_by = reviewer_id
        review.review_comment = reason
        review.reviewed_at = datetime.now()
        
        version.status = VersionStatus.REJECTED
        version.reject_reason = reason
        
        self._log_audit(reviewer_id, "reject_version", "review", review_id,
                       {"reason": reason})
        self._emit_event("version_rejected", reviewer_id, skill_id=version.skill_id)
        
        self._save_review_tasks()
        self._save_versions()
        return version

    def withdraw_review(self, review_id: str,
                       withdrawer_id: str) -> Optional[SkillVersion]:
        """Withdraw a pending review."""
        review = self.review_tasks.get(review_id)
        if not review or review.status != ReviewStatus.PENDING:
            return None
        
        version = self.versions.get(review.skill_version_id)
        if not version:
            return None
        
        del self.review_tasks[review_id]
        version.status = VersionStatus.DRAFT
        
        self._log_audit(withdrawer_id, "withdraw_review", "review", review_id)
        self._save_review_tasks()
        self._save_versions()
        return version

    def yank_version(self, version_id: str,
                    yanker_id: str) -> Optional[SkillVersion]:
        """Yank (withdraw) a published version."""
        version = self.versions.get(version_id)
        if not version or version.status != VersionStatus.PUBLISHED:
            return None
        
        version.status = VersionStatus.YANKED
        
        skill = self.skills.get(version.skill_id)
        if skill and skill.latest_version_id == version_id:
            latest = None
            for v in sorted(skill.versions, key=lambda x: x.created_at, reverse=True):
                if v.status == VersionStatus.PUBLISHED and v.id != version_id:
                    latest = v
                    break
            skill.latest_version_id = latest.id if latest else None
        
        self._log_audit(yanker_id, "yank_version", "skill_version", version_id)
        self._emit_event("version_yanked", yanker_id, skill_id=version.skill_id)
        
        self._save_versions()
        self._save_skills()
        return version

    def get_version(self, version_id: str) -> Optional[SkillVersion]:
        """Get version by ID."""
        return self.versions.get(version_id)

    def get_latest_published_version(self, skill_id: str) -> Optional[SkillVersion]:
        """Get latest published version."""
        skill = self.skills.get(skill_id)
        if not skill or not skill.latest_version_id:
            return None
        return self.versions.get(skill.latest_version_id)

    # ============================================
    # Promotion System
    # ============================================

    def request_promotion(self, source_skill_id: str,
                         source_version_id: str,
                         submitter_id: str,
                         target_namespace_id: str = "global") -> PromotionRequest:
        """Request to promote a team skill to global."""
        source_skill = self.skills.get(source_skill_id)
        if not source_skill:
            raise ValueError(f"Source skill not found")
        
        source_version = self.versions.get(source_version_id)
        if not source_version or source_version.status != VersionStatus.PUBLISHED:
            raise ValueError("Only published versions can be promoted")
        
        for pr in self.promotion_requests.values():
            if pr.source_skill_id == source_skill_id and pr.status == ReviewStatus.PENDING:
                raise ValueError("Already a pending promotion")
        
        request_id = self._generate_id()
        request = PromotionRequest(
            id=request_id,
            source_skill_id=source_skill_id,
            source_version_id=source_version_id,
            target_namespace_id=target_namespace_id,
            submitted_by=submitter_id,
        )
        
        self.promotion_requests[request_id] = request
        
        self._log_audit(submitter_id, "request_promotion", "promotion", request_id)
        self._emit_event("promotion_requested", submitter_id, skill_id=source_skill_id)
        
        self._save_promotion_requests()
        return request

    def approve_promotion(self, promotion_id: str,
                        reviewer_id: str,
                        comment: str = "") -> Optional[Skill]:
        """Approve promotion and create skill in target namespace."""
        request = self.promotion_requests.get(promotion_id)
        if not request or request.status != ReviewStatus.PENDING:
            return None
        
        source_skill = self.skills.get(request.source_skill_id)
        source_version = self.versions.get(request.source_version_id)
        target_namespace = self.namespaces.get(request.target_namespace_id)
        
        if not source_skill or not source_version or not target_namespace:
            return None
        
        new_skill_id = self._generate_id()
        
        new_skill = Skill(
            id=new_skill_id,
            namespace_id=target_namespace.id,
            slug=source_skill.slug,
            display_name=source_skill.display_name,
            summary=source_skill.summary,
            owner_id=reviewer_id,
            source_skill_id=source_skill.id,
            visibility=SkillVisibility.PUBLIC,
            category=source_skill.category,
            topics=source_skill.topics,
            created_by=reviewer_id,
            updated_by=reviewer_id,
        )
        
        self.skills[new_skill_id] = new_skill
        
        new_version_id = self._generate_id()
        new_version = SkillVersion(
            id=new_version_id,
            skill_id=new_skill_id,
            version=source_version.version,
            changelog=source_version.changelog,
            manifest_json=source_version.manifest_json,
            parsed_metadata_json=source_version.parsed_metadata_json,
            status=VersionStatus.PUBLISHED,
            published_by=reviewer_id,
            published_at=datetime.now(),
        )
        
        for file in source_version.files:
            new_file = SkillFile(
                id=self._generate_id(),
                skill_version_id=new_version_id,
                file_path=file.file_path,
                content_type=file.content_type,
                size_bytes=file.size_bytes,
                sha256=file.sha256,
                object_key=file.object_key,
                is_entry_file=file.is_entry_file,
            )
            new_version.files.append(new_file)
        
        self.versions[new_version_id] = new_version
        new_skill.versions.append(new_version)
        new_skill.latest_version_id = new_version_id
        
        request.status = ReviewStatus.APPROVED
        request.target_skill_id = new_skill_id
        request.reviewed_by = reviewer_id
        request.review_comment = comment
        request.reviewed_at = datetime.now()
        
        self._log_audit(reviewer_id, "approve_promotion", "promotion", promotion_id)
        self._emit_event("skill_promoted", reviewer_id, skill_id=new_skill_id)
        
        self._save_promotion_requests()
        self._save_skills()
        self._save_versions()
        return new_skill

    def reject_promotion(self, promotion_id: str,
                       reviewer_id: str,
                       reason: str) -> Optional[PromotionRequest]:
        """Reject promotion request."""
        request = self.promotion_requests.get(promotion_id)
        if not request or request.status != ReviewStatus.PENDING:
            return None
        
        request.status = ReviewStatus.REJECTED
        request.reviewed_by = reviewer_id
        request.review_comment = reason
        request.reviewed_at = datetime.now()
        
        self._log_audit(reviewer_id, "reject_promotion", "promotion", promotion_id,
                       {"reason": reason})
        
        self._save_promotion_requests()
        return request

    # ============================================
    # Star and Rating System
    # ============================================

    def star_skill(self, skill_id: str, user_id: str) -> bool:
        """Star a skill."""
        skill = self.skills.get(skill_id)
        if not skill:
            return False
        
        star_key = f"{skill_id}:{user_id}"
        if star_key in self.stars:
            return True
        
        star = SkillStar(
            id=self._generate_id(),
            skill_id=skill_id,
            user_id=user_id,
        )
        self.stars[star_key] = star
        
        skill.star_count += 1
        
        self._log_audit(user_id, "star_skill", "skill", skill_id)
        self._emit_event("skill_starred", user_id, skill_id=skill_id)
        
        self._save_stars()
        self._save_skills()
        return True

    def unstar_skill(self, skill_id: str, user_id: str) -> bool:
        """Unstar a skill."""
        skill = self.skills.get(skill_id)
        if not skill:
            return False
        
        star_key = f"{skill_id}:{user_id}"
        if star_key not in self.stars:
            return True
        
        del self.stars[star_key]
        skill.star_count = max(0, skill.star_count - 1)
        
        self._log_audit(user_id, "unstar_skill", "skill", skill_id)
        self._save_stars()
        self._save_skills()
        return True

    def is_starred(self, skill_id: str, user_id: str) -> bool:
        """Check if user starred skill."""
        return f"{skill_id}:{user_id}" in self.stars

    def rate_skill(self, skill_id: str, user_id: str,
                 score: int) -> SkillRating:
        """Rate a skill (1-5)."""
        if score < 1 or score > 5:
            raise ValueError("Score must be between 1 and 5")
        
        skill = self.skills.get(skill_id)
        if not skill:
            raise ValueError("Skill not found")
        
        rating_key = f"{skill_id}:{user_id}"
        
        if rating_key in self.ratings:
            rating = self.ratings[rating_key]
            rating.score = score
            rating.updated_at = datetime.now()
        else:
            rating = SkillRating(
                id=self._generate_id(),
                skill_id=skill_id,
                user_id=user_id,
                score=score,
            )
            self.ratings[rating_key] = rating
            skill.rating_count += 1
        
        all_ratings = [r.score for r in self.ratings.values() if r.skill_id == skill_id]
        skill.rating_avg = sum(all_ratings) / len(all_ratings) if all_ratings else 0.0
        
        self._log_audit(user_id, "rate_skill", "skill", skill_id, {"score": score})
        self._emit_event("skill_rated", user_id, skill_id=skill_id)
        
        self._save_ratings()
        self._save_skills()
        return rating

    def get_user_rating(self, skill_id: str, user_id: str) -> Optional[SkillRating]:
        """Get user's rating for a skill."""
        return self.ratings.get(f"{skill_id}:{user_id}")

    # ============================================
    # Search and Discovery
    # ============================================

    def search_skills(self, query: str = "",
                    namespace_id: Optional[str] = None,
                    visibility: Optional[SkillVisibility] = None,
                    category: Optional[str] = None,
                    limit: int = 20,
                    offset: int = 0) -> SearchResult:
        """Search for skills."""
        import time
        start_time = time.time()
        
        results = list(self.skills.values())
        
        if namespace_id:
            results = [s for s in results if s.namespace_id == namespace_id]
        
        if visibility:
            results = [s for s in results if s.visibility == visibility]
        
        if category:
            results = [s for s in results if s.category == category]
        
        results = [s for s in results if not s.hidden and s.status == SkillStatus.ACTIVE]
        
        if query:
            query_lower = query.lower()
            results = [
                s for s in results
                if query_lower in s.display_name.lower()
                or query_lower in s.summary.lower()
                or query_lower in s.slug.lower()
                or any(query_lower in t.lower() for t in s.topics)
            ]
        
        results.sort(key=lambda s: (s.star_count * 10 + s.download_count), reverse=True)
        search_time = (time.time() - start_time) * 1000
        
        return SearchResult(
            skills=results[offset:offset + limit],
            total_count=len(results),
            query=query,
            filters_applied={
                "namespace_id": namespace_id,
                "visibility": visibility.value if visibility else None,
                "category": category,
            },
            search_time_ms=search_time,
        )

    def get_popular_skills(self, namespace_id: Optional[str] = None,
                        limit: int = 10) -> List[Skill]:
        """Get popular skills by stars and downloads."""
        results = list(self.skills.values())
        
        if namespace_id:
            results = [s for s in results if s.namespace_id == namespace_id]
        
        results = [s for s in results if s.status == SkillStatus.ACTIVE and not s.hidden]
        results.sort(key=lambda s: (s.star_count * 10 + s.download_count), reverse=True)
        
        return results[:limit]

    def get_recent_skills(self, namespace_id: Optional[str] = None,
                        limit: int = 10) -> List[Skill]:
        """Get recently updated skills."""
        results = list(self.skills.values())
        
        if namespace_id:
            results = [s for s in results if s.namespace_id == namespace_id]
        
        results = [s for s in results if s.status == SkillStatus.ACTIVE and not s.hidden]
        results.sort(key=lambda s: s.updated_at, reverse=True)
        
        return results[:limit]

    # ============================================
    # Download Tracking
    # ============================================

    def record_download(self, skill_id: str, version_id: str,
                       downloader_id: Optional[str] = None) -> bool:
        """Record a skill download."""
        skill = self.skills.get(skill_id)
        if not skill:
            return False
        
        skill.download_count += 1
        
        self._log_audit(downloader_id or "anonymous", "download_skill", 
                      "skill", skill_id, {"version_id": version_id})
        self._emit_event("skill_downloaded", downloader_id or "anonymous", 
                      skill_id=skill_id)
        
        self._save_skills()
        return True

    # ============================================
    # Review and Governance
    # ============================================

    def get_pending_reviews(self, namespace_id: Optional[str] = None,
                           limit: int = 50) -> List[ReviewTask]:
        """Get pending review tasks."""
        results = [rt for rt in self.review_tasks.values() 
                  if rt.status == ReviewStatus.PENDING]
        
        if namespace_id:
            results = [rt for rt in results if rt.namespace_id == namespace_id]
        
        results.sort(key=lambda rt: rt.submitted_at, reverse=True)
        return results[:limit]

    def get_review(self, review_id: str) -> Optional[ReviewTask]:
        """Get a review task."""
        return self.review_tasks.get(review_id)

    def get_pending_promotions(self, limit: int = 50) -> List[PromotionRequest]:
        """Get pending promotion requests."""
        results = [pr for pr in self.promotion_requests.values() 
                  if pr.status == ReviewStatus.PENDING]
        results.sort(key=lambda pr: pr.submitted_at, reverse=True)
        return results[:limit]

    def get_promotion(self, promotion_id: str) -> Optional[PromotionRequest]:
        """Get a promotion request."""
        return self.promotion_requests.get(promotion_id)

    # ============================================
    # Statistics
    # ============================================

    def get_statistics(self) -> HubStatistics:
        """Get comprehensive hub statistics."""
        total_namespaces = len(self.namespaces)
        total_skills = len(self.skills)
        public_skills = sum(1 for s in self.skills.values() 
                           if s.visibility == SkillVisibility.PUBLIC)
        total_versions = len(self.versions)
        total_downloads = sum(s.download_count for s in self.skills.values())
        total_stars = sum(s.star_count for s in self.skills.values())
        pending_reviews = sum(1 for rt in self.review_tasks.values() 
                             if rt.status == ReviewStatus.PENDING)
        
        category_counts: Dict[str, int] = {}
        for s in self.skills.values():
            if s.visibility == SkillVisibility.PUBLIC:
                category_counts[s.category] = category_counts.get(s.category, 0) + 1
        
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return HubStatistics(
            total_namespaces=total_namespaces,
            total_skills=total_skills,
            public_skills=public_skills,
            total_versions=total_versions,
            total_downloads=total_downloads,
            total_stars=total_stars,
            pending_reviews=pending_reviews,
            top_categories=top_categories,
        )

    # ============================================
    # Audit Log
    # ============================================

    def get_audit_logs(self, target_type: Optional[str] = None,
                      target_id: Optional[str] = None,
                      limit: int = 100) -> List[AuditLog]:
        """Get audit logs with filters."""
        results = self.audit_logs
        
        if target_type:
            results = [log for log in results if log.target_type == target_type]
        
        if target_id:
            results = [log for log in results if log.target_id == target_id]
        
        results.sort(key=lambda log: log.created_at, reverse=True)
        return results[:limit]

    # ============================================
    # Persistence Functions
    # ============================================

    def _save_namespaces(self):
        """Save namespaces to disk."""
        data = {
            ns_id: ns.model_dump() for ns_id, ns in self.namespaces.items()
        }
        file = self.storage_dir / "namespaces.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_skills(self):
        """Save skills to disk."""
        data = {
            skill_id: skill.model_dump() for skill_id, skill in self.skills.items()
        }
        file = self.storage_dir / "skills.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_versions(self):
        """Save versions to disk."""
        data = {
            vid: v.model_dump() for vid, v in self.versions.items()
        }
        file = self.storage_dir / "versions.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_review_tasks(self):
        """Save review tasks to disk."""
        data = {
            rtid: rt.model_dump() for rtid, rt in self.review_tasks.items()
        }
        file = self.storage_dir / "reviews.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_promotion_requests(self):
        """Save promotion requests to disk."""
        data = {
            prid: pr.model_dump() for prid, pr in self.promotion_requests.items()
        }
        file = self.storage_dir / "promotions.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_stars(self):
        """Save stars to disk."""
        data = {
            key: star.model_dump() for key, star in self.stars.items()
        }
        file = self.storage_dir / "stars.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_ratings(self):
        """Save ratings to disk."""
        data = {
            key: rating.model_dump() for key, rating in self.ratings.items()
        }
        file = self.storage_dir / "ratings.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _save_audit_logs(self):
        """Save audit logs to disk."""
        data = [log.model_dump() for log in self.audit_logs]
        file = self.storage_dir / "audit_logs.json"
        with open(file, "w") as f:
            json.dump(data, f, default=str)

    def _load_data(self):
        """Load all data from disk."""
        # Load namespaces
        file = self.storage_dir / "namespaces.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for ns_id, ns_data in data.items():
                try:
                    ns = Namespace.model_validate(ns_data)
                    self.namespaces[ns_id] = ns
                except Exception as e:
                    print(f"Failed to load namespace {ns_id}: {e}")
        
        # Load skills
        file = self.storage_dir / "skills.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for skill_id, skill_data in data.items():
                try:
                    skill = Skill.model_validate(skill_data)
                    self.skills[skill_id] = skill
                except Exception as e:
                    print(f"Failed to load skill {skill_id}: {e}")
        
        # Load versions
        file = self.storage_dir / "versions.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for vid, v_data in data.items():
                try:
                    v = SkillVersion.model_validate(v_data)
                    self.versions[vid] = v
                except Exception as e:
                    print(f"Failed to load version {vid}: {e}")
        
        # Load review tasks
        file = self.storage_dir / "reviews.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for rtid, rt_data in data.items():
                try:
                    rt = ReviewTask.model_validate(rt_data)
                    self.review_tasks[rtid] = rt
                except Exception as e:
                    print(f"Failed to load review {rtid}: {e}")
        
        # Load promotion requests
        file = self.storage_dir / "promotions.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for prid, pr_data in data.items():
                try:
                    pr = PromotionRequest.model_validate(pr_data)
                    self.promotion_requests[prid] = pr
                except Exception as e:
                    print(f"Failed to load promotion {prid}: {e}")
        
        # Load stars
        file = self.storage_dir / "stars.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for key, star_data in data.items():
                try:
                    star = SkillStar.model_validate(star_data)
                    self.stars[key] = star
                except Exception as e:
                    print(f"Failed to load star {key}: {e}")
        
        # Load ratings
        file = self.storage_dir / "ratings.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for key, rating_data in data.items():
                try:
                    rating = SkillRating.model_validate(rating_data)
                    self.ratings[key] = rating
                except Exception as e:
                    print(f"Failed to load rating {key}: {e}")
        
        # Load audit logs
        file = self.storage_dir / "audit_logs.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
            for log_data in data:
                try:
                    log = AuditLog.model_validate(log_data)
                    self.audit_logs.append(log)
                except Exception as e:
                    print(f"Failed to load audit log: {e}")


HubManager = SkillsHubManager  # Alias for backward compatibility
