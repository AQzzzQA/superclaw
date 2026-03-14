#!/bin/bash
# Backup configuration files
# Runs daily at 00:00

BACKUP_DIR="/root/.openclaw/workspace/backups/config"
DATE=$(date +%Y%m%d_%H%M%S)
TIMESTAMP=$(date +%s)

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Files to backup
FILES=(
    ".env"
    "MEMORY.md"
    "IDENTITY.md"
    "SOUL.md"
    "TOOLS.md"
    "USER.md"
    "AGENTS.md"
    "HEARTBEAT.md"
    "memory/heartbeat-state.json"
)

# Backup files
echo "Starting configuration backup at $(date)"
echo "----------------------------------------"

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/$(basename $file).$DATE.bak"
        echo "✅ Backed up: $file"
    else
        echo "⚠️  Skipped (not found): $file"
    fi
done

# Create backup manifest
cat > "$BACKUP_DIR/manifest.$DATE.txt" << MANIFEST
Backup Date: $(date)
Timestamp: $TIMESTAMP
Files Backed Up:
MANIFEST

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "- $file" >> "$BACKUP_DIR/manifest.$DATE.txt"
    fi
done

echo "----------------------------------------"
echo "Backup completed at $(date)"
echo "Backup location: $BACKUP_DIR"

# Clean up old backups (keep last 7 days)
find "$BACKUP_DIR" -name "*.bak" -mtime +7 -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "manifest.*.txt" -mtime +7 -delete 2>/dev/null || true

echo "Old backups cleaned up (kept last 7 days)"
