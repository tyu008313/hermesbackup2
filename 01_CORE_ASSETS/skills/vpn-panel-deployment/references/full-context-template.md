# Full Context File Template for Next Session

When the user asks for a "context file" or "prompt for next session", create a file that includes:

## Required Sections

1. **Quick Reference Table** - Bot token, admin ID, server IP, install path, DB credentials
2. **Cloudflare Tunnel** - How to start, find URL, update webhook, update cron
3. **Services Management** - Apache, MariaDB, Cron start/stop/restart
4. **Database Commands** - Connect, backup, restore, check admin/users
5. **Critical Fixes Applied** - Full code for checktelegramip(), admin table, user status
6. **Cron Jobs** - List of all jobs with domain placeholder
7. **Installed Software** - Versions of all components
8. **File Paths** - All important file locations
9. **Troubleshooting** - Common issues and solutions
10. **User Info** - Name, Telegram, preferences

## GitHub Backup

Save the context file to the backup repo:
```bash
cp CONTEXT_FILE.md /data/workspace/backup_repo/
cd /data/workspace/backup_repo
git add CONTEXT_FILE.md
git commit -m "Add full session context"
git push origin main
```

## Memory Entry

Also add a memory entry summarizing the key facts for quick reference.
