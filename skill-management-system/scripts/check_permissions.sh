#!/bin/bash

# Skill Management System - Permission Checking Script
# This script checks user permissions for accessing resources

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load configuration
CONFIG_FILE="$PROJECT_DIR/config/permissions.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Default values
USER_EMAIL=""
RESOURCE_TYPE=""
RESOURCE_NAME=""
ACTION=""
VERBOSE=false
JSON_OUTPUT=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--user)
            USER_EMAIL="$2"
            shift 2
            ;;
        -r|--resource)
            RESOURCE_TYPE="$2"
            shift 2
            ;;
        -n|--name)
            RESOURCE_NAME="$2"
            shift 2
            ;;
        -a|--action)
            ACTION="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Check user permissions for accessing resources."
            echo ""
            echo "Options:"
            echo "  -u, --user EMAIL         User email address (required)"
            echo "  -r, --resource TYPE      Resource type: workspace, skill, system (required)"
            echo "  -n, --name NAME          Resource name (required for workspace/skill)"
            echo "  -a, --action ACTION      Action to check: view, install, uninstall, manage (required)"
            echo "  -v, --verbose            Enable verbose output"
            echo "  -j, --json               Output results in JSON format"
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
if [ -z "$USER_EMAIL" ]; then
    echo "Error: User email is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

if [ -z "$RESOURCE_TYPE" ]; then
    echo "Error: Resource type is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

if [ -z "$ACTION" ]; then
    echo "Error: Action is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

# Validate resource type
case "$RESOURCE_TYPE" in
    workspace|skill|system)
        # Valid type
        ;;
    *)
        echo "Error: Invalid resource type '$RESOURCE_TYPE'"
        echo "Valid types are: workspace, skill, system"
        exit 1
        ;;
esac

# Check if user exists
USER_FILE="$PROJECT_DIR/data/users/$USER_EMAIL.json"
if [ ! -f "$USER_FILE" ]; then
    echo "Error: User '$USER_EMAIL' does not exist"
    exit 1
fi

# Load user data
USER_DATA=$(cat "$USER_FILE")

# Check resource existence
RESOURCE_EXISTS=false
case "$RESOURCE_TYPE" in
    workspace)
        if [ -n "$RESOURCE_NAME" ]; then
            WORKSPACE_FILE="$PROJECT_DIR/data/workspaces/$RESOURCE_NAME.json"
            if [ -f "$WORKSPACE_FILE" ]; then
                RESOURCE_EXISTS=true
                RESOURCE_DATA=$(cat "$WORKSPACE_FILE")
            fi
        fi
        ;;
    skill)
        if [ -n "$RESOURCE_NAME" ]; then
            SKILL_FILE="$PROJECT_DIR/data/skills/$RESOURCE_NAME.json"
            if [ -f "$SKILL_FILE" ]; then
                RESOURCE_EXISTS=true
                RESOURCE_DATA=$(cat "$SKILL_FILE")
            fi
        fi
        ;;
    system)
        RESOURCE_EXISTS=true
        RESOURCE_DATA='{"name": "system", "type": "system"}'
        ;;
esac

if [ "$RESOURCE_EXISTS" = false ] && [ "$RESOURCE_TYPE" != "system" ]; then
    echo "Error: Resource '$RESOURCE_NAME' of type '$RESOURCE_TYPE' does not exist"
    exit 1
fi

