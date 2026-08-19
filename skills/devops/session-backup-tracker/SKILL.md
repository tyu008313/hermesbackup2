---
name: session-backup-tracker
description: Manages session backup state, clearing after success.
---

# session-backup-tracker

Use this skill to manage the "pending backup" state for sessions in persistent memory.

## Workflow

1. **New Session Detection**:
   - At the start of a new session, check if the `session_id` is already tracked in memory.
   - If not, add an entry: `Session [ID] pending backup`.

2. **Pre-Backup**:
   - Before running `hermes_github_backup.sh`, list all pending sessions from memory to ensure the user knows what's being saved.

3. **Post-Backup Cleanup**:
   - After a successful backup (manual `BACKUP` command or confirming a cron run), use `memory(action='remove')` to clear the "pending backup" entries for the sessions that were just confirmed as uploaded.

## Verification
- Check GitHub repository `tyu008313/hermesbackup2` to ensure the session files actually landed before clearing memory.
