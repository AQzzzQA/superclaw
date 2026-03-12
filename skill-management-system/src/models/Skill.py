"""
Skill Model for Skill Management System
Represents a skill with permissions, versions, and installation status.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from enum import Enum


class SkillStatus(Enum):
    """Skill status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PENDING = "pending"
    BANNED = "banned"


class SkillCategory(Enum):
    """Skill category enumeration"""
    SYSTEM = "system"
    BUSINESS = "business"
    DEVELOPMENT = "development"
    GENERAL = "general"
    SECURITY = "security"
    INTEGRATION = "integration"
    ANALYTICS = "analytics"
    COMMUNICATION = "communication"


class SkillAccessLevel(Enum):
    """Skill access level enumeration"""
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"
    INTERNAL = "internal"


class Skill:
    """Skill model representing a skill"""
    
    def __init__(self, skill_id: str = None, name: str = None, description: str = None):
        self.skill_id = skill_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.category = SkillCategory.GENERAL
        self.status = SkillStatus.PENDING
        self.access_level = SkillAccessLevel.PUBLIC
        self.version = "1.0.0"
        self.versions = {}
        self.author = None
        self.maintainer = None
        self.owners = []
        self.contributors = []
        self.dependencies = []
        self.requirements = {}
        self.permissions = {}
        self.constraints = {}
        self.installation_requirements = {}
        self.uninstallation_requirements = {}
        self.config_schema = {}
        self.default_config = {}
        self.documentation = {}
        self.example_usage = {}
        self.changelog = []
        self.tags = []
        self.rating = 0.0
        self.rating_count = 0
        self.download_count = 0
        self.installation_count = 0
        self.last_updated = datetime.now()
        self.created_at = datetime.now()
        self.metadata = {}
        
    def to_dict(self) -> Dict:
        """Convert skill to dictionary"""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "status": self.status.value,
            "access_level": self.access_level.value,
            "version": self.version,
            "versions": self.versions,
            "author": self.author,
            "maintainer": self.maintainer,
            "owners": self.owners,
            "contributors": self.contributors,
            "dependencies": self.dependencies,
            "requirements": self.requirements,
            "permissions": self.permissions,
            "constraints": self.constraints,
            "installation_requirements": self.installation_requirements,
            "uninstallation_requirements": self.uninstallation_requirements,
            "config_schema": self.config_schema,
            "default_config": self.default_config,
            "documentation": self.documentation,
            "example_usage": self.example_usage,
            "changelog": self.changelog,
            "tags": self.tags,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "download_count": self.download_count,
            "installation_count": self.installation_count,
            "last_updated": self.last_updated.isoformat(),
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Skill':
        """Create skill from dictionary"""
        skill = cls(
            skill_id=data.get("skill_id"),
            name=data.get("name"),
            description=data.get("description")
        )
        skill.category = SkillCategory(data.get("category", "general"))
        skill.status = SkillStatus(data.get("status", "pending"))
        skill.access_level = SkillAccessLevel(data.get("access_level", "public"))
        skill.version = data.get("version", "1.0.0")
        skill.versions = data.get("versions", {})
        skill.author = data.get("author")
        skill.maintainer = data.get("maintainer")
        skill.owners = data.get("owners", [])
        skill.contributors = data.get("contributors", [])
        skill.dependencies = data.get("dependencies", [])
        skill.requirements = data.get("requirements", {})
        skill.permissions = data.get("permissions", {})
        skill.constraints = data.get("constraints", {})
        skill.installation_requirements = data.get("installation_requirements", {})
        skill.uninstallation_requirements = data.get("uninstallation_requirements", {})
        skill.config_schema = data.get("config_schema", {})
        skill.default_config = data.get("default_config", {})
        skill.documentation = data.get("documentation", {})
        skill.example_usage = data.get("example_usage", {})
        skill.changelog = data.get("changelog", [])
        skill.tags = data.get("tags", [])
        skill.rating = data.get("rating", 0.0)
        skill.rating_count = data.get("rating_count", 0)
        skill.download_count = data.get("download_count", 0)
        skill.installation_count = data.get("installation_count", 0)
        skill.last_updated = datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else datetime.now()
        skill.created_at = datetime.fromisoformat(data["created_at"])
        skill.metadata = data.get("metadata", {})
        return skill
    
    def add_version(self, version: str, changelog: str = None) -> None:
        """Add new version of skill"""
        self.versions[version] = {
            "changelog": changelog or "",
            "timestamp": datetime.now().isoformat()
        }
        self.version = version
        self.last_updated = datetime.now()
    
    def is_compatible(self, requirements: Dict) -> bool:
        """Check if skill meets compatibility requirements"""
        # Check version requirements
        if "min_version" in requirements and self.version < requirements["min_version"]:
            return False
        
        if "max_version" in requirements and self.version > requirements["max_version"]:
            return False
        
        # Check category requirements
        if "required_categories" in requirements:
            required_categories = requirements["required_categories"]
            if self.category.value not in required_categories:
                return False
        
        # Check access level requirements
        if "required_access_level" in requirements:
            required_access = requirements["required_access_level"]
            if self.access_level.value not in required_access:
                return False
        
        # Check dependency requirements
        if "required_dependencies" in requirements:
            required_deps = requirements["required_dependencies"]
            for dep in required_deps:
                if dep not in self.dependencies:
                    return False
        
        return True
    
    def can_install(self, user_id: str, user_roles: Set[str], 
                   installation_limits: Dict) -> Dict:
        """Check if skill can be installed by user"""
        result = {
            "can_install": True,
            "reason": None,
            "requirements": []
        }
        
        # Check skill status
        if self.status == SkillStatus.BANNED:
            result["can_install"] = False
            result["reason"] = "Skill is banned"
            return result
        
        if self.status == SkillStatus.DEPRECATED:
            result["can_install"] = False
            result["reason"] = "Skill is deprecated"
            return result
        
        # Check access level
        if self.access_level == SkillLevel.RESTRICTED and user_id not in self.owners:
            result["can_install"] = False
            result["reason"] = "Skill access is restricted"
            return result
        
        # Check installation limits
        if "max_installations" in installation_limits:
            max_installations = installation_limits["max_installations"]
            if self.installation_count >= max_installations:
                result["can_install"] = False
                result["reason"] = f"Skill installation limit reached ({max_installations})"
                return result
        
        # Check user role requirements
        if "required_roles" in self.permissions:
            required_roles = self.permissions["required_roles"]
            if not any(role in user_roles for role in required_roles):
                result["can_install"] = False
                result["reason"] = f"Required roles: {required_roles}"
                return result
        
        # Check dependency requirements
        if "required_dependencies" in self.requirements:
            for dep in self.requirements["required_dependencies"]:
                result["requirements"].append(f"Dependency: {dep}")
        
        # Check resource requirements
        if "required_resources" in self.requirements:
            resources = self.requirements["required_resources"]
            for resource, requirement in resources.items():
                result["requirements"].append(f"Resource: {resource} >= {requirement}")
        
        return result
    
    def add_rating(self, rating: float) -> None:
        """Add rating to skill"""
        if 1 <= rating <= 5:
            total_rating = self.rating * self.rating_count + rating
            self.rating_count += 1
            self.rating = total_rating / self.rating_count
            self.last_updated = datetime.now()
    
    def increment_download_count(self) -> None:
        """Increment download count"""
        self.download_count += 1
        self.last_updated = datetime.now()
    
    def increment_installation_count(self) -> None:
        """Increment installation count"""
        self.installation_count += 1
        self.last_updated = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add tag to skill"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.last_updated = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove tag from skill"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.last_updated = datetime.now()
    
    def set_owner(self, user_id: str) -> None:
        """Set skill owner"""
        if user_id not in self.owners:
            self.owners.append(user_id)
            self.last_updated = datetime.now()
    
    def add_contributor(self, user_id: str) -> None:
        """Add contributor to skill"""
        if user_id not in self.contributors:
            self.contributors.append(user_id)
            self.last_updated = datetime.now()
    
    def remove_contributor(self, user_id: str) -> None:
        """Remove contributor from skill"""
        if user_id in self.contributors:
            self.contributors.remove(user_id)
            self.last_updated = datetime.now()
    
    def update_documentation(self, section: str, content: str) -> None:
        """Update skill documentation"""
        self.documentation[section] = content
        self.last_updated = datetime.now()
    
    def add_changelog_entry(self, version: str, changes: str) -> None:
        """Add changelog entry"""
        self.changelog.append({
            "version": version,
            "changes": changes,
            "timestamp": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def get_compatibility_info(self) -> Dict:
        """Get skill compatibility information"""
        return {
            "current_version": self.version,
            "available_versions": list(self.versions.keys()),
            "minimum_version": self.requirements.get("minimum_version"),
            "maximum_version": self.requirements.get("maximum_version"),
            "supported_platforms": self.requirements.get("supported_platforms", []),
            "required_dependencies": self.dependencies,
            "optional_dependencies": self.requirements.get("optional_dependencies", [])
        }
    
    def get_installation_stats(self) -> Dict:
        """Get skill installation statistics"""
        return {
            "total_installations": self.installation_count,
            "total_downloads": self.download_count,
            "average_rating": self.rating,
            "rating_count": self.rating_count,
            "category": self.category.value,
            "status": self.status.value
        }
    
    def to_json(self) -> str:
        """Convert skill to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Skill':
        """Create skill from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class SkillManager:
    """Manager class for skill operations"""
    
    def __init__(self):
        self.skills = {}
        self.skill_index = {}  # Name to skill_id mapping
        self.category_index = {}  # Category to skill_ids mapping
        self.tag_index = {}  # Tag to skill_ids mapping
    
    def create_skill(self, name: str, description: str, category: SkillCategory = SkillCategory.GENERAL,
                    author: str = None) -> Skill:
        """Create a new skill"""
        skill = Skill(name=name, description=description)
        skill.category = category
        skill.author = author
        skill.status = SkillStatus.ACTIVE
        
        self.skills[skill.skill_id] = skill
        self.skill_index[name] = skill.skill_id
        
        # Update category index
        if category.value not in self.category_index:
            self.category_index[category.value] = []
        self.category_index[category.value].append(skill.skill_id)
        
        return skill
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get skill by ID"""
        return self.skills.get(skill_id)
    
    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """Get skill by name"""
        skill_id = self.skill_index.get(name)
        return self.skills.get(skill_id) if skill_id else None
    
    def update_skill(self, skill_id: str, **kwargs) -> bool:
        """Update skill information"""
        skill = self.get_skill(skill_id)
        if not skill:
            return False
        
        for key, value in kwargs.items():
            if hasattr(skill, key):
                setattr(skill, key, value)
        
        skill.last_updated = datetime.now()
        return True
    
    def delete_skill(self, skill_id: str) -> bool:
        """Delete skill"""
        skill = self.get_skill(skill_id)
        if not skill:
            return False
        
        # Remove from index
        if skill.name in self.skill_index:
            del self.skill_index[skill.name]
        
        # Remove from category index
        if skill.category.value in self.category_index:
            if skill_id in self.category_index[skill.category.value]:
                self.category_index[skill.category.value].remove(skill_id)
        
        # Remove from tag index
        for tag in skill.tags:
            if tag in self.tag_index and skill_id in self.tag_index[tag]:
                self.tag_index[tag].remove(skill_id)
        
        # Remove from skills
        del self.skills[skill_id]
        
        return True
    
    def list_skills(self, status: SkillStatus = None, category: SkillCategory = None) -> List[Skill]:
        """List skills with optional filters"""
        skills = list(self.skills.values())
        if status:
            skills = [skill for skill in skills if skill.status == status]
        if category:
            skills = [skill for skill in skills if skill.category == category]
        return skills
    
    def get_skills_by_category(self, category: SkillCategory) -> List[Skill]:
        """Get skills by category"""
        skill_ids = self.category_index.get(category.value, [])
        return [self.skills[skill_id] for skill_id in skill_ids if skill_id in self.skills]
    
    def get_skills_by_tag(self, tag: str) -> List[Skill]:
        """Get skills by tag"""
        skill_ids = self.tag_index.get(tag, [])
        return [self.skills[skill_id] for skill_id in skill_ids if skill_id in self.skills]
    
    def get_skills_by_author(self, author: str) -> List[Skill]:
        """Get skills by author"""
        return [skill for skill in self.skills.values() if skill.author == author]
    
    def search_skills(self, query: str, category: SkillCategory = None, 
                     access_level: SkillAccessLevel = None) -> List[Skill]:
        """Search skills by query"""
        query = query.lower()
        results = []
        
        for skill in self.skills.values():
            # Apply filters
            if category and skill.category != category:
                continue
            if access_level and skill.access_level != access_level:
                continue
            
            # Check if query matches
            if (query in skill.name.lower() or 
                query in skill.description.lower() or
                any(query in tag.lower() for tag in skill.tags)):
                results.append(skill)
        
        return results
    
    def validate_skill_installation(self, skill_id: str, user_id: str, 
                                   user_roles: Set[str], installation_limits: Dict) -> Dict:
        """Validate skill installation for user"""
        skill = self.get_skill(skill_id)
        if not skill:
            return {"can_install": False, "reason": "Skill not found"}
        
        return skill.can_install(user_id, user_roles, installation_limits)
    
    def audit_skill_activity(self, skill_id: str, user_id: str, 
                           action: str, details: Dict = None) -> None:
        """Log skill activity for audit purposes"""
        skill = self.get_skill(skill_id)
        if skill:
            audit_entry = {
                "skill_id": skill_id,
                "skill_name": skill.name,
                "user_id": user_id,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "details": details or {}
            }
            # In a real implementation, this would write to a central audit log
            print(f"Audit: {audit_entry}")
    
    def get_skill_stats(self) -> Dict:
        """Get skill statistics"""
        total_skills = len(self.skills)
        active_skills = len([skill for skill in self.skills.values() if skill.status == SkillStatus.ACTIVE])
        deprecated_skills = len([skill for skill in self.skills.values() if skill.status == SkillStatus.DEPRECATED])
        banned_skills = len([skill for skill in self.skills.values() if skill.status == SkillStatus.BANNED])
        
        category_stats = {}
        for category in SkillCategory:
            category_stats[category.value] = len(self.get_skills_by_category(category))
        
        return {
            "total_skills": total_skills,
            "active_skills": active_skills,
            "deprecated_skills": deprecated_skills,
            "banned_skills": banned_skills,
            "category_distribution": category_stats,
            "average_rating": sum(skill.rating for skill in self.skills.values()) / total_skills if total_skills > 0 else 0,
            "total_installations": sum(skill.installation_count for skill in self.skills.values()),
            "total_downloads": sum(skill.download_count for skill in self.skills.values())
        }