# Check permissions using Python
cd "$PROJECT_DIR"
PERMISSION_CHECK=$(python3 -c "
import sys
sys.path.append('src')
from models.User import User, UserManager
from models.Workspace import Workspace, WorkspaceManager
from models.Skill import Skill, SkillManager
from services.PermissionService import PermissionService
import json
import uuid

# Initialize managers
user_manager = UserManager()
workspace_manager = WorkspaceManager()
skill_manager = SkillManager()
permission_service = PermissionService()

# Get user
user = user_manager.get_user_by_email('$USER_EMAIL')
if not user:
    print('Error: User not found')
    sys.exit(1)

# Get resource
resource = None
resource_type = '$RESOURCE_TYPE'

if resource_type == 'workspace':
    workspace = workspace_manager.get_workspace_by_name('$RESOURCE_NAME')
    if not workspace:
        print('Error: Workspace not found')
        sys.exit(1)
    resource = workspace
    
elif resource_type == 'skill':
    skill = skill_manager.get_skill_by_name('$RESOURCE_NAME')
    if not skill:
        print('Error: Skill not found')
        sys.exit(1)
    resource = skill
    
elif resource_type == 'system':
    # Create a dummy system resource
    resource = type('SystemResource', (), {
        'name': 'system',
        'type': 'system'
    })()

# Check permissions
result = {
    'user_email': '$USER_EMAIL',
    'resource_type': resource_type,
    'resource_name': '$RESOURCE_NAME' if resource_type != 'system' else 'system',
    'action': '$ACTION',
    'permissions': {}
}

# Check general permissions
if hasattr(permission_service, 'has_permission'):
    has_perm = permission_service.has_permission(user, '$ACTION')
    result['permissions']['general'] = has_perm

# Check resource-specific permissions
if resource_type == 'workspace' and isinstance(resource, Workspace):
    if '$ACTION' == 'view':
        can_access = permission_service.can_access_workspace(user, resource)
        result['permissions']['can_access'] = can_access
    elif '$ACTION' == 'manage':
        can_manage = permission_service.can_manage_workspace(user, resource)
        result['permissions']['can_manage'] = can_manage
    elif '$ACTION' == 'install':
        # Simulate skill installation permission check
        can_install = permission_service.has_permission(user, 'install_workspace_skills')
        result['permissions']['can_install'] = can_install
        
    elif '$ACTION' == 'uninstall':
        # Simulate skill uninstallation permission check
        can_uninstall = permission_service.has_permission(user, 'uninstall_workspace_skills')
        result['permissions']['can_uninstall'] = can_uninstall
        
elif resource_type == 'skill' and isinstance(resource, Skill):
    # Check if skill is accessible
    result['permissions']['accessible'] = True
    
    # Check if user can install skill
    if '$ACTION' == 'install':
        workspace = workspace_manager.get_workspace_by_name('default')  # Default workspace for demo
        if workspace:
            install_result = permission_service.can_install_skill(user, resource, workspace)
            result['permissions']['can_install'] = install_result['can_install']
            result['permissions']['install_reason'] = install_result['reason']
        
    elif '$ACTION' == 'uninstall':
        workspace = workspace_manager.get_workspace_by_name('default')  # Default workspace for demo
        if workspace:
            uninstall_result = permission_service.can_uninstall_skill(user, resource, workspace)
            result['permissions']['can_uninstall'] = uninstall_result['can_uninstall']
            result['permissions']['uninstall_reason'] = uninstall_result['reason']

elif resource_type == 'system':
    # System-level permissions
    if '$ACTION' == 'view':
        can_view = permission_service.has_permission(user, 'view_system')
        result['permissions']['can_view'] = can_view
    elif '$ACTION' == 'manage':
        can_manage = permission_service.has_permission(user, 'manage_system')
        result['permissions']['can_manage'] = can_manage
    elif '$ACTION' == 'config':
        can_config = permission_service.has_permission(user, 'system_config')
        result['permissions']['can_config'] = can_config

# Get user role information
result['user_role'] = user.role.value
result['additional_roles'] = [role.value for role in user.roles]

# Get permission summary
summary = permission_service.get_permission_summary(user)
result['permission_summary'] = summary

print(json.dumps(result, indent=2))
")

# Output results
if [ "$JSON_OUTPUT" = true ]; then
    echo "$PERMISSION_CHECK"
else
    # Parse JSON and display user-friendly output
    echo "Permission Check Results:"
    echo "========================"
    echo "User: $USER_EMAIL"
    echo "Resource Type: $RESOURCE_TYPE"
    echo "Resource Name: ${RESOURCE_NAME:-system}"
    echo "Action: $ACTION"
    echo ""
    
    # Extract and display permission results
    CAN_PERFORM=$(echo "$PERMISSION_CHECK" | python3 -c "
import json, sys
data = json.load(sys.stdin)
permissions = data.get('permissions', {})
for perm, result in permissions.items():
    if isinstance(result, dict):
        if result.get('can_install'):
            print('✓ Can install skill')
        elif result.get('can_uninstall'):
            print('✓ Can uninstall skill')
        elif result.get('can_manage'):
            print('✓ Can manage workspace')
        elif result.get('can_access'):
            print('✓ Can access workspace')
        elif result.get('can_view'):
            print('✓ Can view system')
        elif result.get('can_config'):
            print('✓ Can configure system')
    else:
        if result:
            print(f'✓ {perm}: Allowed')
        else:
            print(f'✗ {perm}: Denied')
")
    
    if [ -n "$CAN_PERFORM" ]; then
        echo "$CAN_PERFORM"
    else
        echo "No specific permissions found for this action."
    fi
    
    echo ""
    echo "User Role: $(echo "$PERMISSION_CHECK" | python3 -c "import json, sys; print(json.load(sys.stdin)['user_role'])")"
    
    echo ""
    echo "Permission Summary:"
    SUMMARY=$(echo "$PERMISSION_CHECK" | python3 -c "
import json, sys
data = json.load(sys.stdin)
summary = data.get('permission_summary', {})
print(f'Total Permissions: {summary.get(\"total_permissions\", 0)}')
print(f'Workspace Permissions: {len(summary.get(\"workspace_permissions\", []))}')
print(f'Skill Permissions: {len(summary.get(\"skill_permissions\", []))}')
")
    echo "$SUMMARY"
    
    echo ""
    echo "Detailed Permission List:"
    DETAILED=$(echo "$PERMISSION_CHECK" | python3 -c "
import json, sys
data = json.load(sys.stdin)
permissions = data.get('permissions', {})
for perm, result in permissions.items():
    if isinstance(result, dict):
        for sub_perm, sub_result in result.items():
            status = '✓' if sub_result else '✗'
            print(f'{status} {perm}.{sub_perm}: {sub_result}')
    else:
        status = '✓' if result else '✗'
        print(f'{status} {perm}: {result}')
")
    echo "$DETAILED"
fi

# Log permission check
AUDIT_LOG=$(cat << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "action": "check_permissions",
  "user": "$USER_EMAIL",
  "resource_type": "$RESOURCE_TYPE",
  "resource_name": "$RESOURCE_NAME",
  "requested_action": "$ACTION",
  "check_result": "completed"
}
EOF
)

# Write audit log
AUDIT_DIR="$PROJECT_DIR/data/audit"
mkdir -p "$AUDIT_DIR"
echo "$AUDIT_LOG" >> "$AUDIT_DIR/permission_check_$(date -u +"%Y%m%d_%H%M%S").json"

echo ""
echo "Permission check completed. Audit log written to: $AUDIT_DIR/permission_check_$(date -u +"%Y%m%d_%H%M%S").json"

exit 0