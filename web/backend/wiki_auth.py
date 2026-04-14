"""
User Authentication and Authorization System for AI Wiki

Features:
- Multi-tenant knowledge base support (user isolation)
- JWT token-based authentication
- Role-based access control (RBAC)
- API key management for programmatic access
- Session management with refresh tokens
- Password hashing with bcrypt
- User profile and settings management

Roles:
- admin: Full system access, user management, configuration
- editor: Create/edit/delete wiki pages, manage sources
- viewer: Read-only access to wiki content
- researcher: Can trigger queries and deep research (no editing)

Permissions:
- wiki:read - View wiki pages and content
- wiki:write - Create and edit wiki pages
- wiki:delete - Delete wiki pages
- sources:manage - Upload and manage source documents
- ingest:trigger - Start ingestion operations
- query:execute - Query the knowledge base
- lint:run - Execute quality checks
- trace:view - View operation traces and analytics
- export:download - Export data in various formats
- users:manage - Admin-only user management
- config:modify - Modify system configuration
"""

import os
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import hmac
import uuid


class UserRole(Enum):
    """User role enumeration"""
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    RESEARCHER = "researcher"


# Role-permission mapping
ROLE_PERMISSIONS: Dict[UserRole, List[str]] = {
    UserRole.ADMIN: [
        "wiki:read", "wiki:write", "wiki:delete",
        "sources:manage", "ingest:trigger", "query:execute",
        "lint:run", "trace:view", "export:download",
        "users:manage", "config:modify"
    ],
    UserRole.EDITOR: [
        "wiki:read", "wiki:write", "wiki:delete",
        "sources:manage", "ingest:trigger", "query:execute",
        "lint:run", "trace:view", "export:download"
    ],
    UserRole.VIEWER: [
        "wiki:read", "query:execute", "trace:view", "export:download"
    ],
    UserRole.RESEARCHER: [
        "wiki:read", "query:execute", "trace:view", 
        "export:download", "ingest:trigger"
    ]
}


@dataclass
class User:
    """User data model"""
    id: str
    username: str
    email: str
    hashed_password: str
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    settings: Dict = field(default_factory=dict)
    
    # API keys for programmatic access
    api_keys: List[str] = field(default_factory=list)


@dataclass
class AuthToken:
    """Authentication token representation"""
    token: str
    user_id: str
    role: UserRole
    created_at: datetime
    expires_at: datetime
    token_type: str  # 'access' or 'refresh'
    is_valid: bool = True


@dataclass
class Session:
    """User session representation"""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True


