"""
Permission Management - Access control for Skills Hub repositories.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field


class Role(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"


class Permission(str, Enum):
    """Granular permissions for repository operations."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    PUBLISH = "publish"
    UNPUBLISH = "unpublish"
    MANAGE_SETTINGS = "manage_settings"
    INVITE_COLLABORATORS = "invite_collaboraborators"
    REMOVE_COLLABORATORS = "remove_collaborators"
    FORK = "fork"
    STAR = "star"
    WATCH = "watch"
    COMMENT = "comment"
    RATE = "rate"
    DOWNLOAD = "download"


ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: set(Permission),
    Role.MODERATOR: {
        Permission.READ,
        Permission.WRITE,
        Permission.DELETE,
        Permission.PUBLISH,
        Permission.UNPUBLISH,
        Permission.MANAGE_SETTINGS,
        Permission.INVITE_COLLABORATORS,
        Permission.REMOVE_COLLABORATORS,
        Permission.FORK,
        Permission.STAR,
        Permission.WATCH,
        Permission.COMMENT,
        Permission.RATE,
        Permission.DOWNLOAD,
    },
    Role.USER: {
        Permission.READ,
        Permission.FORK,
        Permission.STAR,
        Permission.WATCH,
        Permission.COMMENT,
        Permission.RATE,
        Permission.DOWNLOAD,
    },
    Role.GUEST: {
        Permission.READ,
        Permission.DOWNLOAD,
    },
}


@dataclass
class Collaborator:
    """Collaborator on a repository.

    Attributes:
        user_id: User identifier
        role: Role for this repository
        added_at: When they were added
        added_by: Who added them
        permissions: Explicit permissions (if different from role defaults)
    """

    user_id: str = ""
    role: Role = Role.USER
    added_at: str = ""
    added_by: str = ""
    permissions: Set[Permission] = field(default_factory=set)


@dataclass
class AccessRule:
    """Access rule for a repository.

    Attributes:
        repo_id: Repository this rule applies to
        user_id or role: Who this rule applies to
        allowed_permissions: Permissions granted
        denied_permissions: Permissions explicitly denied
        expires_at: When this rule expires (None = never)
    """

    repo_id: str = ""
    user_id: Optional[str] = None
    role: Optional[Role] = None
    allowed_permissions: Set[Permission] = field(default_factory=set)
    denied_permissions: Set[Permission] = field(default_factory=set)
    expires_at: Optional[str] = None


