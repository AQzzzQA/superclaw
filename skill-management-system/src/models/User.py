"""
User Model for Skill Management System
Represents a user with roles, permissions, and workspace associations.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from enum import Enum


class UserRole(Enum):
    """User role enumeration"""
    SYSTEM_ADMIN = "system_admin"
    WORKSPACE_ADMIN = "workspace_admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    BUSINESS_USER = "business_user"
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"
    GUEST = "guest"


class UserStatus(Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User:
    """User model representing a system user"""
    
    def __init__(self, user_id: str = None, email: str = None, name: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email
        self.name = name
        self.status = UserStatus.PENDING
        self.role = UserRole.USER
        self.roles = []
        self.permissions = set()
        self.workspaces = []
        self.skill_usage = {}
        self.last_login = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.constraints = {}
        self.preferences = {}
        self.notification_settings = {}
        
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "status": self.status.value,
            "role": self.role.value,
            "roles": [role.value for role in self.roles],
            "permissions": list(self.permissions),
            "workspaces": self.workspaces,
            "skill_usage": self.skill_usage,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "constraints": self.constraints,
            "preferences": self.preferences,
            "notification_settings": self.notification_settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary"""
        user = cls(
            user_id=data.get("user_id"),
            email=data.get("email"),
            name=data.get("name")
        )
        user.status = UserStatus(data.get("status", "pending"))
        user.role = UserRole(data.get("role", "user"))
        user.roles = [UserRole(role) for role in data.get("roles", [])]
        user.permissions = set(data.get("permissions", []))
        user.workspaces = data.get("workspaces", [])
        user.skill_usage = data.get("skill_usage", {})
        user.last_login = datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None
        user.created_at = datetime.fromisoformat(data["created_at"])
        user.updated_at = datetime.fromisoformat(data["updated_at"])
        user.constraints = data.get("constraints", {})
        user.preferences = data.get("preferences", {})
        user.notification_settings = data.get("notification_settings", {})
        return user
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        return permission in self.permissions
    
    def add_permission(self, permission: str) -> None:
        """Add permission to user"""
        self.permissions.add(permission)
        self.updated_at = datetime.now()
    
    def remove_permission(self, permission: str) -> None:
        """Remove permission from user"""
        self.permissions.discard(permission)
        self.updated_at = datetime.now()
    
    def add_role(self, role: UserRole) -> None:
        """Add role to user"""
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.now()
    
    def remove_role(self, role: UserRole) -> None:
        """Remove role from user"""
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.now()
    
    def add_workspace(self, workspace_id: str) -> None:
        """Add workspace to user"""
        if workspace_id not in self.workspaces:
            self.workspaces.append(workspace_id)
            self.updated_at = datetime.now()
    
    def remove_workspace(self, workspace_id: str) -> None:
        """Remove workspace from user"""
        if workspace_id in self.workspaces:
            self.workspaces.remove(workspace_id)
            self.updated_at = datetime.now()
    
    def update_skill_usage(self, skill_id: str, usage_count: int = 1) -> None:
        """Update skill usage statistics"""
        if skill_id not in self.skill_usage:
            self.skill_usage[skill_id] = 0
        self.skill_usage[skill_id] += usage_count
        self.updated_at = datetime.now()
    
    def check_constraint(self, constraint_type: str, value: any) -> bool:
        """Check if user meets constraint requirements"""
        if constraint_type in self.constraints:
            return value <= self.constraints[constraint_type]
        return True
    
    def set_constraint(self, constraint_type: str, max_value: int) -> None:
        """Set user constraint"""
        self.constraints[constraint_type] = max_value
        self.updated_at = datetime.now()
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE
    
    def activate(self) -> None:
        """Activate user account"""
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.now()
    
    def suspend(self, reason: str = None) -> None:
        """Suspend user account"""
        self.status = UserStatus.SUSPENDED
        self.constraints["suspended_reason"] = reason
        self.updated_at = datetime.now()
    
    def can_install_skill(self, skill_id: str, skill_requirements: Dict) -> bool:
        """Check if user can install a skill"""
        if not self.is_active():
            return False
        
        # Check role-based permissions
        required_level = skill_requirements.get("required_level", "user")
        role_hierarchy = {
            "viewer": 1,
            "user": 2,
            "business_user": 3,
            "developer": 4,
            "analyst": 4,
            "manager": 5,
            "workspace_admin": 6,
            "system_admin": 7
        }
        
        user_level = role_hierarchy.get(self.role.value, 0)
        required_level_value = role_hierarchy.get(required_level, 0)
        
        if user_level < required_level_value:
            return False
        
        # Check skill usage limits
        max_skills = skill_requirements.get("max_skills", 50)
        current_skills = len(self.skill_usage)
        if current_skills >= max_skills:
            return False
        
        # Check workspace limits
        max_workspaces = skill_requirements.get("max_workspaces", 10)
        if len(self.workspaces) >= max_workspaces:
            return False
        
        return True
    
    def get_skill_usage_stats(self) -> Dict:
        """Get skill usage statistics"""
        total_usage = sum(self.skill_usage.values())
        unique_skills = len(self.skill_usage)
        avg_usage = total_usage / unique_skills if unique_skills > 0 else 0
        
        return {
            "total_usage": total_usage,
            "unique_skills": unique_skills,
            "average_usage": avg_usage,
            "most_used_skill": max(self.skill_usage.items(), key=lambda x: x[1])[0] if self.skill_usage else None
        }
    
    def to_json(self) -> str:
        """Convert user to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'User':
        """Create user from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class UserManager:
    """Manager class for user operations"""
    
    def __init__(self):
        self.users = {}
        self.user_index = {}  # Email to user_id mapping
    
    def create_user(self, email: str, name: str, role: UserRole = UserRole.USER) -> User:
        """Create a new user"""
        user = User(email=email, name=name)
        user.role = role
        user.activate()
        
        self.users[user.user_id] = user
        self.user_index[email] = user.user_id
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_id = self.user_index.get(email)
        return self.users.get(user_id) if user_id else None
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user information"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Remove from index
        if user.email in self.user_index:
            del self.user_index[user.email]
        
        # Remove from users
        del self.users[user_id]
        
        return True
    
    def list_users(self, status: UserStatus = None) -> List[User]:
        """List users with optional status filter"""
        users = list(self.users.values())
        if status:
            users = [user for user in users if user.status == status]
        return users
    
    def get_users_by_role(self, role: UserRole) -> List[User]:
        """Get users by role"""
        return [user for user in self.users.values() if user.role == role]
    
    def get_users_by_workspace(self, workspace_id: str) -> List[User]:
        """Get users in a specific workspace"""
        return [user for user in self.users.values() if workspace_id in user.workspaces]
    
    def validate_user_login(self, email: str, password: str) -> Optional[User]:
        """Validate user login"""
        user = self.get_user_by_email(email)
        if user and user.is_active():
            # In a real implementation, this would check a hashed password
            # For now, we'll just check if email exists
            user.update_last_login()
            return user
        return None
    
    def audit_user_activity(self, user_id: str, action: str, details: Dict = None) -> None:
        """Log user activity for audit purposes"""
        user = self.get_user(user_id)
        if user:
            audit_entry = {
                "user_id": user_id,
                "user_email": user.email,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "details": details or {}
            }
            # In a real implementation, this would write to an audit log
            print(f"Audit: {audit_entry}")