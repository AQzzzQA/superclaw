"""
Permission Service for Skill Management System
Handles permission validation, role management, and access control.
"""

import yaml
import json
from typing import Dict, List, Optional, Set
from datetime import datetime

from ..models.User import User, UserRole
from ..models.Workspace import Workspace, WorkspaceType
from ..models.Skill import Skill, SkillCategory, SkillAccessLevel


class PermissionService:
    """Service for managing permissions and access control"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.permissions_config = self._load_permissions_config()
        self.roles_config = self._load_roles_config()
        self.permission_cache = {}
        self.permission_cache_ttl = 3600  # 1 hour
        
    def _load_permissions_config(self) -> Dict:
        """Load permissions configuration from YAML file"""
        try:
            with open(self.config_path or '/root/.openclaw/workspace/skill-management-system/config/permissions.yaml', 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_permissions_config()
    
    def _load_roles_config(self) -> Dict:
        """Load roles configuration from YAML file"""
        try:
            with open(self.config_path or '/root/.openclaw/workspace/skill-management-system/config/roles.yaml', 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_roles_config()
    
    def _get_default_permissions_config(self) -> Dict:
        """Get default permissions configuration"""
        return {
            'global_permissions': {
                'admin': {
                    'description': 'System administrator with full access',
                    'permissions': [
                        'create_workspace', 'delete_workspace', 'manage_users',
                        'manage_all_skills', 'view_all_logs', 'manage_system_config'
                    ]
                },
                'user': {
                    'description': 'Regular user with basic permissions',
                    'permissions': [
                        'view_workspace', 'install_skills', 'uninstall_skills',
                        'view_own_logs', 'view_available_skills'
                    ]
                }
            },
            'skill_permissions': {
                'system': {
                    'required_level': 'admin',
                    'max_users': 5
                },
                'business': {
                    'required_level': 'workspace_admin',
                    'max_users': 20
                },
                'general': {
                    'required_level': 'user',
                    'max_users': 100
                }
            }
        }
    
    def _get_default_roles_config(self) -> Dict:
        """Get default roles configuration"""
        return {
            'roles': {
                'system_admin': {
                    'name': 'System Administrator',
                    'level': 'system',
                    'permissions': [
                        'system_config', 'user_management', 'workspace_management',
                        'skill_management', 'audit_management'
                    ]
                },
                'user': {
                    'name': 'Standard User',
                    'level': 'standard',
                    'permissions': [
                        'view_workspace', 'install_skills', 'use_skills',
                        'view_skill_documentation'
                    ]
                }
            }
        }
    
    def get_user_permissions(self, user: User) -> Set[str]:
        """Get all permissions for a user based on roles"""
        cache_key = f"user_{user.user_id}_permissions"
        
        # Check cache
        if cache_key in self.permission_cache:
            cached_result = self.permission_cache[cache_key]
            if cached_result['timestamp'] > datetime.now().timestamp() - self.permission_cache_ttl:
                return set(cached_result['permissions'])
        
        # Get permissions from roles
        permissions = set()
        
        # Add direct permissions from user's primary role
        primary_role_config = self.roles_config['roles'].get(user.role.value, {})
        if 'permissions' in primary_role_config:
            permissions.update(primary_role_config['permissions'])
        
        # Add permissions from additional roles
        for role in user.roles:
            role_config = self.roles_config['roles'].get(role.value, {})
            if 'permissions' in role_config:
                permissions.update(role_config['permissions'])
        
        # Add inheritance permissions
        permissions = self._apply_inheritance(permissions, user.role, user.roles)
        
        # Cache result
        self.permission_cache[cache_key] = {
            'permissions': list(permissions),
            'timestamp': datetime.now().timestamp()
        }
        
        return permissions
    
    def _apply_inheritance(self, permissions: Set[str], primary_role: UserRole, 
                          additional_roles: List[UserRole]) -> Set[str]:
        """Apply role inheritance to permissions"""
        inheritance_rules = self.roles_config.get('inheritance', {})
        
        # Get inheritance chain for primary role
        if primary_role.value in inheritance_rules:
            inheritance = inheritance_rules[primary_role.value]
            if 'inherits' in inheritance:
                for inherited_role in inheritance['inherits']:
                    role_config = self.roles_config['roles'].get(inherited_role, {})
                    if 'permissions' in role_config:
                        permissions.update(role_config['permissions'])
        
        # Get inheritance for additional roles
        for role in additional_roles:
            if role.value in inheritance_rules:
                inheritance = inheritance_rules[role.value]
                if 'inherits' in inheritance:
                    for inherited_role in inheritance['inherits']:
                        role_config = self.roles_config['roles'].get(inherited_role, {})
                        if 'permissions' in role_config:
                            permissions.update(role_config['permissions'])
        
        return permissions
    
    def has_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        user_permissions = self.get_user_permissions(user)
        return permission in user_permissions
    
    def can_access_workspace(self, user: User, workspace: Workspace) -> bool:
        """Check if user can access workspace"""
        # System admins can access all workspaces
        if user.role == UserRole.SYSTEM_ADMIN:
            return True
        
        # Workspace owners can access their workspaces
        if workspace.owner_id == user.user_id:
            return True
        
        # Workspace admins can access their workspaces
        if user.user_id in workspace.admins:
            return True
        
        # Members can access their workspaces
        if user.user_id in workspace.members:
            return True
        
        # Check if workspace is public
        if workspace.workspace_type == WorkspaceType.INDIVIDUAL:
            return False  # Individual workspaces are not public
        
        return False
    
    def can_manage_workspace(self, user: User, workspace: Workspace) -> bool:
        """Check if user can manage workspace"""
        # System admins can manage all workspaces
        if user.role == UserRole.SYSTEM_ADMIN:
            return True
        
        # Workspace owners can manage their workspaces
        if workspace.owner_id == user.user_id:
            return True
        
        # Workspace admins can manage their workspaces
        if user.user_id in workspace.admins:
            return True
        
        return False
    
    def can_install_skill(self, user: User, skill: Skill, workspace: Workspace) -> Dict:
        """Check if user can install skill in workspace"""
        result = {
            'can_install': False,
            'reason': None,
            'permissions_needed': []
        }
        
        # Check if user can access workspace
        if not self.can_access_workspace(user, workspace):
            result['reason'] = 'User cannot access workspace'
            return result
        
        # Check if user has permission to install skills
        install_permission = 'install_skills' if workspace.workspace_type == WorkspaceType.INDIVIDUAL else 'install_workspace_skills'
        if not self.has_permission(user, install_permission):
            result['reason'] = f'Required permission: {install_permission}'
            result['permissions_needed'].append(install_permission)
            return result
        
        # Check skill-specific permissions
        skill_category = skill.category.value
        if skill_category in self.permissions_config['skill_permissions']:
            skill_perm = self.permissions_config['skill_permissions'][skill_category]
            required_level = skill_perm.get('required_level', 'user')
            
            # Check if user meets required level
            if not self._meets_required_level(user, required_level):
                result['reason'] = f'Required level: {required_level}'
                result['permissions_needed'].append(f'require_level_{required_level}')
                return result
        
        # Check skill access level
        if skill.access_level == SkillAccessLevel.RESTRICTED:
            # Check if user is skill owner
            if user.user_id not in skill.owners:
                result['reason'] = 'Skill access is restricted'
                result['permissions_needed'].append('skill_owner_access')
                return result
        
        # Check workspace skill limits
        max_skills = workspace.get_constraint('max_skills') or 100
        if len(workspace.skills) >= max_skills:
            result['reason'] = f'Workspace skill limit reached: {max_skills}'
            return result
        
        # Check user skill limits
        max_user_skills = user.get_constraint('max_skills') or 50
        user_skill_count = len([s_id for s_id in user.skill_usage.keys() 
                              if self._skill_in_workspace(s_id, workspace)])
        if user_skill_count >= max_user_skills:
            result['reason'] = f'User skill limit reached: {max_user_skills}'
            return result
        
        result['can_install'] = True
        return result
    
    def _meets_required_level(self, user: User, required_level: str) -> bool:
        """Check if user meets required level for skill"""
        level_hierarchy = {
            'viewer': 1,
            'user': 2,
            'business_user': 3,
            'developer': 4,
            'analyst': 4,
            'manager': 5,
            'workspace_admin': 6,
            'system_admin': 7
        }
        
        user_level = level_hierarchy.get(user.role.value, 0)
        required_level_value = level_hierarchy.get(required_level, 0)
        
        return user_level >= required_level_value
    
    def _skill_in_workspace(self, skill_id: str, workspace: Workspace) -> bool:
        """Check if skill exists in workspace"""
        return skill_id in workspace.skills
    
    def can_uninstall_skill(self, user: User, skill: Skill, workspace: Workspace) -> Dict:
        """Check if user can uninstall skill from workspace"""
        result = {
            'can_uninstall': False,
            'reason': None
        }
        
        # Check if user can access workspace
        if not self.can_access_workspace(user, workspace):
            result['reason'] = 'User cannot access workspace'
            return result
        
        # Check if user has permission to uninstall skills
        uninstall_permission = 'uninstall_skills' if workspace.workspace_type == WorkspaceType.INDIVIDUAL else 'uninstall_workspace_skills'
        if not self.has_permission(user, uninstall_permission):
            result['reason'] = f'Required permission: {uninstall_permission}'
            return result
        
        # Check if skill is actually installed in workspace
        if skill.skill_id not in workspace.skills:
            result['reason'] = 'Skill is not installed in workspace'
            return result
        
        result['can_uninstall'] = True
        return result
    
    def get_skill_requirements(self, skill: Skill) -> Dict:
        """Get skill installation requirements"""
        category = skill.category.value
        if category in self.permissions_config['skill_permissions']:
            return self.permissions_config['skill_permissions'][category]
        return {}
    
    def validate_skill_installation_preconditions(self, user: User, skill: Skill, 
                                                  workspace: Workspace) -> Dict:
        """Validate preconditions for skill installation"""
        result = {
            'valid': True,
            'violations': []
        }
        
        # Check skill status
        if skill.status.value == 'banned':
            result['valid'] = False
            result['violations'].append({
                'type': 'skill_status',
                'message': 'Skill is banned',
                'severity': 'critical'
            })
        
        # Check skill dependencies
        for dependency in skill.dependencies:
            # Check if dependency is available
            # In a real implementation, this would check the skill registry
            if not self._is_dependency_available(dependency):
                result['valid'] = False
                result['violations'].append({
                    'type': 'dependency',
                    'message': f'Missing dependency: {dependency}',
                    'severity': 'high'
                })
        
        # Check workspace constraints
        if not workspace.check_constraint('max_skills', len(workspace.skills) + 1):
            result['valid'] = False
            result['violations'].append({
                'type': 'workspace_constraint',
                'message': 'Workspace skill limit exceeded',
                'severity': 'medium'
            })
        
        # Check user constraints
        if not user.check_constraint('max_skills', len(user.skill_usage) + 1):
            result['valid'] = False
            result['violations'].append({
                'type': 'user_constraint',
                'message': 'User skill limit exceeded',
                'severity': 'medium'
            })
        
        return result
    
    def _is_dependency_available(self, dependency: str) -> bool:
        """Check if skill dependency is available"""
        # In a real implementation, this would check the skill registry
        # For now, return True as a placeholder
        return True
    
    def audit_permission_check(self, user: User, permission: str, resource: str, 
                              result: bool, reason: str = None) -> None:
        """Log permission checks for audit purposes"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user.user_id,
            'user_email': user.email,
            'permission': permission,
            'resource': resource,
            'result': result,
            'reason': reason
        }
        # In a real implementation, this would write to an audit log
        print(f"Permission Audit: {audit_entry}")
    
    def clear_permission_cache(self) -> None:
        """Clear permission cache"""
        self.permission_cache.clear()
    
    def get_permission_summary(self, user: User) -> Dict:
        """Get permission summary for user"""
        permissions = self.get_user_permissions(user)
        
        summary = {
            'user_id': user.user_id,
            'user_role': user.role.value,
            'additional_roles': [role.value for role in user.roles],
            'total_permissions': len(permissions),
            'permissions': list(permissions),
            'workspace_permissions': [],
            'skill_permissions': []
        }
        
        # Categorize permissions
        for perm in permissions:
            if perm.startswith('workspace_'):
                summary['workspace_permissions'].append(perm)
            elif perm.startswith('skill_'):
                summary['skill_permissions'].append(perm)
            else:
                summary['permissions'].append(perm)
        
        return summary