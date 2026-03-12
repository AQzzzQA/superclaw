#!/bin/bash

# Skill Management System - Workspace Creation Script
# This script creates a new workspace with specified configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load configuration
CONFIG_FILE="$PROJECT_DIR/config/workspaces.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Load environment variables
source "$PROJECT_DIR/.env" 2>/dev/null || true

# Default values
WORKSPACE_NAME=""
WORKSPACE_DESCRIPTION=""
WORKSPACE_TYPE="team"
OWNER_EMAIL=""
ADMIN_EMAILS=()
FORCE=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            WORKSPACE_NAME="$2"
            shift 2
            ;;
        -d|--description)
            WORKSPACE_DESCRIPTION="$2"
            shift 2
            ;;
        -t|--type)
            WORKSPACE_TYPE="$2"
            shift 2
            ;;
        -o|--owner)
            OWNER_EMAIL="$2"
            shift 2
            ;;
        -a|--admin)
            ADMIN_EMAILS+=("$2")
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
            echo "Create a new workspace in the skill management system."
            echo ""
            echo "Options:"
            echo "  -n, --name NAME           Workspace name (required)"
            echo "  -d, --description DESC    Workspace description"
            echo "  -t, --type TYPE           Workspace type (team, department, organization, individual)"
            echo "  -o, --owner EMAIL         Owner email address (required)"
            echo "  -a, --admin EMAIL         Additional admin email addresses"
            echo "  -f, --force               Force creation even if workspace exists"
            echo "  -v, --verbose             Enable verbose output"
            echo "  -h, --help                Show this help message"
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

if [ -z "$OWNER_EMAIL" ]; then
    echo "Error: Owner email is required"
    echo "Use -h or --help for usage information."
    exit 1
fi

# Check if workspace already exists
if [ -f "$PROJECT_DIR/data/workspaces/$WORKSPACE_NAME.json" ] && [ "$FORCE" != true ]; then
    echo "Error: Workspace '$WORKSPACE_NAME' already exists"
    echo "Use -f or --force to overwrite existing workspace."
    exit 1
fi

# Validate workspace type
case "$WORKSPACE_TYPE" in
    team|department|organization|individual|development|production|testing|collaboration)
        # Valid type
        ;;
    *)
        echo "Error: Invalid workspace type '$WORKSPACE_TYPE'"
        echo "Valid types are: team, department, organization, individual, development, production, testing, collaboration"
        exit 1
        ;;
esac

# Generate workspace ID
WORKSPACE_ID=$(uuidgen)

# Create workspace directory
WORKSPACE_DIR="$PROJECT_DIR/data/workspaces"
mkdir -p "$WORKSPACE_DIR"

# Create user directories if they don't exist
USERS_DIR="$PROJECT_DIR/data/users"
mkdir -p "$USERS_DIR"

# Create workspace data
WORKSPACE_DATA=$(cat << EOF
{
  "workspace_id": "$WORKSPACE_ID",
  "name": "$WORKSPACE_NAME",
  "description": "$WORKSPACE_DESCRIPTION",
  "status": "active",
  "workspace_type": "$WORKSPACE_TYPE",
  "owner_id": "$OWNER_EMAIL",
  "admins": ["$OWNER_EMAIL"],
  "members": ["$OWNER_EMAIL"],
  "skills": [],
  "skill_versions": {},
  "config": {
    "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "created_by": "$0",
    "auto_create_user_directories": true,
    "enable_email_notifications": true,
    "enable_audit_logging": true,
    "require_approval_for_skills": false
  },
  "constraints": {},
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "last_activity": null,
  "audit_log": [],
  "tags": [],
  "metadata": {
    "creation_script": "$0",
    "creation_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  }
}
EOF
)

# Write workspace data to file
echo "$WORKSPACE_DATA" > "$WORKSPACE_DIR/$WORKSPACE_NAME.json"

# Add additional admins if specified
for admin_email in "${ADMIN_EMAILS[@]}"; do
    if [ "$admin_email" != "$OWNER_EMAIL" ]; then
        # Add admin to workspace
        python3 -c "
import sys
sys.path.append('$PROJECT_DIR/src')
from models.Workspace import Workspace, WorkspaceManager

manager = WorkspaceManager()
workspace = manager.get_workspace_by_name('$WORKSPACE_NAME')
if workspace:
    workspace.add_admin('$admin_email')
    manager.update_workspace(workspace.workspace_id, admins=workspace.admins)
    print('Added admin: $admin_email')
else:
    print('Error: Workspace not found')
    sys.exit(1)
"
    fi
done

# Create audit log entry
AUDIT_LOG=$(cat << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "action": "create_workspace",
  "user": "$OWNER_EMAIL",
  "details": {
    "workspace_id": "$WORKSPACE_ID",
    "workspace_name": "$WORKSPACE_NAME",
    "workspace_type": "$WORKSPACE_TYPE",
    "owner_email": "$OWNER_EMAIL",
    "admin_emails": [${ADMIN_EMAILS[@]}],
    "description": "$WORKSPACE_DESCRIPTION"
  }
}
EOF
)

