#!/bin/bash

# Configuration
BACKUP_DIR="/data/workspace/hermesbackup2"
HERMES_DIR="$HOME/.hermes"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create Professional Folder Structure
mkdir -p "$BACKUP_DIR/01_🧠_Knowledge/skills"
mkdir -p "$BACKUP_DIR/01_🧠_Knowledge/memories"
mkdir -p "$BACKUP_DIR/02_💬_Conversations"
mkdir -p "$BACKUP_DIR/03_🛠️_Tools_&_Config/scripts"
mkdir -p "$BACKUP_DIR/04_🏗_Workspace"
mkdir -p "$BACKUP_DIR/05_📊_System_Stats"

# 1. Sync Knowledge (Skills & Memories)
cp -r "$HERMES_DIR/skills/"* "$BACKUP_DIR/01_🧠_Knowledge/skills/" 2>/dev/null
cp -r "$HERMES_DIR/memories/"* "$BACKUP_DIR/01_🧠_Knowledge/memories/" 2>/dev/null

# 2. Sync Conversations (Sessions)
cp -r "$HERMES_DIR/sessions/"* "$BACKUP_DIR/02_💬_Conversations/" 2>/dev/null

# 3. Sync Tools & Configs
cp -r "$HERMES_DIR/scripts/"* "$BACKUP_DIR/03_🛠️_Tools_&_Config/scripts/" 2>/dev/null
cp "$HERMES_DIR/config.yaml" "$BACKUP_DIR/03_🛠️_Tools_&_Config/" 2>/dev/null

# 4. Sync Workspace Projects
# We copy everything from workspace but exclude the backup folder itself
rsync -av --exclude='hermesbackup2' /data/workspace/ "$BACKUP_DIR/04_🏗_Workspace/"

# 5. Capture System Info
echo "Backup generated on: $TIMESTAMP" > "$BACKUP_DIR/05_📊_System_Stats/info.txt"
echo "Hermes Profile: $HERMES_PROFILE" >> "$BACKUP_DIR/05_📊_System_Stats/info.txt"

# Git Operations
cd "$BACKUP_DIR"
git add .
git commit -m "🚀 Professional Backup: $TIMESTAMP"
git push origin main
