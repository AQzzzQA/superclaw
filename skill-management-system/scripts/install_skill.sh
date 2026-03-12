#!/bin/bash

# Skill Management System - Skill Installation Script
# This script installs a skill in a specified workspace

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load configuration
CONFIG_FILE="$PROJECT_DIR/config/permissions.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Load environment variables
source "$PROJECT_DIR/.env" 2>/dev/null || true

# Default values
WORKSPACE_NAME=""
SKILL_NAME=""
SKILL_VERSION=""
USER_EMAIL=""
CONFIG_FILE=""
FORCE=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--workspace)
            WORKSPACE_NAME="$2"
            shift 2
            ;;
        -s|--skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        -v|--version)
            SKILL_VERSION="$2"
            shift 2
            ;;
        -u|--user)
            USER_EMAIL="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Install a skill in the specified workspace."
            echo ""
            echo "Options:"
            echo "  -w, --workspace NAME      Workspace name (required)"
            echo "  -s, --skill NAME         Skill name (required)"
            echo "  -v, --version VERSION    Skill version (optional, uses latest if not specified)"
            echo "  -u, --user EMAIL         User email performing installation (required)"
            echo "  -c, --config FILE        Configuration file path (optional)"
            echo "  -f, --force              Force installation even if skill exists"
            echo "  -v, --verbose            Enable verbose output"
            echo "  -h, --help               Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information."
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$WORKSPACE_NAME" ]; then
    echo "Error: Workspace name is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

if [ -z "$SKILL_NAME" ]; then
    echo "Error: Skill name is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

if [ -z "$USER_EMAIL" ]; then
    echo "Error: User email is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

# Check if workspace exists
WORKSPACE_FILE="$PROJECT_DIR/data/workspaces/$WORKSPACE_NAME.json"
if [ ! -f "$WORKSPACE_FILE" ]; then
    echo "Error: Workspace '$WORKSPACE_NAME' does not exist"
    exit 1
fi

# Check if skill exists (in real implementation, this would check skill registry)
SKILL_FILE="$PROJECT_DIR/data/skills/$SKILL_NAME.json"
if [ ! -f "$SKILL_FILE" ] && [ "$FORCE" != true ]; then
    echo "Error: Skill '$SKILL_NAME' not found"
    echo "Use -f or --force to proceed anyway."
    exit 1
}

# Load configuration if specified
SKILL_CONFIG=""
if [ -n "$CONFIG_FILE" ]; then
    if [ -f "$CONFIG_FILE" ]; then
        SKILL_CONFIG=$(cat "$CONFIG_FILE")
    else
        echo "Error: Configuration file '$CONFIG_FILE' not found"
        exit 1
    fi
fi