# Write audit log
AUDIT_DIR="$PROJECT_DIR/data/audit"
mkdir -p "$AUDIT_DIR"
echo "$AUDIT_LOG" >> "$AUDIT_DIR/workspace_creation_$(date -u +"%Y%m%d_%H%M%S").json"

# Send notification emails (if configured)
if [ -n "$SMTP_HOST" ] && [ -n "$SMTP_PORT" ] && [ -n "$SMTP_USER" ] && [ -n "$SMTP_PASSWORD" ]; then
    # Send notification to owner
    python3 -c "
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

workspace_data = '''$WORKSPACE_DATA'''

# Parse workspace data
workspace_info = json.loads(workspace_data)

# Create email
msg = MIMEMultipart()
msg['From'] = 'noreply@skill-management-system.com'
msg['To'] = '$OWNER_EMAIL'
msg['Subject'] = f'Workspace Created: {workspace_info[\"name\"]}'

# Email body
body = f'''
Hello,

Your workspace '{workspace_info['name']}' has been successfully created!

Workspace Details:
- Name: {workspace_info['name']}
- ID: {workspace_info['workspace_id']}
- Type: {workspace_info['workspace_type']}
- Description: {workspace_info['description']}
- Created: {workspace_info['created_at']}

You have been added as the owner of this workspace with full administrative privileges.

Best regards,
Skill Management System
'''

msg.attach(MIMEText(body, 'plain'))

# Send email
server = smtplib.SMTP('$SMTP_HOST', $SMTP_PORT)
server.starttls()
server.login('$SMTP_USER', '$SMTP_PASSWORD')
server.send_message(msg)
server.quit()
"
    
    # Send notifications to additional admins
    for admin_email in "${ADMIN_EMAILS[@]}"; do
        if [ "$admin_email" != "$OWNER_EMAIL" ]; then
            python3 -c "
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

workspace_data = '''$WORKSPACE_DATA'''

# Parse workspace data
workspace_info = json.loads(workspace_data)

# Create email
msg = MIMEMultipart()
msg['From'] = 'noreply@skill-management-system.com'
msg['To'] = '$admin_email'
msg['Subject'] = f'Added as Admin to Workspace: {workspace_info[\"name\"]}'

# Email body
body = f'''
Hello,

You have been added as an administrator to workspace '{workspace_info['name']}'.

Workspace Details:
- Name: {workspace_info['name']}
- ID: {workspace_info['workspace_id']}
- Type: {workspace_info['workspace_type']}
- Description: {workspace_info['description']}
- Owner: {workspace_info['owner_id']}

You now have administrative privileges for this workspace.

Best regards,
Skill Management System
'''

msg.attach(MIMEText(body, 'plain'))

# Send email
server = smtplib.SMTP('$SMTP_HOST', $SMTP_PORT)
server.starttls()
server.login('$SMTP_USER', '$SMTP_PASSWORD')
server.send_message(msg)
server.quit()
"
        fi
    done
fi

# Display success message
echo "✓ Workspace '$WORKSPACE_NAME' created successfully!"
echo ""
echo "Workspace Details:"
echo "  Name: $WORKSPACE_NAME"
echo "  ID: $WORKSPACE_ID"
echo "  Type: $WORKSPACE_TYPE"
echo "  Owner: $OWNER_EMAIL"
echo "  Admins: $OWNER_EMAIL ${ADMIN_EMAILS[@]}"
echo "  Description: $WORKSPACE_DESCRIPTION"
echo ""
echo "Workspace data saved to: $WORKSPACE_DIR/$WORKSPACE_NAME.json"
echo "Audit log created: $AUDIT_DIR/workspace_creation_$(date -u +"%Y%m%d_%H%M%S").json"
echo ""

# Show next steps
echo "Next steps:"
echo "1. Add users to the workspace using: ./scripts/manage_users.sh add user workspace role"
echo "2. Install skills using: ./scripts/install_skill.sh workspace skill_name"
echo "3. View workspace status using: ./scripts/workspace_status.sh workspace_name"
echo ""

exit 0