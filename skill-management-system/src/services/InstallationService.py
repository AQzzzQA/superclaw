"""
Installation Service for Skill Management System
Handles skill installation, uninstallation, and dependency management.
"""

import json
import shutil
import subprocess
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import threading
import time

from ..models.User import User
from ..models.Workspace import Workspace
from ..models.Skill import Skill, SkillCategory, SkillAccessLevel
from .PermissionService import PermissionService


class InstallationService:
    """Service for managing skill installations"""
    
    def __init__(self, permission_service: PermissionService, 
                 base_path: str = "/root/.openclaw/workspace/skill-management-system"):
        self.permission_service = permission_service
        self.base_path = base_path
        self.installation_queue = []
        self.installation_status = {}
        self.lock = threading.Lock()
        self.max_concurrent_installations = 3
        self.installation_timeout = 3600  # 1 hour
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for skill installation"""
        directories = [
            f"{self.base_path}/data/skills",
            f"{self.base_path}/data/skills/installed",
            f"{self.base_path}/data/skills/pending",
            f"{self.base_path}/data/skills/failed",
            f"{self.base_path}/data/installation_logs",
            f"{self.base_path}/data/skill_cache"
        ]
        
        for directory in directories:
            try:
                import os
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
    
    def install_skill(self, user: User, skill: Skill, workspace: Workspace, 
                    version: str = None, config: Dict = None) -> Dict:
        """Install a skill in a workspace"""
        result = {
            'success': False,
            'message': None,
            'installation_id': None,
            'progress': 0,
            'logs': []
        }
        
        # Validate installation preconditions
        validation_result = self.permission_service.validate_skill_installation_preconditions(
            user, skill, workspace
        )
        
        if not validation_result['valid']:
            result['message'] = f"Installation validation failed: {validation_result['violations']}"
            return result
        
        # Check if user can install skill
        permission_result = self.permission_service.can_install_skill(user, skill, workspace)
        if not permission_result['can_install']:
            result['message'] = f"Cannot install skill: {permission_result['reason']}"
            return result
        
        # Create installation record
        installation_id = self._create_installation_record(user, skill, workspace, version, config)
        
        # Add to installation queue
        with self.lock:
            self.installation_queue.append({
                'id': installation_id,
                'user_id': user.user_id,
                'skill_id': skill.skill_id,
                'workspace_id': workspace.workspace_id,
                'version': version or skill.version,
                'config': config or {},
                'status': 'pending',
                'created_at': datetime.now(),
                'started_at': None,
                'completed_at': None,
                'progress': 0,
                'logs': []
            })
        
        result['installation_id'] = installation_id
        result['message'] = "Skill added to installation queue"
        
        # Start installation process
        self._start_installation_process()
        
        return result
    
    def _create_installation_record(self, user: User, skill: Skill, workspace: Workspace, 
                                   version: str, config: Dict) -> str:
        """Create installation record"""
        import uuid
        installation_id = str(uuid.uuid4())
        
        record = {
            'installation_id': installation_id,
            'user_id': user.user_id,
            'skill_id': skill.skill_id,
            'workspace_id': workspace.workspace_id,
            'skill_name': skill.name,
            'version': version or skill.version,
            'config': config or {},
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'progress': 0,
            'logs': []
        }
        
        # Save installation record
        try:
            with open(f"{self.base_path}/data/skills/pending/{installation_id}.json", 'w') as f:
                json.dump(record, f, indent=2)
        except Exception as e:
            print(f"Error saving installation record: {e}")
        
        return installation_id
    
    def _start_installation_process(self):
        """Start the installation process"""
        def install_worker():
            while True:
                with self.lock:
                    # Check if we can start more installations
                    active_installations = len([inst for inst in self.installation_queue 
                                             if inst['status'] == 'running'])
                    
                    if active_installations >= self.max_concurrent_installations:
                        break
                    
                    # Get next pending installation
                    pending_installations = [inst for inst in self.installation_queue 
                                           if inst['status'] == 'pending']
                    if not pending_installations:
                        break
                    
                    installation = pending_installations[0]
                    installation['status'] = 'running'
                    installation['started_at'] = datetime.now()
                    
                    # Start installation in background
                    threading.Thread(
                        target=self._perform_installation,
                        args=(installation['id'],),
                        daemon=True
                    ).start()
                
                time.sleep(1)  # Check every second
        
        # Start worker thread if not already running
        if not hasattr(self, '_worker_thread') or not self._worker_thread.is_alive():
            self._worker_thread = threading.Thread(target=install_worker, daemon=True)
            self._worker_thread.start()
    
    def _perform_installation(self, installation_id: str):
        """Perform actual skill installation"""
        try:
            # Load installation record
            record_path = f"{self.base_path}/data/skills/pending/{installation_id}.json"
            with open(record_path, 'r') as f:
                installation_record = json.load(f)
            
            # Update status
            installation_record['status'] = 'running'
            installation_record['progress'] = 10
            self._save_installation_record(installation_record)
            
            # Simulate installation steps
            steps = [
                {'step': 'validation', 'progress': 20, 'message': 'Validating skill requirements'},
                {'step': 'download', 'progress': 40, 'message': 'Downloading skill dependencies'},
                {'step': 'extraction', 'progress': 60, 'message': 'Extracting skill files'},
                {'step': 'configuration', 'progress': 80, 'message': 'Configuring skill'},
                {'step': 'initialization', 'progress': 90, 'message': 'Initializing skill'},
                {'step': 'completion', 'progress': 100, 'message': 'Installation completed'}
            ]
            
            for step in steps:
                # Update progress
                installation_record['progress'] = step['progress']
                installation_record['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'level': 'info',
                    'message': step['message']
                })
                self._save_installation_record(installation_record)
                
                # Simulate work
                time.sleep(2)
                
                # Check for timeout
                if (datetime.now() - datetime.fromisoformat(installation_record['started_at'])).seconds > self.installation_timeout:
                    raise Exception("Installation timeout")
            
            # Mark as completed
            installation_record['status'] = 'completed'
            installation_record['completed_at'] = datetime.now().isoformat()
            installation_record['progress'] = 100
            installation_record['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'level': 'success',
                'message': 'Installation completed successfully'
            })
            self._save_installation_record(installation_record)
            
            # Move to installed directory
            shutil.move(record_path, f"{self.base_path}/data/skills/installed/{installation_id}.json")
            
        except Exception as e:
            # Mark as failed
            try:
                with open(record_path, 'r') as f:
                    installation_record = json.load(f)
                
                installation_record['status'] = 'failed'
                installation_record['completed_at'] = datetime.now().isoformat()
                installation_record['progress'] = installation_record['progress']
                installation_record['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'level': 'error',
                    'message': f'Installation failed: {str(e)}'
                })
                self._save_installation_record(installation_record)
                
                # Move to failed directory
                shutil.move(record_path, f"{self.base_path}/data/skills/failed/{installation_id}.json")
                
            except Exception as move_error:
                print(f"Error handling failed installation: {move_error}")
        
        finally:
            # Remove from queue
            with self.lock:
                self.installation_queue = [inst for inst in self.installation_queue 
                                        if inst['id'] != installation_id]
    
    def _save_installation_record(self, record: Dict):
        """Save installation record"""
        record_path = f"{self.base_path}/data/skills/pending/{record['installation_id']}.json"
        with open(record_path, 'w') as f:
            json.dump(record, f, indent=2)
    
    def uninstall_skill(self, user: User, skill: Skill, workspace: Workspace) -> Dict:
        """Uninstall a skill from a workspace"""
        result = {
            'success': False,
            'message': None,
            'uninstallation_id': None,
            'progress': 0,
            'logs': []
        }
        
        # Check if user can uninstall skill
        permission_result = self.permission_service.can_uninstall_skill(user, skill, workspace)
        if not permission_result['can_uninstall']:
            result['message'] = f"Cannot uninstall skill: {permission_result['reason']}"
            return result
        
        # Find installed skill
        installed_skill = self._find_installed_skill(skill.skill_id, workspace.workspace_id)
        if not installed_skill:
            result['message'] = "Skill is not installed in workspace"
            return result
        
        # Create uninstallation record
        import uuid
        uninstallation_id = str(uuid.uuid4())
        
        record = {
            'uninstallation_id': uninstallation_id,
            'user_id': user.user_id,
            'skill_id': skill.skill_id,
            'workspace_id': workspace.workspace_id,
            'skill_name': skill.name,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'progress': 0,
            'logs': []
        }
        
        # Save uninstallation record
        try:
            with open(f"{self.base_path}/data/skills/uninstalling/{uninstallation_id}.json", 'w') as f:
                json.dump(record, f, indent=2)
        except Exception as e:
            print(f"Error saving uninstallation record: {e}")
        
        # Start uninstallation process
        threading.Thread(
            target=self._perform_uninstallation,
            args=(uninstallation_id,),
            daemon=True
        ).start()
        
        result['uninstallation_id'] = uninstallation_id
        result['message'] = "Skill added to uninstallation queue"
        
        return result
    
    def _find_installed_skill(self, skill_id: str, workspace_id: str) -> Optional[Dict]:
        """Find installed skill record"""
        import glob
        pattern = f"{self.base_path}/data/skills/installed/*{skill_id}*"
        
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    if record.get('workspace_id') == workspace_id:
                        return record
            except Exception as e:
                print(f"Error reading skill record: {e}")
        
        return None
    
    def _perform_uninstallation(self, uninstallation_id: str):
        """Perform actual skill uninstallation"""
        try:
            # Load uninstallation record
            record_path = f"{self.base_path}/data/skills/uninstalling/{uninstallation_id}.json"
            with open(record_path, 'r') as f:
                uninstallation_record = json.load(f)
            
            # Update status
            uninstallation_record['status'] = 'running'
            uninstallation_record['progress'] = 10
            self._save_uninstallation_record(uninstallation_record)
            
            # Simulate uninstallation steps
            steps = [
                {'step': 'validation', 'progress': 20, 'message': 'Validating uninstall requirements'},
                {'step': 'cleanup', 'progress': 40, 'message': 'Cleaning up skill files'},
                {'step': 'configuration_removal', 'progress': 60, 'message': 'Removing configuration'},
                {'step': 'dependency_cleanup', 'progress': 80, 'message': 'Cleaning up dependencies'},
                {'step': 'completion', 'progress': 100, 'message': 'Uninstallation completed'}
            ]
            
            for step in steps:
                # Update progress
                uninstallation_record['progress'] = step['progress']
                uninstallation_record['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'level': 'info',
                    'message': step['message']
                })
                self._save_uninstallation_record(uninstallation_record)
                
                # Simulate work
                time.sleep(1)
            
            # Mark as completed
            uninstallation_record['status'] = 'completed'
            uninstallation_record['completed_at'] = datetime.now().isoformat()
            uninstallation_record['progress'] = 100
            uninstallation_record['logs'].append({
                'timestamp': datetime.now().isoformat(),
                'level': 'success',
                'message': 'Uninstallation completed successfully'
            })
            self._save_uninstallation_record(uninstallation_record)
            
            # Remove skill record
            skill_path = f"{self.base_path}/data/skills/installed/{uninstallation_id}.json"
            import os
            if os.path.exists(skill_path):
                os.remove(skill_path)
            
        except Exception as e:
            # Mark as failed
            try:
                with open(record_path, 'r') as f:
                    uninstallation_record = json.load(f)
                
                uninstallation_record['status'] = 'failed'
                uninstallation_record['completed_at'] = datetime.now().isoformat()
                uninstallation_record['progress'] = uninstallation_record['progress']
                uninstallation_record['logs'].append({
                    'timestamp': datetime.now().isoformat(),
                    'level': 'error',
                    'message': f'Uninstallation failed: {str(e)}'
                })
                self._save_uninstallation_record(uninstallation_record)
                
            except Exception as move_error:
                print(f"Error handling failed uninstallation: {move_error}")
        
        finally:
            # Clean up uninstallation record
            import os
            if os.path.exists(record_path):
                os.remove(record_path)
    
    def _save_uninstallation_record(self, record: Dict):
        """Save uninstallation record"""
        record_path = f"{self.base_path}/data/skills/uninstalling/{record['uninstallation_id']}.json"
        with open(record_path, 'w') as f:
            json.dump(record, f, indent=2)
    
    def get_installation_status(self, installation_id: str) -> Dict:
        """Get installation status"""
        # Check pending installations
        for record in self.installation_queue:
            if record['id'] == installation_id:
                return {
                    'status': record['status'],
                    'progress': record['progress'],
                    'created_at': record['created_at'],
                    'started_at': record['started_at'],
                    'completed_at': record['completed_at'],
                    'logs': record['logs']
                }
        
        # Check completed installations
        import glob
        pattern = f"{self.base_path}/data/skills/installed/{installation_id}.json"
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    return {
                        'status': record['status'],
                        'progress': record['progress'],
                        'created_at': record['created_at'],
                        'started_at': record['started_at'],
                        'completed_at': record['completed_at'],
                        'logs': record['logs']
                    }
            except Exception as e:
                print(f"Error reading installation record: {e}")
        
        # Check failed installations
        pattern = f"{self.base_path}/data/skills/failed/{installation_id}.json"
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    return {
                        'status': record['status'],
                        'progress': record['progress'],
                        'created_at': record['created_at'],
                        'started_at': record['started_at'],
                        'completed_at': record['completed_at'],
                        'logs': record['logs']
                    }
            except Exception as e:
                print(f"Error reading failed installation record: {e}")
        
        return {'status': 'not_found', 'message': 'Installation not found'}
    
    def get_workspace_skills(self, workspace_id: str) -> List[Dict]:
        """Get all skills installed in a workspace"""
        skills = []
        import glob
        pattern = f"{self.base_path}/data/skills/installed/*{workspace_id}*"
        
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    skills.append({
                        'skill_id': record['skill_id'],
                        'skill_name': record['skill_name'],
                        'version': record['version'],
                        'installed_at': record['created_at'],
                        'status': record['status']
                    })
            except Exception as e:
                print(f"Error reading skill record: {e}")
        
        return skills
    
    def get_user_installations(self, user_id: str) -> List[Dict]:
        """Get all installations for a user"""
        installations = []
        
        # Check active installations
        for record in self.installation_queue:
            if record['user_id'] == user_id:
                installations.append({
                    'installation_id': record['id'],
                    'skill_name': record.get('skill_name', 'Unknown'),
                    'workspace_id': record['workspace_id'],
                    'status': record['status'],
                    'progress': record['progress'],
                    'created_at': record['created_at']
                })
        
        # Check completed installations
        import glob
        pattern = f"{self.base_path}/data/skills/installed/*"
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    if record['user_id'] == user_id:
                        installations.append({
                            'installation_id': record['installation_id'],
                            'skill_name': record['skill_name'],
                            'workspace_id': record['workspace_id'],
                            'status': record['status'],
                            'progress': record['progress'],
                            'created_at': record['created_at']
                        })
            except Exception as e:
                print(f"Error reading installation record: {e}")
        
        return installations
    
    def cancel_installation(self, installation_id: str) -> Dict:
        """Cancel a pending installation"""
        with self.lock:
            for i, record in enumerate(self.installation_queue):
                if record['id'] == installation_id:
                    if record['status'] == 'pending':
                        # Remove from queue
                        del self.installation_queue[i]
                        
                        # Cancel record
                        record['status'] = 'cancelled'
                        record['completed_at'] = datetime.now().isoformat()
                        
                        # Save record
                        try:
                            with open(f"{self.base_path}/data/skills/failed/{installation_id}.json", 'w') as f:
                                json.dump(record, f, indent=2)
                        except Exception as e:
                            print(f"Error saving cancelled installation record: {e}")
                        
                        return {'success': True, 'message': 'Installation cancelled'}
                    else:
                        return {'success': False, 'message': 'Cannot cancel running installation'}
        
        return {'success': False, 'message': 'Installation not found'}
    
    def get_system_stats(self) -> Dict:
        """Get system installation statistics"""
        import glob
        import os
        
        stats = {
            'pending_installations': len([f for f in glob.glob(f"{self.base_path}/data/skills/pending/*.json")]),
            'installed_skills': len([f for f in glob.glob(f"{self.base_path}/data/skills/installed/*.json")]),
            'failed_installations': len([f for f in glob.glob(f"{self.base_path}/data/skills/failed/*.json")]),
            'active_installations': len([inst for inst in self.installation_queue if inst['status'] == 'running']),
            'pending_queue_size': len([inst for inst in self.installation_queue if inst['status'] == 'pending']),
            'total_disk_usage': self._get_total_disk_usage(),
            'average_installation_time': self._get_average_installation_time()
        }
        
        return stats
    
    def _get_total_disk_usage(self) -> int:
        """Get total disk usage for skills"""
        total_size = 0
        import os
        
        for root, dirs, files in os.walk(f"{self.base_path}/data/skills"):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        
        return total_size
    
    def _get_average_installation_time(self) -> float:
        """Get average installation time"""
        import glob
        
        total_time = 0
        count = 0
        
        pattern = f"{self.base_path}/data/skills/installed/*.json"
        for file_path in glob.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                    if record.get('started_at') and record.get('completed_at'):
                        start_time = datetime.fromisoformat(record['started_at'])
                        end_time = datetime.fromisoformat(record['completed_at'])
                        total_time += (end_time - start_time).total_seconds()
                        count += 1
            except Exception as e:
                print(f"Error reading installation time: {e}")
        
        return total_time / count if count > 0 else 0