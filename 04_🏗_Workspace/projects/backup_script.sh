#!/bin/bash

# Configuration
BACKUP_DIR="/data/workspace/hermesbackup2"
HERMES_SESSIONS_DIR="$HOME/.hermes/sessions"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Ensure the backup directory exists
mkdir -p "$BACKUP_DIR/sessions"
mkdir -p "$BACKUP_DIR/workspace_data"

# Copy all session files
# These are the .jsonl transcripts that contain all our work
cp -r "$HERMES_SESSIONS_DIR"/* "$BACKUP_DIR/sessions/" 2>/dev/null

# Copy current workspace files (excluding the backup repo itself)
cp -r /data/workspace/* "$BACKUP_DIR/workspace_data/" 2>/dev/null
rm -rf "$BACKUP_DIR/workspace_data/hermesbackup2"

# Move to the backup repo
cd "$BACKUP_DIR"

# Organize and clean up (optional: you can add more logic here)
# For example, create a summary file or categorize by date

# Stage everything
git add .

# Commit with a timestamp
git commit -m "Backup: $TIMESTAMP"

# Push to GitHub (using HTTPS since port 22 is closed)
git push origin main
