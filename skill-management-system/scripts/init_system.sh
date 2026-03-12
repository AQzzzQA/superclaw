#!/bin/bash

# Skill Management System - System Initialization Script
# This script initializes the skill management system with basic setup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Initializing Skill Management System..."
echo "========================================"

# Create necessary directories
echo "📁 Creating directory structure..."
DIRECTORIES=(
    "$PROJECT_DIR/data"
    "$PROJECT_DIR/data/users"
    "$PROJECT_DIR/data/workspaces"
    "$PROJECT_DIR/data/skills"
    "$PROJECT_DIR/data/skills/installed"
    "$PROJECT_DIR/data/skills/pending"
    "$PROJECT_DIR/data/skills/failed"
    "$PROJECT_DIR/data/skills/uninstalling"
    "$PROJECT_DIR/data/audit"
    "$PROJECT_DIR/data/cache"
    "$PROJECT_DIR/logs"
    "$PROJECT_DIR/config"
    "$PROJECT_DIR/scripts"
    "$PROJECT_DIR/src"
    "$PROJECT_DIR/src/models"
    "$PROJECT_DIR/src/services"
    "$PROJECT_DIR/src/utils"
    "$PROJECT_DIR/tests"
    "$PROJECT_DIR/tests/unit"
    "$PROJECT_DIR/tests/integration"
    "$PROJECT_DIR/tests/fixtures"
)

for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "✓ Created: $dir"
    else
        echo "✓ Already exists: $dir"
    fi
done

# Copy configuration files if they don't exist
echo "📋 Setting up configuration files..."

if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo "✓ Created .env from .env.example"
    echo "⚠️  Please review and update .env with your configuration"
else
    echo "✓ .env already exists"
fi

# Create system database (SQLite for development)
echo "🗄️  Setting up database..."
if [ ! -f "$PROJECT_DIR/data/skills.db" ]; then
    sqlite3 "$PROJECT_DIR/data/skills.db" << EOF
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_login TEXT,
    preferences TEXT,
    constraints TEXT
);

-- Create workspaces table
CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    workspace_type TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    admins TEXT,
    members TEXT,
    config TEXT,
    constraints TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_activity TEXT,
    tags TEXT,
    metadata TEXT
);

-- Create skills table
CREATE TABLE IF NOT EXISTS skills (
    skill_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    access_level TEXT NOT NULL,
    version TEXT NOT NULL,
    author TEXT,
    maintainer TEXT,
    owners TEXT,
    contributors TEXT,
    dependencies TEXT,
    requirements TEXT,
    permissions TEXT,
    constraints TEXT,
    config_schema TEXT,
    default_config TEXT,
    documentation TEXT,
    tags TEXT,
    rating REAL,
    rating_count INTEGER,
    download_count INTEGER,
    installation_count INTEGER,
    last_updated TEXT NOT NULL,
    created_at TEXT NOT NULL,
    metadata TEXT
);

-- Create skill installations table
CREATE TABLE IF NOT EXISTS skill_installations (
    installation_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    version TEXT NOT NULL,
    config TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    progress INTEGER,
    logs TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- Create audit log table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id TEXT,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    details TEXT,
    ip_address TEXT,
    user_agent TEXT,
    status TEXT NOT NULL
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_workspaces_owner ON workspaces(owner_id);
CREATE INDEX IF NOT EXISTS idx_workspaces_type ON workspaces(workspace_type);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);
CREATE INDEX IF NOT EXISTS idx_skills_status ON skills(status);
CREATE INDEX IF NOT EXISTS idx_installations_user ON skill_installations(user_id);
CREATE INDEX IF NOT EXISTS idx_installations_workspace ON skill_installations(workspace_id);
CREATE INDEX IF NOT EXISTS idx_installations_status ON skill_installations(status);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);

-- Insert initial admin user
INSERT OR IGNORE INTO users (user_id, email, name, role, status, created_at, updated_at)
VALUES ('admin', 'admin@skill-management.com', 'System Administrator', 'system_admin', 'active', datetime('now'), datetime('now'));

