"""
Skills Hub - GitHub-like skill repository management system.

Features:
- Public and private skill repositories
- Version control and publishing workflow
- Skill discovery and search
- User collaboration (fork, star, contribute)
- Skill marketplace with ratings and reviews
"""

from .hub import (
    SkillRepository,
    RepositoryVisibility,
    RepositoryStatus,
    SkillVersion,
    RepositoryEvent,
    ForkRecord,
)
from .manager import (
    HubManager,
    SkillsHubManager,
    PublishRequest,
    SearchResult,
    HubStatistics,
)
from .permissions import PermissionManager, Role, Permission
from .marketplace import MarketplaceManager, Rating, Review
from .collaboration import (
    CollaborationManager,
    PullRequest,
    Issue,
    Comment,
    ActivityItem,
    ReviewRequest,
    PRStatus,
    IssueType,
    IssueStatus,
)

__all__ = [
    "SkillRepository",
    "RepositoryVisibility",
    "RepositoryStatus",
    "SkillVersion",
    "RepositoryEvent",
    "ForkRecord",
    "HubManager",
    "SkillsHubManager",
    "PublishRequest",
    "SearchResult",
    "HubStatistics",
    "PermissionManager",
    "Role",
    "Permission",
    "MarketplaceManager",
    "Rating",
    "Review",
    "CollaborationManager",
    "PullRequest",
    "Issue",
    "Comment",
    "ActivityItem",
    "ReviewRequest",
    "PRStatus",
    "IssueType",
    "IssueStatus",
]
