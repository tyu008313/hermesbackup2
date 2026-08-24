#!/usr/bin/env bash
# HERMES BRAIN BACKUP — History Reporter (for BACKUP LIST)
# Prints recent backup commits + last update. No LLM needed.
REPO="/data/workspace/backup_repo"

if [ ! -d "$REPO/.git" ]; then
    echo "ERROR: local repo missing at $REPO"; exit 1
fi

echo "=== LAST UPDATE ==="
git -C "$REPO" log -1 --date=format-local:'%Y-%m-%d %H:%M UTC' \
    --pretty=format:'%ad — %h'

echo ""
echo ""
echo "=== RECENT BACKUPS (newest first) ==="
git -C "$REPO" log -15 --date=format-local:'%Y-%m-%d %H:%M UTC' \
    --pretty=format:'%ad | %h | %s'

echo ""
echo ""
echo "=== WORKING TREE ==="
if [ -n "$(git -C "$REPO" status --porcelain)" ]; then
    echo "DIRTY — uncommitted changes pending (next run will pick them up)"
else
    echo "CLEAN — everything committed"
fi
