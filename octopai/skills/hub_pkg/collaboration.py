"""
Collaboration Manager - GitHub-style collaboration features for Skills Hub.

Provides:
- Pull Request (PR) workflow
- Issue tracking
- Discussion/Comment system
- Change review
- Contribution guidelines
- Activity feed
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class PRStatus(str, Enum):
    """Pull Request status."""
    OPEN = "open"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    MERGED = "merged"
    CLOSED = "closed"


class IssueType(str, Enum):
    """Issue types."""
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    DOCUMENTATION = "documentation"
    QUESTION = "question"


class IssueStatus(str, Enum):
    """Issue status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


@dataclass
class PullRequest:
    """Pull Request for skill changes.

    Attributes:
        pr_id: Unique identifier
        title: PR title
        description: Detailed description
        source_repo: Source repository ID
        target_repo: Target repository ID
        source_branch: Source branch name
        target_branch: Target branch (usually main)
        author: Who created this PR
        status: Current status
        created_at: When created
        updated_at: Last update time
        merged_at: When merged (if applicable)
        reviewers: List of reviewer IDs
        comments: List of comment IDs
        changed_files: List of files changed
        additions: Lines added
        deletions: Lines deleted
        labels: Labels for categorization
        metadata: Additional PR data
    """

    pr_id: str = ""
    title: str = ""
    description: str = ""
    source_repo: str = ""
    target_repo: str = ""
    source_branch: str = ""
    target_branch: str = "main"
    author: str = ""
    status: PRStatus = PRStatus.OPEN
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    merged_at: Optional[datetime] = None
    reviewers: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    changed_files: List[str] = field(default_factory=list)
    additions: int = 0
    deletions: int = 0
    labels: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Issue:
    """Issue or bug report.

    Attributes:
        issue_id: Unique identifier
        title: Issue title
        description: Detailed description
        issue_type: Type of issue (bug, feature, etc.)
        status: Current status
        priority: Priority level (low/medium/high/critical)
        author: Who reported it
        assignee: Who is assigned to fix it
        repo_id: Repository this belongs to
        labels: Issue labels
        created_at: When created
        updated_at: Last update
        closed_at: When closed (if applicable)
        comments: List of comment IDs
        related_prs: Related pull request IDs
        metadata: Additional issue data
    """

    issue_id: str = ""
    title: str = ""
    description: str = ""
    issue_type: IssueType = IssueType.BUG
    status: IssueStatus = IssueStatus.OPEN
    priority: str = "medium"
    author: str = ""
    assignee: Optional[str] = None
    repo_id: str = ""
    labels: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    comments: List[str] = field(default_factory=list)
    related_prs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Comment:
    """Comment on a PR, issue, or skill.

    Attributes:
        comment_id: Unique identifier
        content: Comment text/markdown
        author: Who wrote it
        parent_type: What this comments on ("pr", "issue", "skill")
        parent_id: Parent PR/issue/skill ID
        created_at: When written
        updated_at: Last edit time
        reactions: Emoji reactions {emoji: count}
        resolved: Whether this comment's concern was addressed
        replies: Reply comment IDs
    """

    comment_id: str = ""
    content: str = ""
    author: str = ""
    parent_type: str = ""  # "pr", "issue", "skill"
    parent_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    reactions: Dict[str, int] = field(default_factory=dict)
    resolved: bool = False
    replies: List[str] = field(default_factory=list)


@dataclass
class ActivityItem:
    """Activity feed item.

    Attributes:
        activity_id: Unique identifier
        actor: Who performed the action
        action_type: Type of action (starred, forked, commented, etc.)
        target_type: What was acted on ("repo", "pr", "issue")
        target_id: Target object ID
        timestamp: When this happened
        details: Additional context about the action
    """

    activity_id: str = ""
    actor: str = ""
    action_type: str = ""
    target_type: str = ""
    target_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewRequest:
    """Request for someone to review a PR.

    Attributes:
        request_id: Unique identifier
        pr_id: Pull request being reviewed
        reviewer: Who is requested to review
        requester: Who requested the review
        status: Status of the review request
        submitted_at: When the review was submitted (if done)
        review_content: The actual review content
        approval_status: Approved / Changes Requested / Comment only
    """

    request_id: str = ""
    pr_id: str = ""
    reviewer: str = ""
    requester: str = ""
    status: str = "pending"  # pending, completed, declined
    submitted_at: Optional[datetime] = None
    review_content: str = ""
    approval_status: Optional[str] = None


