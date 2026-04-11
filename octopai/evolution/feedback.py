"""
Feedback History - Tracks and manages feedback from evolution iterations.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List
from dataclasses import dataclass, field, asdict


@dataclass
class FeedbackEntry:
    """Single feedback entry from an evolution iteration.

    Attributes:
        iteration: Iteration number when this feedback was recorded
        variant_name: Name of the variant that was evaluated
        proposal: Description of the proposed mutation
        justification: Rationale for the mutation
        outcome: Result of applying this mutation ("improved" or "discarded")
        score: Score achieved by the variant
        parent_score: Score of the parent variant
        active_skills: List of skills active at this point
        timestamp: When this entry was created
        metadata: Additional information about this feedback
    """

    iteration: int = 0
    variant_name: str = ""
    proposal: str = ""
    justification: str = ""
    outcome: str = ""
    score: float = 0.0
    parent_score: float = 0.0
    active_skills: List[str] = field(default_factory=list)
    timestamp: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'FeedbackEntry':
        """Create from dictionary."""
        return cls(**data)


class FeedbackHistory:
    """Manages feedback history for the evolution loop.

    Tracks all mutations and their outcomes to inform future proposals
    and prevent repeating unsuccessful changes.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize feedback history.

        Args:
            storage_path: Path to store feedback history file
        """
        self.storage_path = storage_path or Path(".octopai/feedback_history.json")
        self.entries: List[FeedbackEntry] = []
        self._load()

    def add(self, entry: FeedbackEntry) -> None:
        """Add a new feedback entry.

        Args:
            entry: Feedback entry to add
        """
        self.entries.append(entry)
        self._save()

    def append_feedback(
        self,
        variant_name: str,
        proposal: str,
        justification: str,
        outcome: str,
        score: float,
        parent_score: float,
        active_skills: List[str],
        iteration: int = 0,
        metadata: dict = None,
    ) -> None:
        """Convenience method to add feedback with all parameters.

        Args:
            variant_name: Name of the evaluated variant
            proposal: Proposed mutation description
            justification: Rationale for the mutation
            outcome: Outcome ("improved" or "discarded")
            score: Achieved score
            parent_score: Parent's score
            active_skills: Active skills at this point
            iteration: Current iteration number
            metadata: Additional metadata
        """
        entry = FeedbackEntry(
            iteration=iteration,
            variant_name=variant_name,
            proposal=proposal,
            justification=justification,
            outcome=outcome,
            score=score,
            parent_score=parent_score,
            active_skills=active_skills,
            metadata=metadata or {},
        )
        self.add(entry)

    def get_recent(self, count: int = 10) -> List[FeedbackEntry]:
        """Get most recent feedback entries.

        Args:
            count: Number of entries to return

        Returns:
            List of recent FeedbackEntry objects
        """
        return self.entries[-count:] if self.entries else []

    def get_by_outcome(self, outcome: str) -> List[FeedbackEntry]:
        """Get entries filtered by outcome.

        Args:
            outcome: Outcome to filter by ("improved" or "discarded")

        Returns:
            List of matching FeedbackEntry objects
        """
        return [e for e in self.entries if e.outcome == outcome]

    def get_successful_mutations(self):
        """Get all successful (improved) mutations."""
        return self.get_by_outcome("improved")

    def get_failed_mutations(self):
        """Get all failed (discarded) mutations."""
        return self.get_by_outcome("discarded")

    def get_improvement_rate(self) -> float:
        """Calculate overall improvement rate.

        Returns:
            Fraction of mutations that improved (0.0 to 1.0)
        """
        if not self.entries:
            return 0.0

        successful = len(self.get_successful_mutations())
        return successful / len(self.entries)

    def get_average_score_change(self) -> float:
        """Calculate average score change from mutations.

        Returns:
            Average difference between child and parent scores
        """
        if not self.entries:
            return 0.0

        total_change = sum(e.score - e.parent_score for e in self.entries)
        return total_change / len(self.entries)

    def find_repeated_proposals(self, threshold: int = 2) -> List[dict]:
        """Find proposals that have been tried multiple times.

        Args:
            threshold: Minimum occurrences to flag

        Returns:
            List of dictionaries with proposal info and counts
        """
        from collections import Counter

        proposal_counts = Counter(e.proposal for e in self.entries)
        repeated = [
            {"proposal": proposal, "count": count}
            for proposal, count in proposal_counts.items()
            if count >= threshold
        ]

        return sorted(repeated, key=lambda x: x["count"], reverse=True)

    def should_avoid_proposal(self, proposal: str, max_attempts: int = 3) -> bool:
        """Check if a proposal has been attempted too many times without success.

        Args:
            proposal: Proposal string to check
            max_attempts: Maximum attempts before avoiding

        Returns:
            True if this proposal should be avoided
        """
        related_entries = [e for e in self.entries if e.proposal == proposal]

        if len(related_entries) < max_attempts:
            return False

        failed_count = sum(1 for e in related_entries if e.outcome == "discarded")
        return failed_count >= max_attempts

    def get_summary(self) -> dict:
        """Get comprehensive summary of feedback history.

        Returns:
            Dictionary with statistics and insights
        """
        if not self.entries:
            return {
                "total_entries": 0,
                "improvement_rate": 0.0,
                "average_score_change": 0.0,
                "recent_trend": "stable",
                "recommendations": [],
            }

        recent = self.get_recent(10)
        recent_improvements = sum(1 for e in recent if e.outcome == "improved")
        recent_rate = recent_improvements / len(recent)

        if recent_rate > 0.7:
            trend = "improving"
        elif recent_rate < 0.3:
            trend = "declining"
        else:
            trend = "stable"

        repeated = self.find_repeated_proposals()
        recommendations = []

        if repeated:
            recommendations.append(f"Avoid repeated proposals: {repeated[0]['proposal']}")

        if self.get_improvement_rate() < 0.3 and len(self.entries) > 5:
            recommendations.append("Consider adjusting mutation strategy - low success rate")

        if trend == "declining":
            recommendations.append("Recent performance declining - review approach")

        return {
            "total_entries": len(self.entries),
            "improvement_rate": self.get_improvement_rate(),
            "average_score_change": self.get_average_score_change(),
            "recent_trend": trend,
            "repeated_proposals": repeated[:5],
            "recommendations": recommendations,
        }

    def export_to_markdown(self) -> str:
        """Export feedback history as markdown report.

        Returns:
            Markdown formatted string
        """
        lines = [
            "# Evolution Feedback History",
            "",
            f"**Total Entries:** {len(self.entries)}",
            f"**Improvement Rate:** {self.get_improvement_rate():.1%}",
            f"**Avg Score Change:** {self.get_average_score_change():+.4f}",
            "",
            "## Recent Entries",
            "",
        ]

        for entry in self.get_recent(20):
            status = "✅" if entry.outcome == "improved" else "❌"
            lines.append(f"### Iteration {entry.iteration} - {entry.variant_name} {status}")
            lines.append(f"- **Score:** {entry.score:.4f} (parent: {entry.parent_score:.4f})")
            lines.append(f"- **Proposal:** {entry.proposal[:100]}...")
            lines.append(f"- **Outcome:** {entry.outcome}")
            lines.append("")

        summary = self.get_summary()
        lines.extend([
            "## Summary",
            "",
            f"- **Trend:** {summary['recent_trend']}",
            "- **Recommendations:**",
        ])

        for rec in summary.get("recommendations", []):
            lines.append(f"  - {rec}")

        return "\n".join(lines)

    def clear(self) -> None:
        """Clear all feedback entries."""
        self.entries.clear()
        self._save()

    def _save(self) -> None:
        """Save feedback history to file."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = [e.to_dict() for e in self.entries]
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save feedback history: {e}")

    def _load(self) -> None:
        """Load feedback history from file."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            self.entries = [FeedbackEntry.from_dict(e) for e in data]
        except Exception as e:
            print(f"Failed to load feedback history: {e}")
            self.entries = []

    def __len__(self) -> int:
        """Return number of entries."""
        return len(self.entries)

    def __iter__(self):
        """Iterate over entries."""
        return iter(self.entries)
