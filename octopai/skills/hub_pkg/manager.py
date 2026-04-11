"""
Hub Manager - Core management operations for Skills Hub.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, List, Dict, Tuple
from dataclasses import dataclass

from .hub import (
    SkillRepository,
    RepositoryVisibility,
    RepositoryStatus,
    SkillVersion,
    ForkRecord,
)


@dataclass
class PublishRequest:
    """Request to publish a repository.

    Attributes:
        repo_id: Repository ID to publish
        version: Version string to publish
        release_notes: Notes for this release
        changelog: Detailed changelog
        notify_followers: Whether to send notifications
    """

    repo_id: str = ""
    version: str = ""
    release_notes: str = ""
    changelog: str = ""
    notify_followers: bool = True


@dataclass
class SearchResult:
    """Result from a search operation.

    Attributes:
        repositories: Matching repositories
        total_count: Total number of matches (for pagination)
        query: Original search query
        filters_applied: Filters that were applied
        search_time_ms: Time taken for search in milliseconds
    """

    repositories: List[SkillRepository] = None
    total_count: int = 0
    query: str = ""
    filters_applied: Dict[str, Any] = None
    search_time_ms: float = 0.0

    def __post_init__(self):
        if self.repositories is None:
            self.repositories = []
        if self.filters_applied is None:
            self.filters_applied = {}


@dataclass
class HubStatistics:
    """Aggregated statistics for the entire hub.

    Attributes:
        total_repositories: Total number of repositories
        public_repositories: Number of public repos
        private_repositories: Number of private repos
        published_repositories: Number of published repos
        total_versions: Total versions across all repos
        total_downloads: Total downloads across all skills
        total_stars: Total stars across all repos
        top_categories: Most popular categories
        recent_activity: Recent activity count
    """

    total_repositories: int = 0
    public_repositories: int = 0
    private_repositories: int = 0
    published_repositories: int = 0
    total_versions: int = 0
    total_downloads: int = 0
    total_stars: int = 0
    top_categories: List[Tuple[str, int]] = None
    recent_activity: int = 0

    def __post_init__(self):
        if self.top_categories is None:
            self.top_categories = []


class HubManager:
    """Main manager for Skills Hub operations.

    Provides complete CRUD operations for skill repositories,
    search and discovery, publishing workflow, and statistics.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize Hub Manager.

        Args:
            storage_dir: Directory to store repository data
        """
        self.storage_dir = storage_dir or Path(".octopai/skills-hub")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.repositories: Dict[str, SkillRepository] = {}
        self.forks: List[ForkRecord] = []

        self._load_repositories()

    def create_repository(
        self,
        name: str,
        owner: str,
        description: str = "",
        visibility: RepositoryVisibility = RepositoryVisibility.PRIVATE,
        **kwargs,
    ) -> SkillRepository:
        """Create a new skill repository.

        Args:
            name: Repository name (will be slugified)
            owner: Owner username
            description: Short description
            visibility: Visibility setting (enum or string value)
            **kwargs: Additional fields for SkillRepository

        Returns:
            Created SkillRepository object

        Raises:
            ValueError: If name is invalid or already exists
        """
        if isinstance(visibility, str):
            try:
                visibility = RepositoryVisibility(visibility)
            except ValueError:
                visibility = RepositoryVisibility.PRIVATE

        slug = self._slugify(name)

        if not slug:
            raise ValueError("Invalid repository name")

        if slug in self.repositories:
            raise ValueError(f"Repository '{slug}' already exists")

        repo_id = f"{owner}/{slug}"

        repo = SkillRepository(
            id=repo_id,
            name=slug,
            display_name=name,
            description=description,
            owner=owner,
            visibility=visibility,
            status=RepositoryStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **kwargs,
        )

        initial_version = SkillVersion(
            version="1.0.0",
            content="",
            created_by=owner,
            is_latest=True,
        )
        repo.versions.append(initial_version)

        self.repositories[repo_id] = repo
        self._save_repository(repo)

        return repo

    def get_repository(self, repo_id: str) -> Optional[SkillRepository]:
        """Get a repository by ID.

        Args:
            repo_id: Repository identifier (owner/name format)

        Returns:
            SkillRepository or None if not found
        """
        return self.repositories.get(repo_id)

    def update_repository(
        self,
        repo_id: str,
        **updates,
    ) -> Optional[SkillRepository]:
        """Update repository metadata.

        Args:
            repo_id: Repository ID
            **updates: Fields to update

        Returns:
            Updated repository or None if not found
        """
        repo = self.repositories.get(repo_id)
        if not repo:
            return None

        for key, value in updates.items():
            if hasattr(repo, key):
                setattr(repo, key, value)

        repo.updated_at = datetime.now()
        self._save_repository(repo)

        return repo

    def delete_repository(self, repo_id: str) -> bool:
        """Delete a repository.

        Args:
            repo_id: Repository ID to delete

        Returns:
            True if deleted, False if not found
        """
        if repo_id not in self.repositories:
            return False

        del self.repositories[repo_id]

        repo_path = self._get_repo_path(repo_id)
        if repo_path.exists():
            repo_path.unlink()

        return True

    def list_repositories(
        self,
        owner: Optional[str] = None,
        visibility: Optional[RepositoryVisibility] = None,
        status: Optional[RepositoryStatus] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
    ) -> List[SkillRepository]:
        """List repositories with filtering and pagination.

        Args:
            owner: Filter by owner
            visibility: Filter by visibility
            status: Filter by status
            category: Filter by category
            tag: Filter by tag
            limit: Max results to return
            offset: Offset for pagination
            sort_by: Field to sort by
            sort_order: Sort direction (asc/desc)

        Returns:
            List of matching SkillRepository objects
        """
        results = list(self.repositories.values())

        if owner:
            results = [r for r in results if r.owner == owner]

        if visibility:
            results = [r for r in results if r.visibility == visibility]

        if status:
            results = [r for r in results if r.status == status]

        if category:
            results = [r for r in results if r.category == category]

        if tag:
            results = [r for r in results if tag in r.tags]

        reverse = sort_order.lower() == "desc"
        results.sort(key=lambda r: getattr(r, sort_by, ""), reverse=reverse)

        return results[offset:offset + limit]

    def search(
        self,
        query: str = "",
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        visibility: Optional[RepositoryVisibility] = RepositoryVisibility.PUBLIC,
        limit: int = 20,
    ) -> SearchResult:
        """Search repositories.

        Args:
            query: Search query (searches name, description, tags)
            categories: Filter by categories
            tags: Filter by tags
            visibility: Visibility filter (default: PUBLIC only)
            limit: Max results

        Returns:
            SearchResult with matching repositories
        """
        import time
        start_time = time.time()

        results = list(self.repositories.values())

        if visibility:
            results = [r for r in results if r.visibility == visibility]

        if query:
            query_lower = query.lower()
            results = [
                r for r in results
                if query_lower in r.name.lower()
                or query_lower in r.description.lower()
                or query_lower in r.display_name.lower()
                or any(query_lower in t.lower() for t in r.tags)
                or any(query_lower in topic.lower() for topic in r.topics)
            ]

        if categories:
            results = [r for r in results if r.category in categories]

        if tags:
            results = [r for r in results if any(t in r.tags for t in tags)]

        search_time = (time.time() - start_time) * 1000

        return SearchResult(
            repositories=results[:limit],
            total_count=len(results),
            query=query,
            filters_applied={
                "categories": categories,
                "tags": tags,
                "visibility": visibility.value if visibility else None,
            },
            search_time_ms=search_time,
        )

    def publish_repository(
        self,
        request: PublishRequest,
    ) -> Optional[SkillRepository]:
        """Publish a repository to make it publicly available.

        Args:
            request: Publish request with details

        Returns:
            Published repository or None if failed
        """
        repo = self.repositories.get(request.repo_id)
        if not repo:
            return None

        if repo.status == RepositoryStatus.PUBLISHED:
            return repo

        new_version = SkillVersion(
            version=request.version or self._increment_version(repo.current_version),
            content=self._get_latest_content(repo),
            changelog=request.changelog,
            release_notes=request.release_notes,
            created_by=repo.owner,
            is_latest=True,
        )

        for v in repo.versions:
            v.is_latest = False

        repo.versions.append(new_version)
        repo.current_version = new_version.version
        repo.status = RepositoryStatus.PUBLISHED
        repo.published_at = datetime.now()
        repo.updated_at = datetime.now()

        self._save_repository(repo)

        return repo

    def fork_repository(
        self,
        source_repo_id: str,
        fork_owner: str,
        fork_name: Optional[str] = None,
    ) -> Optional[SkillRepository]:
        """Fork a repository.

        Args:
            source_repo_id: Source repository to fork
            fork_owner: Owner of the new fork
            fork_name: Name for the fork (defaults to source name)

        Returns:
            New forked repository or None if failed
        """
        source = self.repositories.get(source_repo_id)
        if not source:
            return None

        fork_name = fork_name or source.name

        try:
            fork_repo = self.create_repository(
                name=fork_name,
                owner=fork_owner,
                description=f"Forked from {source.id}",
                visibility=RepositoryVisibility.PRIVATE,
                category=source.category,
                tags=list(source.tags),
                language=source.language,
                license=source.license,
            )

            source_content = self._get_latest_content(source)
            self.update_version(fork_repo.id, source_content)

            source.forks += 1
            self._save_repository(source)

            fork_record = ForkRecord(
                source_repo_id=source_repo_id,
                forked_repo_id=fork_repo.id,
                forked_by=fork_owner,
            )
            self.forks.append(fork_record)

            return fork_repo

        except ValueError:
            return None

    def star_repository(self, repo_id: str, user_id: str) -> bool:
        """Star/favorite a repository.

        Args:
            repo_id: Repository to star
            user_id: User starring

        Returns:
            True if starred successfully
        """
        repo = self.repositories.get(repo_id)
        if not repo:
            return False

        repo.stars += 1
        self._save_repository(repo)

        return True

    def watch_repository(self, repo_id: str, user_id: str) -> bool:
        """Watch a repository for updates.

        Args:
            repo_id: Repository to watch
            user_id: User watching

        Returns:
            True if watching started
        """
        repo = self.repositories.get(repo_id)
        if not repo:
            return False

        repo.watchers += 1
        self._save_repository(repo)

        return True

    def get_popular_repositories(self, limit: int = 10) -> List[SkillRepository]:
        """Get most popular repositories by stars.

        Args:
            limit: Number to return

        Returns:
            List of popular repositories sorted by stars
        """
        all_public = self.list_repositories(visibility=RepositoryVisibility.PUBLIC)
        sorted_repos = sorted(all_public, key=lambda r: r.stars, reverse=True)
        return sorted_repos[:limit]

    def get_recently_updated(self, limit: int = 10) -> List[SkillRepository]:
        """Get recently updated repositories.

        Args:
            limit: Number to return

        Returns:
            List of recently updated repositories
        """
        all_public = self.list_repositories(visibility=RepositoryVisibility.PUBLIC)
        sorted_repos = sorted(all_public, key=lambda r: r.updated_at, reverse=True)
        return sorted_repos[:limit]

    def get_statistics(self) -> HubStatistics:
        """Get comprehensive hub statistics.

        Returns:
            HubStatistics object with aggregated data
        """
        repos = list(self.repositories.values())

        public_count = sum(1 for r in repos if r.visibility == RepositoryVisibility.PUBLIC)
        private_count = sum(1 for r in repos if r.visibility == RepositoryVisibility.PRIVATE)
        published_count = sum(1 for r in repos if r.status == RepositoryStatus.PUBLISHED)

        total_versions = sum(len(r.versions) for r in repos)
        total_downloads = sum(v.download_count for r in repos for v in r.versions)
        total_stars = sum(r.stars for r in repos)

        category_counts: Dict[str, int] = {}
        for r in repos:
            if r.visibility == RepositoryVisibility.PUBLIC:
                category_counts[r.category] = category_counts.get(r.category, 0) + 1

        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return HubStatistics(
            total_repositories=len(repos),
            public_repositories=public_count,
            private_repositories=private_count,
            published_repositories=published_count,
            total_versions=total_versions,
            total_downloads=total_downloads,
            total_stars=total_stars,
            top_categories=top_categories,
        )

    def update_version(
        self,
        repo_id: str,
        content: str,
        version: Optional[str] = None,
        changelog: str = "",
    ) -> Optional[SkillVersion]:
        """Update/create a new version of a repository's skill.

        Args:
            repo_id: Repository ID
            content: New skill content
            version: Version string (auto-incremented if None)
            changelog: Changelog for this version

        Returns:
            New SkillVersion or None if failed
        """
        repo = self.repositories.get(repo_id)
        if not repo:
            return None

        new_version_str = version or self._increment_version(repo.current_version)

        new_version = SkillVersion(
            version=new_version_str,
            content=content,
            changelog=changelog,
            created_by=repo.owner,
            is_latest=True,
        )

        for v in repo.versions:
            v.is_latest = False

        repo.versions.append(new_version)
        repo.current_version = new_version_str
        repo.updated_at = datetime.now()

        self._save_repository(repo)

        return new_version

    def _slugify(self, name: str) -> str:
        """Convert name to URL-safe slug."""
        slug = name.lower().strip()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')

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

    def _get_latest_content(self, repo: SkillRepository) -> str:
        """Get content from latest version."""
        for v in reversed(repo.versions):
            if v.is_latest and v.content:
                return v.content
        return ""

    def _get_repo_path(self, repo_id: str) -> Path:
        """Get file path for repository storage."""
        safe_name = repo_id.replace('/', '_')
        return self.storage_dir / f"{safe_name}.json"

    def _save_repository(self, repo: SkillRepository) -> None:
        """Save repository to disk."""
        path = self._get_repo_path(repo.id)
        with open(path, 'w') as f:
            json.dump(repo.model_dump(), f, indent=2, default=str)

    def _load_repositories(self) -> None:
        """Load all repositories from disk."""
        if not self.storage_dir.exists():
            return

        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                repo = SkillRepository.model_validate(data)
                self.repositories[repo.id] = repo
            except Exception as e:
                print(f"Failed to load repository {file_path}: {e}")

    def __len__(self) -> int:
        """Return total number of repositories."""
        return len(self.repositories)