-- Insert initial system workspace
INSERT OR IGNORE INTO workspaces (workspace_id, name, description, status, workspace_type, owner_id, admins, members, config, created_at, updated_at)
VALUES ('system-workspace', 'System', 'System administration workspace', 'active', 'organization', 'admin', '["admin"]', '["admin"]', '{"auto_create_user_directories": true, "enable_email_notifications": true, "enable_audit_logging": true}', datetime('now'), datetime('now'));

EOF
    echo "✓ Created SQLite database with initial data"
else
    echo "✓ Database already exists"
fi

# Create initial skill registry
echo "🔧 Setting up initial skills..."
if [ ! -f "$PROJECT_DIR/data/skills/system-monitor.json" ]; then
    # Create system monitor skill
    cat > "$PROJECT_DIR/data/skills/system-monitor.json" << EOF
{
  "skill_id": "system-monitor",
  "name": "System Monitor",
  "description": "Monitor system performance and health",
  "category": "system",
  "status": "active",
  "access_level": "internal",
  "version": "1.0.0",
  "versions": {
    "1.0.0": {
      "changelog": "Initial release",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
  },
  "author": "system",
  "maintainer": "system",
  "owners": ["admin"],
  "contributors": [],
  "dependencies": [],
  "requirements": {
    "minimum_version": "1.0.0",
    "supported_platforms": ["linux", "windows", "macos"]
  },
  "permissions": {
    "required_roles": ["system_admin"],
    "required_permissions": ["system_monitoring"]
  },
  "constraints": {
    "max_instances": 1,
    "requires_approval": true
  },
  "installation_requirements": {},
  "uninstallation_requirements": {},
  "config_schema": {
    "monitoring_interval": {
      "type": "integer",
      "default": 60,
      "min": 30,
      "max": 3600,
      "description": "Monitoring interval in seconds"
    },
    "enable_alerts": {
      "type": "boolean",
      "default": true,
      "description": "Enable monitoring alerts"
    }
  },
  "default_config": {
    "monitoring_interval": 60,
    "enable_alerts": true
  },
  "documentation": {
    "description": "A comprehensive system monitoring skill that tracks system performance metrics.",
    "usage": "The skill monitors CPU usage, memory usage, disk space, and network statistics.",
    "examples": [
      "monitor start - Start monitoring",
      "monitor stop - Stop monitoring",
      "monitor status - Check monitoring status"
    ]
  },
  "example_usage": {
    "start": "system-monitor start",
    "stop": "system-monitor stop",
    "status": "system-monitor status",
    "config": "system-monitor config --monitoring-interval 30 --enable-alerts true"
  },
  "changelog": [
    {
      "version": "1.0.0",
      "changes": "Initial release with basic system monitoring",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
  ],
  "tags": ["system", "monitoring", "performance"],
  "rating": 0.0,
  "rating_count": 0,
  "download_count": 0,
  "installation_count": 0,
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "metadata": {
    "system_skill": true,
    "critical": true,
    "maintenance_required": false
  }
}
EOF
    echo "✓ Created system-monitor skill"
fi

if [ ! -f "$PROJECT_DIR/data/skills/backup-manager.json" ]; then
    # Create backup manager skill
    cat > "$PROJECT_DIR/data/skills/backup-manager.json" << EOF
{
  "skill_id": "backup-manager",
  "name": "Backup Manager",
  "description": "Manage system backups and restore operations",
  "category": "system",
  "status": "active",
  "access_level": "internal",
  "version": "1.0.0",
  "versions": {
    "1.0.0": {
      "changelog": "Initial release",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
  },
  "author": "system",
  "maintainer": "system",
  "owners": ["admin"],
  "contributors": [],
  "dependencies": [],
  "requirements": {
    "minimum_version": "1.0.0",
    "supported_platforms": ["linux", "windows", "macos"]
  },
  "permissions": {
    "required_roles": ["system_admin"],
    "required_permissions": ["system_backup"]
  },
  "constraints": {
    "max_instances": 1,
    "requires_approval": true,
    "backup_required": true,
    "retention_days": 90
  },
  "installation_requirements": {
    "required_space": "10GB"
  },
  "uninstallation_requirements": {
    "confirm_backup": true
  },
  "config_schema": {
    "backup_schedule": {
      "type": "string",
      "default": "0 2 * * *",
      "description": "Cron schedule for backups"
    },
    "retention_days": {
      "type": "integer",
      "default": 90,
      "min": 7,
      "max": 365,
      "description": "Number of days to keep backups"
    },
    "compression": {
      "type": "boolean",
      "default": true,
      "description": "Enable backup compression"
    }
  },
  "default_config": {
    "backup_schedule": "0 2 * * *",
    "retention_days": 90,
    "compression": true
  },
  "documentation": {
    "description": "A comprehensive backup management skill that handles automated backups and restore operations.",
    "usage": "The skill supports scheduled backups, manual backups, and restore operations.",
    "examples": [
      "backup create - Create backup",
      "backup list - List available backups",
      "backup restore - Restore from backup",
      "backup schedule --cron '0 2 * * *' - Set backup schedule"
    ]
  },
  "example_usage": {
    "create": "backup-manager create",
    "list": "backup-manager list",
    "restore": "backup-manager restore --backup-id 20240101-120000",
    "schedule": "backup-manager schedule --cron '0 2 * * *'"
  },
  "changelog": [
    {
      "version": "1.0.0",
      "changes": "Initial release with backup management capabilities",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
  ],
  "tags": ["system", "backup", "restore", "data-protection"],
  "rating": 0.0,
  "rating_count": 0,
  "download_count": 0,
  "installation_count": 0,
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "metadata": {
    "system_skill": true,
    "critical": true,
    "data_protection": true
  }
}
EOF
    echo "✓ Created backup-manager skill"
fi

# Create initial user
echo "👤 Creating initial admin user..."
if [ ! -f "$PROJECT_DIR/data/users/admin.json" ]; then
    cat > "$PROJECT_DIR/data/users/admin.json" << EOF
{
  "user_id": "admin",
  "email": "admin@skill-management.com",
  "name": "System Administrator",
  "status": "active",
  "role": "system_admin",
  "roles": ["system_admin"],
  "permissions": [
    "system_config",
    "user_management",
    "workspace_management",
    "skill_management",
    "audit_management",
    "view_all_workspaces",
    "manage_all_skills",
    "view_all_logs",
    "create_workspace",
    "delete_workspace",
    "manage_users"
  ],
  "workspaces": ["system-workspace"],
  "skill_usage": {},
  "last_login": null,
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "constraints": {
    "max_skills": 100,
    "max_workspaces": 10,
    "max_installations_per_hour": 50
  },
  "preferences": {
    "theme": "dark",
    "language": "en",
    "notifications": true,
    "email_notifications": true
  },
  "notification_settings": {
    "email": true,
    "push": false,
    "sms": false
  }
}
EOF
    echo "✓ Created admin user"
fi

# Set up Python environment
echo "🐍 Setting up Python environment..."
if command -v python3 &> /dev/null; then
    # Create requirements.txt if it doesn't exist
    if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
        cat > "$PROJECT_DIR/requirements.txt" << EOF
# Core dependencies
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.1

# Database
sqlite3  # Built-in
psycopg2-binary==2.9.9  # PostgreSQL
aiosqlite==0.19.0  # Async SQLite

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Configuration
python-dotenv==1.0.0
pyyaml==6.0.1

# Utilities
click==8.1.7
rich==13.7.0
typer==0.9.0
requests==2.31.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0
mypy==1.7.1
pre-commit==3.6.0

# Logging
structlog==23.2.0
colorlog==6.8.0

# Monitoring
prometheus-client==0.19.0
psutil==5.9.6

# Optional dependencies for enhanced features
redis==5.0.1
celery==5.3.4
flower==2.0.1
sentry-sdk==1.39.1
EOF
        echo "✓ Created requirements.txt"
    fi

    # Create virtual environment if it doesn't exist
    if [ ! -d "$PROJECT_DIR/venv" ]; then
        python3 -m venv "$PROJECT_DIR/venv"
        echo "✓ Created Python virtual environment"
        
        # Activate virtual environment and install dependencies
        source "$PROJECT_DIR/venv/bin/activate"
        pip install --upgrade pip
        pip install -r "$PROJECT_DIR/requirements.txt"
        echo "✓ Installed Python dependencies"
    else
        echo "✓ Virtual environment already exists"
    fi
else
    echo "⚠️  Python3 not found. Please install Python 3.8+ to use the full functionality."
fi

# Create system service file (optional)
echo "🔄 Setting up system service..."
if [ -d "/etc/systemd/system" ]; then
    # Create systemd service file
    cat > "$PROJECT_DIR/skill-management.service" << EOF
[Unit]
Description=Skill Management System
After=network.target

[Service]
Type=exec
User=root
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    echo "✓ Created systemd service file (skill-management.service)"
    echo "  To install: sudo cp $PROJECT_DIR/skill-management.service /etc/systemd/system/"
    echo "  To enable: sudo systemctl enable skill-management"
    echo "  To start: sudo systemctl start skill-management"
fi

# Create basic API endpoints
echo "🌐 Setting up API endpoints..."
if [ ! -d "$PROJECT_DIR/src/api" ]; then
    mkdir -p "$PROJECT_DIR/src/api"
    
    # Create main API file
    cat > "$PROJECT_DIR/src/api/main.py" << EOF
"""
Skill Management System - Main API Entry Point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.User import User, UserManager
from models.Workspace import Workspace, WorkspaceManager
from models.Skill import Skill, SkillManager
from services.PermissionService import PermissionService
from services.InstallationService import InstallationService

# Initialize managers
user_manager = UserManager()
workspace_manager = WorkspaceManager()
skill_manager = SkillManager()
permission_service = PermissionService()
installation_service = InstallationService(permission_service)

# Create FastAPI app
app = FastAPI(
    title="Skill Management System API",
    description="API for managing skills, workspaces, and users",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Skill Management System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

# User endpoints
@app.post("/users")
async def create_user(user_data: Dict[str, Any]):
    """Create a new user"""
    try:
        user = user_manager.create_user(
            email=user_data["email"],
            name=user_data["name"],
            role=user_data.get("role", "user")
        )
        return {"success": True, "user": user.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    user = user_manager.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "user": user.to_dict()}

# Workspace endpoints
@app.post("/workspaces")
async def create_workspace(workspace_data: Dict[str, Any]):
    """Create a new workspace"""
    try:
        workspace = workspace_manager.create_workspace(
            name=workspace_data["name"],
            description=workspace_data.get("description"),
            workspace_type=workspace_data.get("workspace_type", "team"),
            owner_id=workspace_data.get("owner_id")
        )
        return {"success": True, "workspace": workspace.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str):
    """Get workspace by ID"""
    workspace = workspace_manager.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"success": True, "workspace": workspace.to_dict()}

@app.get("/workspaces/{workspace_id}/skills")
async def get_workspace_skills(workspace_id: str):
    """Get skills in workspace"""
    skills = installation_service.get_workspace_skills(workspace_id)
    return {"success": True, "skills": skills}

# Skill endpoints
@app.post("/skills")
async def create_skill(skill_data: Dict[str, Any]):
    """Create a new skill"""
    try:
        skill = skill_manager.create_skill(
            name=skill_data["name"],
            description=skill_data.get("description"),
            category=skill_data.get("category", "general"),
            author=skill_data.get("author")
        )
        return {"success": True, "skill": skill.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/skills/{skill_id}")
async def get_skill(skill_id: str):
    """Get skill by ID"""
    skill = skill_manager.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"success": True, "skill": skill.to_dict()}

@app.get("/skills")
async def list_skills(category: str = None, status: str = None):
    """List skills with optional filters"""
    skills = skill_manager.list_skills(
        category=category if category else None,
        status=status if status else None
    )
    return {"success": True, "skills": [skill.to_dict() for skill in skills]}

# Installation endpoints
@app.post("/skills/install")
async def install_skill(install_data: Dict[str, Any]):
    """Install a skill"""
    try:
        # This would require proper authentication and user context
        # For now, return a placeholder response
        return {
            "success": True,
            "message": "Skill installation initiated",
            "installation_id": "placeholder-id"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/skills/{skill_id}")
async def uninstall_skill(skill_id: str):
    """Uninstall a skill"""
    try:
        # This would require proper authentication and user context
        # For now, return a placeholder response
        return {
            "success": True,
            "message": "Skill uninstallation initiated"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# System endpoints
@app.get("/system/stats")
async def get_system_stats():
    """Get system statistics"""
    user_stats = {
        "total_users": len(user_manager.users),
        "active_users": len([u for u in user_manager.users.values() if u.is_active()])
    }
    
    workspace_stats = workspace_manager.get_workspace_stats()
    
    skill_stats = skill_manager.get_skill_stats()
    
    installation_stats = installation_service.get_system_stats()
    
    return {
        "success": True,
        "stats": {
            "users": user_stats,
            "workspaces": workspace_stats,
            "skills": skill_stats,
            "installations": installation_stats
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF
    echo "✓ Created basic API endpoints"
fi

# Create test files
echo "🧪 Setting up test files..."
if [ ! -f "$PROJECT_DIR/tests/test_basic.py" ]; then
    cat > "$PROJECT_DIR/tests/test_basic.py" << EOF
"""
Basic tests for Skill Management System
"""

import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.User import User, UserManager
from models.Workspace import Workspace, WorkspaceManager
from models.Skill import Skill, SkillManager

def test_user_creation():
    """Test user creation"""
    user_manager = UserManager()
    user = user_manager.create_user(
        email="test@example.com",
        name="Test User",
        role="user"
    )
    
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.role.value == "user"
    assert user.is_active()

def test_workspace_creation():
    """Test workspace creation"""
    workspace_manager = WorkspaceManager()
    workspace = workspace_manager.create_workspace(
        name="Test Workspace",
        description="Test workspace",
        workspace_type="team",
        owner_id="test@example.com"
    )
    
    assert workspace.name == "Test Workspace"
    assert workspace.description == "Test workspace"
    assert workspace.workspace_type.value == "team"
    assert workspace.owner_id == "test@example.com"
    assert workspace.is_active()

def test_skill_creation():
    """Test skill creation"""
    skill_manager = SkillManager()
    skill = skill_manager.create_skill(
        name="Test Skill",
        description="Test skill",
        category="general",
        author="test@example.com"
    )
    
    assert skill.name == "Test Skill"
    assert skill.description == "Test skill"
    assert skill.category.value == "general"
    assert skill.author == "test@example.com"
    assert skill.status.value == "active"

if __name__ == "__main__":
    pytest.main([__file__])
EOF
    echo "✓ Created basic test file"
fi

# Create README for the system
echo "📚 Creating system documentation..."
cat > "$PROJECT_DIR/GETTING_STARTED.md" << EOF
# Skill Management System - Getting Started

## Overview
The Skill Management System is a comprehensive platform for managing AI skills, workspaces, and user permissions. It provides workspace creation, user binding, skill installation limits, permission management, and user-based skill installation control.

## Quick Start

### 1. System Initialization
Run the initialization script to set up the system:
\`\`\`bash
./scripts/init_system.sh
\`\`\`

### 2. Create Your First Workspace
\`\`\`bash
./scripts/create_workspace.sh \\
  --name "my-team" \\
  --description "My development team workspace" \\
  --type "team" \\
  --owner admin@skill-management.com \\
  --admin dev1@skill-management.com \\
  --admin dev2@skill-management.com
\`\`\`

### 3. Add Users
\`\`\`bash
./scripts/manage_users.sh add dev1@skill-management.com my-team developer
./scripts/manage_users.sh add dev2@skill-management.com my-team user
\`\`\`

### 4. Install Skills
\`\`\`bash
./scripts/install_skill.sh \\
  --workspace "my-team" \\
  --skill "code-analyzer" \\
  --user dev1@skill-management.com
\`\`\`

### 5. Check Permissions
\`\`\`bash
./scripts/check_permissions.sh \\
  --user dev1@skill-management.com \\
  --resource workspace \\
  --name "my-team" \\
  --action install
\`\`\`

## Configuration

### Environment Variables
Copy \`.env.example\` to \`.env\` and configure your settings:

\`\`\`
# Database Configuration
DATABASE_URL=sqlite:///./data/skills.db

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
\`\`\`

### Configuration Files
The system uses YAML configuration files for different aspects:

- \`config/permissions.yaml\` - Permission definitions
- \`config/limits.yaml\` - Installation limits
- \`config/workspaces.yaml\` - Workspace configurations
- \`config/roles.yaml\` - Role definitions

## API Usage

### Start the API Server
\`\`\`bash
source venv/bin/activate
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080
\`\`\`

### Example API Calls

#### Create a workspace
\`\`\`bash
curl -X POST "http://localhost:8080/workspaces" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "my-workspace",
    "description": "My workspace",
    "workspace_type": "team",
    "owner_id": "admin@skill-management.com"
  }'
\`\`\`

#### Get workspace skills
\`\`\`bash
curl "http://localhost:8080/workspaces/workspace-id-123/skills"
\`\`\`

#### List all skills
\`\`\`bash
curl "http://localhost:8080/skills"
\`\`\`

## Scripts Reference

### create_workspace.sh
Create a new workspace with specified configuration.

**Usage:**
\`\`\`bash
./scripts/create_workspace.sh [OPTIONS]
\`\`\`

**Options:**
- \`-n, --name NAME\` - Workspace name (required)
- \`-d, --description DESC\` - Workspace description
- \`-t, --type TYPE\` - Workspace type
- \`-o, --owner EMAIL\` - Owner email (required)
- \`-a, --admin EMAIL\` - Additional admin emails
- \`-f, --force\` - Force creation
- \`-v, --verbose\` - Verbose output

### install_skill.sh
Install a skill in a specified workspace.

**Usage:**
\`\`\`bash
./scripts/install_skill.sh [OPTIONS]
\`\`\`

**Options:**
- \`-w, --workspace NAME\` - Workspace name (required)
- \`-s, --skill NAME\` - Skill name (required)
- \`-v, --version VERSION\` - Skill version
- \`-u, --user EMAIL\` - User email (required)
- \`-c, --config FILE\` - Configuration file
- \`-f, --force\` - Force installation
- \`-v, --verbose\` - Verbose output

### check_permissions.sh
Check user permissions for accessing resources.

**Usage:**
\`\`\`bash
./scripts/check_permissions.sh [OPTIONS]
\`\`\`

**Options:**
- \`-u, --user EMAIL\` - User email (required)
- \`-r, --resource TYPE\` - Resource type (required)
- \`-n, --name NAME\` - Resource name
- \`-a, --action ACTION\` - Action to check (required)
- \`-v, --verbose\` - Verbose output
- \`-j, --json\` - JSON output

## Architecture

### Core Components
1. **User Management** - User authentication, roles, and permissions
2. **Workspace Management** - Workspace creation and configuration
3. **Skill Management** - Skill registry and version control
4. **Installation Service** - Skill installation and dependency management
5. **Permission Service** - Access control and authorization

### Data Models
- **User** - Represents system users with roles and permissions
- **Workspace** - Represents workspaces with users and skills
- **Skill** - Represents AI skills with metadata and versions

### Services
- **PermissionService** - Handles permission validation and access control
- **InstallationService** - Manages skill installation and uninstallation

## Testing

Run tests with pytest:
\`\`\`bash
source venv/bin/activate
pytest tests/
\`\`\`

## Monitoring

The system provides comprehensive monitoring and logging:

- **Audit Logs** - All actions are logged for security and compliance
- **Performance Metrics** - Track system performance and usage
- **Error Tracking** - Monitor and alert on errors
- **Health Checks** - System health monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please refer to the documentation or create an issue in the repository.
EOF
    echo "✓ Created getting started documentation"

echo ""
echo "🎉 Skill Management System initialization completed!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Review and update .env file with your configuration"
echo "2. Create your first workspace: ./scripts/create_workspace.sh --name my-team --owner your-email@example.com"
echo "3. Start the API server: source venv/bin/activate && python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8080"
echo "4. Check the documentation: cat GETTING_STARTED.md"
echo ""
echo "System is ready to use! 🚀"