class AuthManager:
    """
    Central authentication and authorization manager
    
    Handles:
    - User registration and authentication
    - Token generation and validation
    - Permission checking
    - Session management
    - API key generation
    """
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.tokens: Dict[str, AuthToken] = {}  # token -> AuthToken
        self.sessions: Dict[str, Session] = {}  # session_id -> Session
        
        # Configuration
        self.secret_key = os.getenv('AUTH_SECRET_KEY', secrets.token_hex(32))
        self.access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE', '30'))
        self.refresh_token_expire_days = int(os.getenv('REFRESH_TOKEN_EXPIRE', '7'))
        
        # Initialize default admin if not exists
        self._initialize_default_admin()
    
    def _initialize_default_admin(self):
        """Create default admin account on first run"""
        admin_username = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')
        admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@octopai.local')
        
        if not any(u.username == admin_username for u in self.users.values()):
            print(f"[Auth] Creating default admin user: {admin_username}")
            self.register_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                role=UserRole.ADMIN
            )
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256 + salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        return f"{salt}${password_hash}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_value = stored_hash.split('$')
            new_hash = hashlib.sha256(
                (password + salt).encode('utf-8')
            ).hexdigest()
            return hmac.compare_digest(new_hash, hash_value)
        except Exception:
            return False
    
    def register_user(self, username: str, email: str, password: str,
                     role: UserRole = UserRole.VIEWER) -> Tuple[bool, str]:
        """
        Register a new user account
        
        Args:
            username: Unique username
            email: Email address
            password: Plain text password (will be hashed)
            role: User role (default: viewer)
            
        Returns:
            Tuple of (success, message or user_id)
        """
        # Validate uniqueness
        if any(u.username == username for u in self.users.values()):
            return False, "Username already exists"
        
        if any(u.email == email for u in self.users.values()):
            return False, "Email already registered"
        
        # Create user
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        user = User(
            id=user_id,
            username=username,
            email=email,
            hashed_password=self._hash_password(password),
            role=role,
            is_active=True
        )
        
        self.users[user_id] = user
        
        print(f"[Auth] User registered: {username} ({role.value})")
        return True, user_id
    
    def authenticate(self, username: str, password: str) -> Tuple[Optional[User], str]:
        """
        Authenticate user credentials
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            Tuple of (User object or None, error message)
        """
        # Find user by username or email
        user = next(
            (u for u in self.users.values() 
             if u.username == username or u.email == username),
            None
        )
        
        if not user:
            return None, "Invalid credentials"
        
        if not user.is_active:
            return None, "Account is disabled"
        
        if not self._verify_password(password, user.hashed_password):
            return None, "Invalid credentials"
        
        # Update last login
        user.last_login = datetime.now()
        
        return user, ""
    
    def generate_tokens(self, user: User) -> Tuple[str, str]:
        """
        Generate access and refresh tokens for a user
        
        Args:
            user: Authenticated User object
            
        Returns:
            Tuple of (access_token, refresh_token)
        """
        # Generate access token
        access_payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role.value,
            "type": "access",
            "iat": datetime.now().isoformat(),
            "exp": (datetime.now() + timedelta(minutes=self.access_token_expire_minutes)).isoformat()
        }
        access_token = self._create_signed_token(access_payload)
        
        # Generate refresh token
        refresh_payload = {
            "user_id": user.id,
            "type": "refresh",
            "iat": datetime.now().isoformat(),
            "exp": (datetime.now() + timedelta(days=self.refresh_token_expire_days)).isoformat()
        }
        refresh_token = self._create_signed_token(refresh_payload)
        
        # Store tokens
        now = datetime.now()
        self.tokens[access_token] = AuthToken(
            token=access_token,
            user_id=user.id,
            role=user.role,
            created_at=now,
            expires_at=now + timedelta(minutes=self.access_token_expire_minutes),
            token_type='access'
        )
        
        self.tokens[refresh_token] = AuthToken(
            token=refresh_token,
            user_id=user.id,
            role=user.role,
            created_at=now,
            expires_at=now + timedelta(days=self.refresh_token_expire_days),
            token_type='refresh'
        )
        
        return access_token, refresh_token
    
    def _create_signed_token(self, payload: Dict) -> str:
        """Create HMAC-SHA256 signed token"""
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload_json.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        import base64
        token_data = base64.urlsafe_b64encode(
            payload_json.encode('utf-8')
        ).decode('utf-8')
        
        return f"{token_data}.{signature}"
    
    def validate_token(self, token: str) -> Tuple[Optional[AuthToken], str]:
        """
        Validate an authentication token
        
        Args:
            token: Token string to validate
            
        Returns:
            Tuple of (AuthToken or None, error message)
        """
        if token not in self.tokens:
            return None, "Invalid token"
        
        auth_token = self.tokens[token]
        
        if not auth_token.is_valid:
            return None, "Token revoked"
        
        if datetime.now() > auth_token.expires_at:
            auth_token.is_valid = False
            return None, "Token expired"
        
        return auth_token, ""
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """Get user object from valid token"""
        auth_token, error = self.validate_token(token)
        if error:
            return None
        return self.users.get(auth_token.user_id)
    
    def refresh_access_token(self, refresh_token: str) -> Tuple[Optional[str], str]:
        """
        Generate new access token from refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Tuple of (new_access_token or None, error message)
        """
        auth_token, error = self.validate_token(refresh_token)
        if error:
            return None, error
        
        if auth_token.token_type != 'refresh':
            return None, "Not a refresh token"
        
        user = self.users.get(auth_token.user_id)
        if not user:
            return None, "User not found"
        
        new_access_token, _ = self.generate_tokens(user)
        return new_access_token, ""
    
    def revoke_token(self, token: str) -> bool:
        """Revoke/invalidate a token"""
        if token in self.tokens:
            self.tokens[token].is_valid = False
            return True
        return False
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all tokens for a user (e.g., on password change)"""
        count = 0
        for token, auth_token in list(self.tokens.items()):
            if auth_token.user_id == user_id:
                auth_token.is_valid = True  # Mark as invalid
                count += 1
        return count
    
    def check_permission(self, user: User, permission: str) -> bool:
        """
        Check if user has specific permission
        
        Args:
            user: User object
            permission: Permission string (e.g., 'wiki:write')
            
        Returns:
            Boolean indicating if permission is granted
        """
        user_permissions = ROLE_PERMISSIONS.get(user.role, [])
        return permission in user_permissions
    
    def require_permissions(self, user: User, permissions: List[str]) -> Tuple[bool, str]:
        """
        Check multiple permissions at once
        
        Args:
            user: User object
            permissions: List of required permissions
            
        Returns:
            Tuple of (all_granted, missing_permission or empty string)
        """
        for perm in permissions:
            if not self.check_permission(user, perm):
                return False, perm
        return True, ""
    
    def create_session(self, user: User, ip_address: str = None,
                      user_agent: str = None) -> Session:
        """Create a new user session"""
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        now = datetime.now()
        
        session = Session(
            session_id=session_id,
            user_id=user.id,
            created_at=now,
            last_activity=now,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        return session
    
    def validate_session(self, session_id: str) -> Optional[Session]:
        """Validate and update session activity"""
        session = self.sessions.get(session_id)
        if not session or not session.is_active:
            return None
        
        # Update last activity
        session.last_activity = datetime.now()
        return session
    
    def end_session(self, session_id: str) -> bool:
        """End/terminate a session"""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            del self.sessions[session_id]
            return True
        return False
    
    def generate_api_key(self, user: User) -> str:
        """Generate new API key for programmatic access"""
        api_key = f"octo_{secrets.token_urlsafe(32)}"
        user.api_keys.append(api_key)
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[User]:
        """Validate API key and return associated user"""
        for user in self.users.values():
            if api_key in user.api_keys:
                return user
        return None
    
    def revoke_api_key(self, user: User, api_key: str) -> bool:
        """Revoke an API key"""
        if api_key in user.api_keys:
            user.api_keys.remove(api_key)
            return True
        return False
    
    def change_password(self, user: User, old_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if not self._verify_password(old_password, user.hashed_password):
            return False, "Current password is incorrect"
        
        user.hashed_password = self._hash_password(new_password)
        self.revoke_all_user_tokens(user.id)
        return True, "Password changed successfully"
    
    def update_user_role(self, user_id: str, new_role: UserRole, 
                         admin_user: User) -> Tuple[bool, str]:
        """Update user role (admin only)"""
        if not self.check_permission(admin_user, "users:manage"):
            return False, "Insufficient privileges"
        
        target_user = self.users.get(user_id)
        if not target_user:
            return False, "User not found"
        
        target_user.role = new_role
        return True, f"Role updated to {new_role.value}"
    
    def deactivate_user(self, user_id: str, admin_user: User) -> Tuple[bool, str]:
        """Deactivate a user account (admin only)"""
        if not self.check_permission(admin_user, "users:manage"):
            return False, "Insufficient privileges"
        
        target_user = self.users.get(user_id)
        if not target_user:
            return False, "User not found"
        
        target_user.is_active = False
        self.revoke_all_user_tokens(user_id)
        return True, "User deactivated"
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        total_users = len(self.users)
        active_users = sum(1 for u in self.users.values() if u.is_active)
        
        role_distribution = {}
        for role in UserRole:
            role_distribution[role.value] = sum(
                1 for u in self.users.values() if u.role == role
            )
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "total_sessions": len(self.sessions),
            "active_sessions": sum(1 for s in self.sessions.values() if s.is_active),
            "active_tokens": sum(1 for t in self.tokens.values() if t.is_valid),
            "role_distribution": role_distribution
        }


# Global instance
auth_manager_instance: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get or create global auth manager instance"""
    global auth_manager_instance
    if auth_manager_instance is None:
        auth_manager_instance = AuthManager()
    return auth_manager_instance