class CollaborationManager:
    """Manages collaboration features for Skills Hub.

    Provides complete GitHub-style collaboration:
    - Pull requests with review workflow
    - Issue tracking and management
    - Comments and discussions
    - Activity feeds
    - Review assignments
    """

    def __init__(self):
        """Initialize collaboration manager."""
        self.pull_requests: Dict[str, PullRequest] = {}
        self.issues: Dict[str, Issue] = {}
        self.comments: Dict[str, Comment] = {}
        self.activities: List[ActivityItem] = []
        self.review_requests: Dict[str, ReviewRequest] = {}

    # =========================================================================
    # PULL REQUEST METHODS
    # =========================================================================

    def create_pull_request(
        self,
        title: str,
        description: str,
        source_repo: str,
        target_repo: str,
        author: str,
        source_branch: str = "feature-branch",
        target_branch: str = "main",
        **kwargs,
    ) -> PullRequest:
        """Create a new pull request.

        Args:
            title: PR title
            description: Detailed description of changes
            source_repo: Source repository ID
            target_repo: Target repository ID
            author: Author username
            source_branch: Branch with changes
            target_branch: Branch to merge into

        Returns:
            Created PullRequest object
        """
        import uuid

        pr = PullRequest(
            pr_id=f"pr-{uuid.uuid4().hex[:8]}",
            title=title,
            description=description,
            source_repo=source_repo,
            target_repo=target_repo,
            source_branch=source_branch,
            target_branch=target_branch,
            author=author,
            **kwargs,
        )

        self.pull_requests[pr.pr_id] = pr
        self._log_activity(author, "opened_pr", "pr", pr.pr_id, {"title": title})

        return pr

    def get_pull_request(self, pr_id: str) -> Optional[PullRequest]:
        """Get a pull request by ID."""
        return self.pull_requests.get(pr_id)

    def list_pull_requests(
        self,
        repo_id: Optional[str] = None,
        author: Optional[str] = None,
        status: Optional[PRStatus] = None,
        limit: int = 50,
    ) -> List[PullRequest]:
        """List pull requests with filtering."""
        prs = list(self.pull_requests.values())

        if repo_id:
            prs = [p for p in prs if p.target_repo == repo_id]
        if author:
            prs = [p for p in prs if p.author == author]
        if status:
            prs = [p for p in prs if p.status == status]

        return sorted(prs, key=lambda p: p.created_at, reverse=True)[:limit]

    def update_pr_status(
        self,
        pr_id: str,
        status: PRStatus,
        user: str = "",
    ) -> Optional[PullRequest]:
        """Update PR status.

        Args:
            pr_id: PR to update
            status: New status
            user: Who made the change

        Returns:
            Updated PR or None if not found
        """
        pr = self.pull_requests.get(pr_id)
        if not pr:
            return None

        old_status = pr.status
        pr.status = status
        pr.updated_at = datetime.now()

        if status == PRStatus.MERGED:
            pr.merged_at = datetime.now()

        self._log_activity(user, f"pr_{status.value}", "pr", pr_id, {
            "old_status": old_status.value,
            "new_status": status.value,
        })

        return pr

    def add_reviewer_to_pr(
        self,
        pr_id: str,
        reviewer: str,
        requester: str = "",
    ) -> Optional[ReviewRequest]:
        """Request a review from a user.

        Args:
            pr_id: PR to review
            reviewer: User to request review from
            requester: Who is requesting

        Returns:
            Created ReviewRequest
        """
        import uuid

        pr = self.pull_requests.get(pr_id)
        if not pr:
            return None

        if reviewer not in pr.reviewers:
            pr.reviewers.append(reviewer)

        request = ReviewRequest(
            request_id=f"rr-{uuid.uuid4().hex[:8]}",
            pr_id=pr_id,
            reviewer=reviewer,
            requester=requester,
        )

        self.review_requests[request.request_id] = request
        return request

    # =========================================================================
    # ISSUE METHODS
    # =========================================================================

    def create_issue(
        self,
        title: str,
        description: str,
        issue_type: IssueType = IssueType.BUG,
        author: str = "",
        repo_id: str = "",
        priority: str = "medium",
        **kwargs,
    ) -> Issue:
        """Create a new issue.

        Args:
            title: Issue title
            description: Detailed description
            issue_type: Type of issue
            author: Reporter
            repo_id: Associated repository
            priority: Priority level

        Returns:
            Created Issue object
        """
        import uuid

        issue = Issue(
            issue_id=f"issue-{uuid.uuid4().hex[:8]}",
            title=title,
            description=description,
            issue_type=issue_type,
            author=author,
            repo_id=repo_id,
            priority=priority,
            **kwargs,
        )

        self.issues[issue.issue_id] = issue
        self._log_activity(author, "opened_issue", "issue", issue.issue_id, {
            "type": issue_type.value,
            "priority": priority,
        })

        return issue

    def get_issue(self, issue_id: str) -> Optional[Issue]:
        """Get an issue by ID."""
        return self.issues.get(issue_id)

    def list_issues(
        self,
        repo_id: Optional[str] = None,
        author: Optional[str] = None,
        issue_type: Optional[IssueType] = None,
        status: Optional[IssueStatus] = None,
        limit: int = 50,
    ) -> List[Issue]:
        """List issues with filtering."""
        issues = list(self.issues.values())

        if repo_id:
            issues = [i for i in issues if i.repo_id == repo_id]
        if author:
            issues = [i for i in issues if i.author == author]
        if issue_type:
            issues = [i for i in issues if i.issue_type == issue_type]
        if status:
            issues = [i for i in issues if i.status == status]

        return sorted(issues, key=lambda i: i.created_at, reverse=True)[:limit]

    def update_issue_status(
        self,
        issue_id: str,
        status: IssueStatus,
        user: str = "",
    ) -> Optional[Issue]:
        """Update issue status."""
        issue = self.issues.get(issue_id)
        if not issue:
            return None

        issue.status = status
        issue.updated_at = datetime.now()

        if status == IssueStatus.CLOSED:
            issue.closed_at = datetime.now()

        self._log_activity(user, f"issue_{status.value}", "issue", issue_id)
        return issue

    def assign_issue(
        self,
        issue_id: str,
        assignee: str,
        assigner: str = "",
    ) -> Optional[Issue]:
        """Assign an issue to someone."""
        issue = self.issues.get(issue_id)
        if not issue:
            return None

        issue.assignee = assignee
        issue.updated_at = datetime.now()
        self._log_activity(assigner, "assigned_issue", "issue", issue_id, {
            "assignee": assignee,
        })
        return issue

    # =========================================================================
    # COMMENT METHODS
    # =========================================================================

    def create_comment(
        self,
        content: str,
        author: str,
        parent_type: str,
        parent_id: str,
        **kwargs,
    ) -> Comment:
        """Create a new comment.

        Args:
            content: Comment text
            author: Author username
            parent_type: Type of parent ("pr", "issue", "skill")
            parent_id: Parent object ID

        Returns:
            Created Comment object
        """
        import uuid

        comment = Comment(
            comment_id=f"comment-{uuid.uuid4().hex[:8]}",
            content=content,
            author=author,
            parent_type=parent_type,
            parent_id=parent_id,
            **kwargs,
        )

        self.comments[comment.comment_id] = comment

        # Add to parent's comment list
        if parent_type == "pr":
            pr = self.pull_requests.get(parent_id)
            if pr and comment.comment_id not in pr.comments:
                pr.comments.append(comment.comment_id)
        elif parent_type == "issue":
            issue = self.issues.get(parent_id)
            if issue and comment.comment_id not in issue.comments:
                issue.comments.append(comment.comment_id)

        self._log_activity(author, "commented", parent_type, parent_id)
        return comment

    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """Get a comment by ID."""
        return self.comments.get(comment_id)

    def list_comments(
        self,
        parent_type: str,
        parent_id: str,
        limit: int = 100,
    ) -> List[Comment]:
        """List comments for a parent object."""
        comments = [
            c for c in self.comments.values()
            if c.parent_type == parent_type and c.parent_id == parent_id
        ]
        return sorted(comments, key=lambda c: c.created_at)[:limit]

    def add_reaction(
        self,
        comment_id: str,
        emoji: str,
        user: str,
    ) -> bool:
        """Add a reaction to a comment.

        Args:
            comment_id: Comment to react to
            emoji: Emoji character (e.g., "👍", "❤️")
            user: Who reacted

        Returns:
            True if successful
        """
        comment = self.comments.get(comment_id)
        if not comment:
            return False

        current = comment.reactions.get(emoji, 0)

        # Check if user already reacted
        reaction_key = f"{user}:{emoji}"
        if comment.metadata.get(reaction_key):
            # Remove reaction
            del comment.metadata[reaction_key]
            comment.reactions[emoji] = max(0, current - 1)
        else:
            # Add reaction
            comment.metadata[reaction_key] = True
            comment.reactions[emoji] = current + 1

        return True

    # =========================================================================
    # ACTIVITY FEED METHODS
    # =========================================================================

    def _log_activity(
        self,
        actor: str,
        action_type: str,
        target_type: str,
        target_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Log an activity event."""
        import uuid

        activity = ActivityItem(
            activity_id=f"act-{uuid.uuid4().hex[:6]}",
            actor=actor,
            action_type=action_type,
            target_type=target_type,
            target_id=target_id,
            details=details or {},
        )

        self.activities.append(activity)

        # Keep only last 1000 activities
        if len(self.activities) > 1000:
            self.activities = self.activities[-1000:]

    def get_activity_feed(
        self,
        user: Optional[str] = None,
        target_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[ActivityItem]:
        """Get activity feed with filtering."""
        activities = self.activities

        if user:
            activities = [
                a for a in activities
                if a.actor == user or (
                    target_type and a.target_type == target_type
                    and a.target_id in {
                        r.target_repo for r in self.list_pull_requests(repo_id=a.details.get("repo_id"))
                    }
                )
            ]

        if target_type:
            activities = [a for a in activities if a.target_type == target_type]

        return sorted(activities, key=lambda a: a.timestamp, reverse=True)[:limit]

    # =========================================================================
    # STATISTICS AND REPORTS
    # =========================================================================

    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Get comprehensive collaboration statistics."""
        total_prs = len(self.pull_requests)
        open_prs = sum(1 for p in self.pull_requests.values() if p.status == PRStatus.OPEN)
        merged_prs = sum(1 for p in self.pull_requests.values() if p.status == PRStatus.MERGED)

        total_issues = len(self.issues)
        open_issues = sum(1 for i in self.issues.values() if i.status == IssueStatus.OPEN)

        total_comments = len(self.comments)

        recent_activities = len([a for a in self.activities
                                  if (datetime.now() - a.timestamp).days < 7])

        return {
            "pull_requests": {
                "total": total_prs,
                "open": open_prs,
                "merged": merged_prs,
                "closed": total_prs - open_prs - merged_prs,
            },
            "issues": {
                "total": total_issues,
                "open": open_issues,
                "resolved": sum(1 for i in self.issues.values() if i.status == IssueStatus.RESOLVED),
            },
            "comments": {
                "total": total_comments,
                "avg_per_pr": round(total_comments / max(total_prs, 1), 1),
            },
            "activity": {
                "last_7_days": recent_activities,
                "total_events": len(self.activities),
            },
            "review_requests": {
                "total": len(self.review_requests),
                "pending": sum(1 for r in self.review_requests.values() if r.status == "pending"),
                "completed": sum(1 for r in self.review_requests.values() if r.status == "completed"),
            },
        }
