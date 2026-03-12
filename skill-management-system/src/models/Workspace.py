"""
Workspace Model for Skill Management System
Represents a workspace with users, skills, and configuration.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from enum import Enum


class WorkspaceStatus(Enum):
    """Workspace status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    PENDING = "pending"


class WorkspaceType(Enum):
    """Workspace type enumeration"""
    TEAM = "team"
    DEPARTMENT = "department"
    ORGANIZATION = "organization"
    INDIVIDUAL = "individual"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    COLLABORATION = "collaboration"


class Workspace:
    """Workspace model representing a skill workspace"""
    
    def __init__(self, workspace_id: str = None, name: str = None, description: str = None):
        self.workspace_id = workspace_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.status = WorkspaceStatus.PENDING
        self.workspace_type = WorkspaceType.TEAM
        self.owner_id = None
        self.admins = []
        self.members = []
        self.skills = []
        self.skill_versions = {}
        self.config = {}
        self.constraints = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_activity = None
        self.audit_log = []
        self.tags = []
        self.metadata = {}
        
    def to_dict(self) -> Dict:
        """Convert workspace to dictionary"""
        return {
            "workspace_id": self.workspace_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "workspace_type": self.workspace_type.value,
            "owner_id": self.owner_id,
            "admins": self.admins,
            "members": self.members,
            "skills": self.skills,
            "skill_versions": self.skill_versions,
            "config": self.config,
            "constraints": self.constraints,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "audit_log": self.audit_log,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Workspace':
        """Create workspace from dictionary"""
        workspace = cls(
            workspace_id=data.get("workspace_id"),
            name=data.get("name"),
            description=data.get("description")
        )
        workspace.status = WorkspaceStatus(data.get("status", "pending"))
        workspace.workspace_type = WorkspaceType(data.get("workspace_type", "team"))
        workspace.owner_id = data.get("owner_id")
        workspace.admins = data.get("admins", [])
        workspace.members = data.get("members", [])
        workspace.skills = data.get("skills", [])
        workspace.skill_versions = data.get("skill_versions", {})
        workspace.config = data.get("config", {})
        workspace.constraints = data.get("constraints", {})
        workspace.created_at = datetime.fromisoformat(data["created_at"])
        workspace.updated_at = datetime.fromisoformat(data["updated_at"])
        workspace.last_activity = datetime.fromisoformat(data["last_activity"]) if data.get("last_activity") else None
        workspace.audit_log = data.get("audit_log", [])
        workspace.tags = data.get("tags", [])
        workspace.metadata = data.get("metadata", {})
        return workspace
    
    def add_admin(self, user_id: str) -> None:
        """Add admin to workspace"""
        if user_id not in self.admins:
            self.admins.append(user_id)
            self.members.append(user_id)
            self.updated_at = datetime.now()
            self.add_audit_log("add_admin", {"user_id": user_id})
    
    def remove_admin(self, user_id: str) -> None:
        """Remove admin from workspace"""
        if user_id in self.admins:
            self.admins.remove(user_id)
            self.updated_at = datetime.now()
            self.add_audit_log("remove_admin", {"user_id": user_id})
    
    def add_member(self, user_id: str) -> None:
        """Add member to workspace"""
        if user_id not in self.members:
            self.members.append(user_id)
            self.updated_at = datetime.now()
            self.add_audit_log("add_member", {"user_id": user_id})
    
    def remove_member(self, user_id: str) -> None:
        """Remove member from workspace"""
        if user_id in self.members:
            self.members.remove(user_id)
            if user_id in self.admins:
                self.admins.remove(user_id)
            self.updated_at = datetime.now()
            self.add_audit_log("remove_member", {"user_id": user_id})
    
    def is_admin(self, user_id: str) -> bool:
        """Check if user is workspace admin"""
        return user_id in self.admins
    
    def is_member(self, user_id: str) -> bool:
        """Check if user is workspace member"""
        return user_id in self.members
    
    def add_skill(self, skill_id: str, version: str = "1.0.0") -> None:
        """Add skill to workspace"""
        if skill_id not in self.skills:
            self.skills.append(skill_id)
        
        if skill_id not in self.skill_versions:
            self.skill_versions[skill_id] = []
        
        if version not in self.skill_versions[skill_id]:
            self.skill_versions[skill_id].append(version)
        
        self.updated_at = datetime.now()
        self.last_activity = datetime.now()
        self.add_audit_log("add_skill", {"skill_id": skill_id, "version": version})
    
    def remove_skill(self, skill_id: str) -> None:
        """Remove skill from workspace"""
        if skill_id in self.skills:
            self.skills.remove(skill_id)
            if skill_id in self.skill_versions:
                del self.skill_versions[skill_id]
            self.updated_at = datetime.now()
            self.last_activity = datetime.now()
            self.add_audit_log("remove_skill", {"skill_id": skill_id})
    
    def get_skill_versions(self, skill_id: str) -> List[str]:
        """Get versions of a specific skill"""
        return self.skill_versions.get(skill_id, [])
    
    def set_constraint(self, constraint_type: str, value: any) -> None:
        """Set workspace constraint"""
        self.constraints[constraint_type] = value
        self.updated_at = datetime.now()
    
    def get_constraint(self, constraint_type: str) -> any:
        """Get workspace constraint value"""
        return self.constraints.get(constraint_type)
    
    def check_constraint(self, constraint_type: str, value: any) -> bool:
        """Check if workspace meets constraint requirements"""
        if constraint_type in self.constraints:
            return value <= self.constraints[constraint_type]
        return True
    
    def add_tag(self, tag: str) -> None:
        """Add tag to workspace"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove tag from workspace"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def set_config(self, key: str, value: any) -> None:
        """Set workspace configuration"""
        self.config[key] = value
        self.updated_at = datetime.now()
    
    def get_config(self, key: str) -> any:
        """Get workspace configuration value"""
        return self.config.get(key)
    
    def add_audit_log(self, action: str, details: Dict = None) -> None:
        """Add entry to audit log"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        self.audit_log.append(audit_entry)
        
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Get recent audit log entries"""
        return self.audit_log[-limit:]
    
    def update_activity(self) -> None:
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """Check if workspace is active"""
        return self.status == WorkspaceStatus.ACTIVE
    
    def activate(self) -> None:
        """Activate workspace"""
        self.status = WorkspaceStatus.ACTIVE
        self.updated_at = datetime.now()
        self.add_audit_log("activate_workspace")
    
    def archive(self) -> None:
        """Archive workspace"""
        self.status = WorkspaceStatus.ARCHIVED
        self.updated_at = datetime.now()
        self.add_audit_log("archive_workspace")
    
    def get_member_count(self) -> int:
        """Get total member count"""
        return len(self.members)
    
    def get_admin_count(self) -> int:
        """Get admin count"""
        return len(self.admins)
    
    def get_skill_count(self) -> int:
        """Get skill count"""
        return len(self.skills)
    
    def to_json(self) -> str:
        """Convert workspace to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Workspace':
        """Create workspace from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class WorkspaceManager:
    """Manager class for workspace operations"""
    
    def __init__(self):
        self.workspaces = {}
        self.workspace_index = {}  # Name to workspace_id mapping
    
    def create_workspace(self, name: str, description: str = None, 
                        workspace_type: WorkspaceType = WorkspaceType.TEAM,
                        owner_id: str = None) -> Workspace:
        """Create a new workspace"""
        workspace = Workspace(name=name, description=description)
        workspace.workspace_type = workspace_type
        workspace.owner_id = owner_id
        workspace.activate()
        
        self.workspaces[workspace.workspace_id] = workspace
        self.workspace_index[name] = workspace.workspace_id
        
        return workspace
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID"""
        return self.workspaces.get(workspace_id)
    
    def get_workspace_by_name(self, name: str) -> Optional[Workspace]:
        """Get workspace by name"""
        workspace_id = self.workspace_index.get(name)
        return self.workspaces.get(workspace_id) if workspace_id else None
    
    def update_workspace(self, workspace_id: str, **kwargs) -> bool:
        """Update workspace information"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        for key, value in kwargs.items():
            if hasattr(workspace, key):
                setattr(workspace, key, value)
        
        workspace.updated_at = datetime.now()
        return True
    
    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete workspace"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        
        # Remove from index
        if workspace.name in self.workspace_index:
            del self.workspace_index[workspace.name]
        
        # Remove from workspaces
        del self.workspaces[workspace_id]
        
        return True
    
    def list_workspaces(self, status: WorkspaceStatus = None) -> List[Workspace]:
        """List workspaces with optional status filter"""
        workspaces = list(self.workspaces.values())
        if status:
            workspaces = [ws for ws in workspaces if ws.status == status]
        return workspaces
    
    def get_workspaces_by_type(self, workspace_type: WorkspaceType) -> List[Workspace]:
        """Get workspaces by type"""
        return [ws for ws in self.workspaces.values() if ws.workspace_type == workspace_type]
    
    def get_workspaces_by_user(self, user_id: str) -> List[Workspace]:
        """Get workspaces for a specific user"""
        return [ws for ws in self.workspaces.values() if user_id in ws.members]
    
    def get_workspaces_by_admin(self, user_id: str) -> List[Workspace]:
        """Get workspaces where user is admin"""
        return [ws for ws in self.workspaces.values() if user_id in ws.admins]
    
    def validate_workspace_access(self, user_id: str, workspace_id: str) -> bool:
        """Validate user access to workspace"""
        workspace = self.get_workspace(workspace_id)
        return workspace and (user_id in workspace.members or user_id == workspace.owner_id)
    
    def audit_workspace_activity(self, workspace_id: str, user_id: str, 
                               action: str, details: Dict = None) -> None:
        """Log workspace activity for audit purposes"""
        workspace = self.get_workspace(workspace_id)
        if workspace:
            audit_entry = {
                "workspace_id": workspace_id,
                "workspace_name": workspace.name,
                "user_id": user_id,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "details": details or {}
            }
            workspace.add_audit_log(action, details)
            # In a real implementation, this would write to a central audit log
            print(f"Audit: {audit_entry}")
    
    def get_workspace_stats(self) -> Dict:
        """Get workspace statistics"""
        total_workspaces = len(self.workspaces)
        active_workspaces = len([ws for ws in self.workspaces.values() if ws.is_active()])
        archived_workspaces = len([ws for ws in self.workspaces.values() if ws.status == WorkspaceStatus.ARCHIVED])
        
        member_counts = [ws.get_member_count() for ws in self.workspaces.values()]
        skill_counts = [ws.get_skill_count() for ws in self.workspaces.values()]
        
        return {
            "total_workspaces": total_workspaces,
            "active_workspaces": active_workspaces,
            "archived_workspaces": archived_workspaces,
            "avg_members_per_workspace": sum(member_counts) / len(member_counts) if member_counts else 0,
            "avg_skills_per_workspace": sum(skill_counts) / len(skill_counts) if skill_counts else 0,
            "workspace_types": {ws_type.value: len([ws for ws in self.workspaces.values() if ws.workspace_type == ws_type]) 
                              for ws_type in WorkspaceType}
        }