#!/bin/bash

# SOP Configuration
BACKUP_DIR="/data/workspace/hermesbackup2"
HERMES_DIR="$HOME/.hermes"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create SOP-compliant Folder Structure
mkdir -p "$BACKUP_DIR/01_CORE_ASSETS/skills" "$BACKUP_DIR/01_CORE_ASSETS/memories"
mkdir -p "$BACKUP_DIR/02_OPERATIONS/sessions" "$BACKUP_DIR/02_OPERATIONS/tasks"
mkdir -p "$BACKUP_DIR/03_INFRASTRUCTURE/config" "$BACKUP_DIR/03_INFRASTRUCTURE/scripts"
mkdir -p "$BACKUP_DIR/04_PROJECTS_LAB/active" "$BACKUP_DIR/04_PROJECTS_LAB/archive"
mkdir -p "$BACKUP_DIR/05_SYSTEM_INTELLIGENCE/metadata" "$BACKUP_DIR/05_SYSTEM_INTELLIGENCE/docs"

# 1. Sync Knowledge (Skills & Memories)
cp -r "$HERMES_DIR/skills/"* "$BACKUP_DIR/01_CORE_ASSETS/skills/" 2>/dev/null
cp -r "$HERMES_DIR/memories/"* "$BACKUP_DIR/01_CORE_ASSETS/memories/" 2>/dev/null

# 2. Sync Conversations (Sessions)
cp -r "$HERMES_DIR/sessions/"* "$BACKUP_DIR/02_OPERATIONS/sessions/" 2>/dev/null

# 3. Sync Tools & Configs
cp -r "$HERMES_DIR/scripts/"* "$BACKUP_DIR/03_INFRASTRUCTURE/scripts/" 2>/dev/null
cp "$HERMES_DIR/config.yaml" "$BACKUP_DIR/03_INFRASTRUCTURE/config/" 2>/dev/null

# 4. Sync Workspace Projects
# We copy everything from workspace but exclude the backup folder itself
rsync -av --exclude='hermesbackup2' /data/workspace/ "$BACKUP_DIR/04_PROJECTS_LAB/active/"

# 5. Capture System Info
echo "Backup generated on: $TIMESTAMP" > "$BACKUP_DIR/05_SYSTEM_INTELLIGENCE/metadata/info.txt"
echo "Hermes Profile: $HERMES_PROFILE" >> "$BACKUP_DIR/05_SYSTEM_INTELLIGENCE/metadata/info.txt"

# Git Operations
cd "$BACKUP_DIR"
git add .
git commit -m "🚀 SOP Backup: $TIMESTAMP"
git push origin main
