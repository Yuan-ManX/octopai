"""
Version Control - Manages skill variant versions and checkpoints.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, List
from dataclasses import dataclass, field

from .config import SkillVariant


@dataclass
class VersionInfo:
    """Information about a specific version.

    Attributes:
        version_id: Unique version identifier
        variant_name: Name of the skill variant
        content_hash: Hash of the content for integrity checking
        timestamp: When this version was created
        parent_version: Parent version ID (None for initial)
        generation: Generation number
        score: Score at this version
        metadata: Additional version metadata
        file_path: Path to stored version file (if saved to disk)
    """

    version_id: str = ""
    variant_name: str = ""
    content_hash: str = ""
    timestamp: Optional[str] = None
    parent_version: Optional[str] = None
    generation: int = 0
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    file_path: Optional[Path] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class Checkpoint:
    """Checkpoint state for resuming evolution.

    Attributes:
        iteration: Current iteration number
        best_variant_name: Name of best variant so far
        best_score: Best score achieved
        frontier_state: State of the frontier
        feedback_entries_count: Number of feedback entries
        total_cost_usd: Total cost incurred
        mutations_applied: Total mutations applied
        timestamp: When checkpoint was created
    """

    iteration: int = 0
    best_variant_name: str = ""
    best_score: float = 0.0
    frontier_state: dict = field(default_factory=dict)
    feedback_entries_count: int = 0
    total_cost_usd: float = 0.0
    mutations_applied: int = 0
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class VersionManager:
    """Manages versioning for skill variants during evolution.

    Provides:
    - Content hashing for integrity
    - Version history tracking
    - Checkpoint/resume functionality
    - Storage and retrieval of versions
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize version manager.

        Args:
            storage_dir: Directory to store version files
        """
        self.storage_dir = storage_dir or Path(".octopai/versions")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.versions: dict[str, VersionInfo] = {}
        self.version_history: List[str] = []
        self._load_index()

    def create_version(self, variant: SkillVariant) -> VersionInfo:
        """Create a new version from a skill variant.

        Args:
            variant: Skill variant to version

        Returns:
            VersionInfo for the new version
        """
        content_hash = self._hash_content(variant.content)
        version_id = self._generate_version_id(variant.name, variant.generation)

        version_info = VersionInfo(
            version_id=version_id,
            variant_name=variant.name,
            content_hash=content_hash,
            parent_version=self.version_history[-1] if self.version_history else None,
            generation=variant.generation,
            score=variant.score,
            metadata={
                "mutations": variant.mutations,
                "parent": variant.parent,
            },
        )

        self.versions[version_id] = version_info
        self.version_history.append(version_id)

        self._save_version(variant, version_info)
        self._update_index()

        return version_info

    def get_version(self, version_id: str) -> Optional[SkillVariant]:
        """Retrieve a specific version.

        Args:
            version_id: Version identifier

        Returns:
            SkillVariant or None if not found
        """
        version_info = self.versions.get(version_id)
        if not version_info:
            return None

        return self._load_version(version_info)

    def get_latest_version(self) -> Optional[SkillVariant]:
        """Get the most recent version.

        Returns:
            Latest SkillVariant or None if no versions exist
        """
        if not self.version_history:
            return None

        latest_id = self.version_history[-1]
        return self.get_version(latest_id)

    def get_best_version(self) -> Optional[SkillVariant]:
        """Get the highest-scoring version.

        Returns:
            Best-scoring SkillVariant or None if no versions exist
        """
        if not self.versions:
            return None

        best_info = max(
            self.versions.values(),
            key=lambda v: v.score,
        )
        return self.get_version(best_info.version_id)

    def get_version_history(self, limit: int = 20) -> List[VersionInfo]:
        """Get recent version history.

        Args:
            limit: Maximum number of versions to return

        Returns:
            List of VersionInfo objects (most recent first)
        """
        recent_ids = self.version_history[-limit:]
        return [self.versions[vid] for vid in reversed(recent_ids) if vid in self.versions]

    def restore_to_version(self, version_id: str) -> bool:
        """Restore state to a specific version (for rollback).

        Args:
            version_id: Version to restore to

        Returns:
            True if successful, False otherwise
        """
        if version_id not in self.versions:
            return False

        current_history = list(self.version_history)
        target_index = current_history.index(version_id)

        self.version_history = current_history[:target_index + 1]

        removed_versions = set(current_history[target_index + 1:]) - set(self.version_history)
        for vid in removed_versions:
            if vid in self.versions:
                del self.versions[vid]

        self._update_index()
        return True

    def create_checkpoint(
        self,
        iteration: int,
        frontier_manager=None,
        feedback_history=None,
        total_cost: float = 0.0,
        mutations_count: int = 0,
    ) -> Checkpoint:
        """Create a checkpoint for resuming evolution later.

        Args:
            iteration: Current iteration number
            frontier_manager: FrontierManager instance (optional)
            feedback_history: FeedbackHistory instance (optional)
            total_cost: Total cost incurred so far
            mutations_count: Total mutations applied

        Returns:
            Checkpoint object with current state
        """
        checkpoint = Checkpoint(
            iteration=iteration,
            best_variant_name="",
            best_score=0.0,
            frontier_state={},
            feedback_entries_count=len(feedback_history.entries) if feedback_history else 0,
            total_cost_usd=total_cost,
            mutations_applied=mutations_count,
        )

        if frontier_manager:
            best = frontier_manager.get_best()
            if best:
                checkpoint.best_variant_name = best.name
                checkpoint.best_score = best.score
            checkpoint.frontier_state = {
                name: v.score
                for name, v in frontier_manager.variants.items()
            }

        checkpoint_path = self.storage_dir / "checkpoint.json"
        with open(checkpoint_path, 'w') as f:
            json.dump({
                "iteration": checkpoint.iteration,
                "best_variant_name": checkpoint.best_variant_name,
                "best_score": checkpoint.best_score,
                "frontier_state": checkpoint.frontier_state,
                "feedback_entries_count": checkpoint.feedback_entries_count,
                "total_cost_usd": checkpoint.total_cost_usd,
                "mutations_applied": checkpoint.mutations_applied,
                "timestamp": checkpoint.timestamp,
            }, f, indent=2)

        return checkpoint

    def load_checkpoint(self) -> Optional[Checkpoint]:
        """Load the most recent checkpoint.

        Returns:
            Checkpoint object or None if no checkpoint exists
        """
        checkpoint_path = self.storage_dir / "checkpoint.json"

        if not checkpoint_path.exists():
            return None

        try:
            with open(checkpoint_path, 'r') as f:
                data = json.load(f)

            return Checkpoint(**data)
        except Exception as e:
            print(f"Failed to load checkpoint: {e}")
            return None

    def delete_checkpoint(self) -> bool:
        """Delete existing checkpoint.

        Returns:
            True if deleted, False otherwise
        """
        checkpoint_path = self.storage_dir / "checkpoint.json"

        if checkpoint_path.exists():
            checkpoint_path.unlink()
            return True

        return False

    def get_statistics(self) -> dict:
        """Get statistics about version history.

        Returns:
            Dictionary with version statistics
        """
        if not self.versions:
            return {
                "total_versions": 0,
                "generations": [],
                "score_range": (0.0, 0.0),
                "storage_size_mb": 0.0,
            }

        scores = [v.score for v in self.versions.values()]
        generations = [v.generation for v in self.versions.values()]

        storage_size = sum(
            f.stat().st_size
            for f in self.storage_dir.glob("*.json")
            if f.is_file()
        )
        storage_size_mb = storage_size / (1024 * 1024)

        return {
            "total_versions": len(self.versions),
            "generations": sorted(set(generations)),
            "score_range": (min(scores), max(scores)) if scores else (0.0, 0.0),
            "storage_size_mb": round(storage_size_mb, 2),
        }

    def cleanup_old_versions(self, keep_recent: int = 50) -> int:
        """Remove old versions to save space.

        Args:
            keep_recent: Number of recent versions to keep

        Returns:
            Number of versions removed
        """
        if len(self.version_history) <= keep_recent:
            return 0

        versions_to_remove = self.version_history[:-keep_recent]
        removed_count = 0

        for version_id in versions_to_remove:
            version_info = self.versions.get(version_id)
            if version_info and version_info.file_path and version_info.file_path.exists():
                version_info.file_path.unlink()
                removed_count += 1

            if version_id in self.versions:
                del self.versions[version_id]

        self.version_history = self.version_history[-keep_recent:]
        self._update_index()

        return removed_count

    def _hash_content(self, content: str) -> str:
        """Generate hash of content for integrity checking."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _generate_version_id(self, name: str, generation: int) -> str:
        """Generate unique version ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        clean_name = name.lower().replace(" ", "-")[:20]
        return f"{clean_name}-gen{generation}-{timestamp}"

    def _save_version(self, variant: SkillVariant, version_info: VersionInfo) -> None:
        """Save version to disk."""
        filename = f"{version_info.version_id}.json"
        filepath = self.storage_dir / filename

        data = {
            "name": variant.name,
            "content": variant.content,
            "score": variant.score,
            "generation": variant.generation,
            "parent": variant.parent,
            "mutations": variant.mutations,
            "metadata": variant.metadata,
            "version_info": {
                "version_id": version_info.version_id,
                "content_hash": version_info.content_hash,
                "timestamp": version_info.timestamp,
            },
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        version_info.file_path = filepath

    def _load_version(self, version_info: VersionInfo) -> Optional[SkillVariant]:
        """Load version from disk."""
        if not version_info.file_path or not version_info.file_path.exists():
            return None

        try:
            with open(version_info.file_path, 'r') as f:
                data = json.load(f)

            return SkillVariant(
                name=data["name"],
                content=data["content"],
                score=data.get("score", 0.0),
                generation=data.get("generation", 0),
                parent=data.get("parent"),
                mutations=data.get("mutations", []),
                metadata=data.get("metadata", {}),
            )
        except Exception as e:
            print(f"Failed to load version {version_info.version_id}: {e}")
            return None

    def _update_index(self) -> None:
        """Update version index file."""
        index_path = self.storage_dir / "index.json"

        index_data = {
            "total_versions": len(self.versions),
            "version_order": self.version_history,
            "last_updated": datetime.now().isoformat(),
        }

        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)

    def _load_index(self) -> None:
        """Load version index from disk."""
        index_path = self.storage_dir / "index.json"

        if not index_path.exists():
            return

        try:
            with open(index_path, 'r') as f:
                index_data = json.load(f)

            self.version_history = index_data.get("version_order", [])
        except Exception as e:
            print(f"Failed to load version index: {e}")
            self.version_history = []

    def __len__(self) -> int:
        """Return total number of versions."""
        return len(self.versions)