class PermissionManager:
    """Manages access control and permissions for skill repositories.

    Supports:
    - Role-based access control (RBAC)
    - Per-repository permissions
    - Collaborator management
    - Fine-grained permission checks
    """

    def __init__(self):
        """Initialize permission manager."""
        self.collaborators: Dict[str, List[Collaborator]] = {}
        self.access_rules: List[AccessRule] = []
        self.user_roles: Dict[str, Role] = {}

    def set_user_role(self, user_id: str, role: Role) -> None:
        """Set global role for a user.

        Args:
            user_id: User identifier
            role: Role to assign
        """
        self.user_roles[user_id] = role

    def get_user_role(self, user_id: str) -> Role:
        """Get global role for a user.

        Args:
            user_id: User identifier

        Returns:
            User's role (defaults to GUEST)
        """
        return self.user_roles.get(user_id, Role.GUEST)

    def add_collaborator(
        self,
        repo_id: str,
        user_id: str,
        role: Role = Role.USER,
        added_by: str = "",
        permissions: Optional[Set[Permission]] = None,
    ) -> bool:
        """Add a collaborator to a repository.

        Args:
            repo_id: Repository ID
            user_id: User to add
            role: Role for this repository
            added_by: Who is adding them
            permissions: Custom permissions (if different from role)

        Returns:
            True if added successfully
        """
        from datetime import datetime

        if repo_id not in self.collaborators:
            self.collaborators[repo_id] = []

        existing = [c for c in self.collaborators[repo_id] if c.user_id == user_id]
        if existing:
            return False

        collaborator = Collaborator(
            user_id=user_id,
            role=role,
            added_at=datetime.now().isoformat(),
            added_by=added_by,
            permissions=permissions or set(),
        )

        self.collaborators[repo_id].append(collaborator)
        return True

    def remove_collaborator(self, repo_id: str, user_id: str) -> bool:
        """Remove a collaborator from a repository.

        Args:
            repo_id: Repository ID
            user_id: User to remove

        Returns:
            True if removed successfully
        """
        if repo_id not in self.collaborators:
            return False

        original_len = len(self.collaborators[repo_id])
        self.collaborators[repo_id] = [
            c for c in self.collaborators[repo_id] if c.user_id != user_id
        ]

        return len(self.collaborators[repo_id]) < original_len

    def get_collaborators(self, repo_id: str) -> List[Collaborator]:
        """Get all collaborators for a repository.

        Args:
            repo_id: Repository ID

        Returns:
            List of collaborators
        """
        return self.collaborators.get(repo_id, [])

    def check_permission(
        self,
        user_id: str,
        repo_id: str,
        permission: Permission,
    ) -> bool:
        """Check if a user has a specific permission on a repository.

        Args:
            user_id: User identifier
            repo_id: Repository ID
            permission: Permission to check

        Returns:
            True if user has the permission
        """
        user_role = self.get_user_role(user_id)

        if user_role == Role.ADMIN:
            return True

        base_permissions = ROLE_PERMISSIONS.get(user_role, set())

        if permission in base_permissions:
            pass

        collaborator_perms = self._get_collaborator_permissions(user_id, repo_id)

        all_perms = base_permissions | collaborator_perms

        for rule in self.access_rules:
            if rule.repo_id == repo_id:
                if rule.user_id == user_id or (rule.role and rule.role == user_role):
                    all_perms = all_perms | rule.allowed_permissions
                    all_perms = all_perms - rule.denied_permissions

        owner_repo_id = f"{user_id}/"
        if repo_id.startswith(owner_repo_id):
            return True

        return permission in all_perms

    def check_any_permission(
        self,
        user_id: str,
        repo_id: str,
        permissions: List[Permission],
    ) -> bool:
        """Check if user has ANY of the specified permissions.

        Args:
            user_id: User identifier
            repo_id: Repository ID
            permissions: List of permissions to check

        Returns:
            True if user has at least one permission
        """
        return any(
            self.check_permission(user_id, repo_id, perm)
            for perm in permissions
        )

    def check_all_permissions(
        self,
        user_id: str,
        repo_id: str,
        permissions: List[Permission],
    ) -> bool:
        """Check if user has ALL of the specified permissions.

        Args:
            user_id: User identifier
            repo_id: Repository ID
            permissions: List of permissions to check

        Returns:
            True if user has all permissions
        """
        return all(
            self.check_permission(user_id, repo_id, perm)
            for perm in permissions
        )

    def _get_collaborator_permissions(
        self,
        user_id: str,
        repo_id: str,
    ) -> Set[Permission]:
        """Get permissions from collaborator status."""
        collaborators = self.get_collaborators(repo_id)

        for collab in collaborators:
            if collab.user_id == user_id:
                if collab.permissions:
                    return collab.permissions
                else:
                    return ROLE_PERMISSIONS.get(collab.role, set())

        return set()

    def can_read(self, user_id: str, repo_id: str) -> bool:
        """Check read access."""
        return self.check_permission(user_id, repo_id, Permission.READ)

    def can_write(self, user_id: str, repo_id: str) -> bool:
        """Check write access."""
        return self.check_permission(user_id, repo_id, Permission.WRITE)

    def can_delete(self, user_id: str, repo_id: str) -> bool:
        """Check delete access."""
        return self.check_permission(user_id, repo_id, Permission.DELETE)

    def can_publish(self, user_id: str, repo_id: str) -> bool:
        """Check publish access."""
        return self.check_permission(user_id, repo_id, Permission.PUBLISH)

    def can_manage(self, user_id: str, repo_id: str) -> bool:
        """Check full management access."""
        return self.check_all_permissions(
            user_id,
            repo_id,
            [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.PUBLISH],
        )