# Get skill information (in real implementation, this would fetch from registry)
SKILL_DATA=$(cat << EOF
{
  "skill_id": "$(uuidgen)",
  "name": "$SKILL_NAME",
  "description": "Sample skill for installation",
  "category": "general",
  "status": "active",
  "access_level": "public",
  "version": "$SKILL_VERSION",
  "versions": {
    "$SKILL_VERSION": {
      "changelog": "Initial version",
      "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    }
  },
  "author": "system",
  "maintainer": "system",
  "owners": [],
  "contributors": [],
  "dependencies": [],
  "requirements": {},
  "permissions": {},
  "constraints": {},
  "installation_requirements": {},
  "uninstallation_requirements": {},
  "config_schema": {},
  "default_config": {},
  "documentation": {},
  "example_usage": {},
  "changelog": [],
  "tags": [],
  "rating": 0.0,
  "rating_count": 0,
  "download_count": 0,
  "installation_count": 0,
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "metadata": {
    "installation_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  }
}
EOF
)

# Create installation record
INSTALLATION_ID=$(uuidgen)
INSTALLATION_DATA=$(cat << EOF
{
  "installation_id": "$INSTALLATION_ID",
  "workspace_name": "$WORKSPACE_NAME",
  "skill_name": "$SKILL_NAME",
  "skill_version": "$SKILL_VERSION",
  "user_email": "$USER_EMAIL",
  "config": $SKILL_CONFIG,
  "status": "pending",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "started_at": null,
  "completed_at": null,
  "progress": 0,
  "logs": []
}
EOF
)

# Create installation directory
INSTALLATION_DIR="$PROJECT_DIR/data/skills/pending"
mkdir -p "$INSTALLATION_DIR"

# Save installation record
echo "$INSTALLATION_DATA" > "$INSTALLATION_DIR/$INSTALLATION_ID.json"

# Start installation process
cd "$PROJECT_DIR"
python3 -c "
import sys
sys.path.append('src')
from models.User import User, UserManager
from models.Workspace import Workspace, WorkspaceManager
from models.Skill import Skill, SkillManager
from services.PermissionService import PermissionService
from services.InstallationService import InstallationService
import json

# Initialize managers
user_manager = UserManager()
workspace_manager = WorkspaceManager()
skill_manager = SkillManager()
permission_service = PermissionService()
installation_service = InstallationService(permission_service)

# Get workspace
workspace = workspace_manager.get_workspace_by_name('$WORKSPACE_NAME')
if not workspace:
    print('Error: Workspace not found')
    sys.exit(1)

# Get user (in real implementation, this would be properly authenticated)
user = user_manager.get_user_by_email('$USER_EMAIL')
if not user:
    print('Error: User not found')
    sys.exit(1)

# Parse skill data
skill_data = '''$SKILL_DATA'''
skill_dict = json.loads(skill_data)
skill = Skill.from_dict(skill_dict)

# Parse configuration
config = {}
if '''$SKILL_CONFIG''':
    config = json.loads('''$SKILL_CONFIG''')

# Install skill
result = installation_service.install_skill(user, skill, workspace, '''$SKILL_VERSION''', config)

print(f'Installation started successfully!')
print(f'Installation ID: {result[\"installation_id\"]}')
print(f'Status: {result[\"message\"]}')

# Log installation start
audit_data = {
    'timestamp': json.loads('''$INSTALLATION_DATA''')['created_at'],
    'action': 'install_skill',
    'user': '$USER_EMAIL',
    'workspace': '$WORKSPACE_NAME',
    'skill': '$SKILL_NAME',
    'version': '$SKILL_VERSION',
    'installation_id': '$INSTALLATION_ID',
    'status': 'started'
}

with open('$PROJECT_DIR/data/audit/skill_installation_$(date -u +"%Y%m%d_%H%M%S").json', 'w') as f:
    json.dump(audit_data, f, indent=2)
"

# Display progress if verbose mode is enabled
if [ "$VERBOSE" = true ]; then
    echo ""
    echo "Installation started. You can check progress using:"
    echo "./scripts/installation_status.sh $INSTALLATION_ID"
    echo ""
    
    # Monitor installation progress
    echo "Monitoring installation progress..."
    while true; do
        sleep 5
        STATUS=$(python3 -c "
import sys
sys.path.append('$PROJECT_DIR/src')
from services.InstallationService import InstallationService
service = InstallationService(None)
status = service.get_installation_status('$INSTALLATION_ID')
print(status.get('status', 'unknown'))
")
        
        if [ "$STATUS" = "completed" ]; then
            echo "✓ Installation completed successfully!"
            break
        elif [ "$STATUS" = "failed" ]; then
            echo "✗ Installation failed!"
            break
        elif [ "$STATUS" = "cancelled" ]; then
            echo "⚠ Installation cancelled!"
            break
        fi
        
        echo "Current status: $STATUS"
    done
fi

# Display success message
echo ""
echo "✓ Skill installation started successfully!"
echo ""
echo "Installation Details:"
echo "  Workspace: $WORKSPACE_NAME"
echo "  Skill: $SKILL_NAME"
echo "  Version: $SKILL_VERSION"
echo "  User: $USER_EMAIL"
echo "  Installation ID: $INSTALLATION_ID"
echo ""
echo "Installation record saved to: $INSTALLATION_DIR/$INSTALLATION_ID.json"
echo ""

# Show next steps
echo "Next steps:"
echo "1. Check installation progress: ./scripts/installation_status.sh $INSTALLATION_ID"
echo "2. View installed skills: ./scripts/workspace_skills.sh $WORKSPACE_NAME"
echo "3. Monitor installation logs: ./scripts/installation_logs.sh $INSTALLATION_ID"
echo ""

exit 0