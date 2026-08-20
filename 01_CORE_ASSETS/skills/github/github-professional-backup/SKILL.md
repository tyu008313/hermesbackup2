---
name: github-professional-backup
description: "Structure and professionalize your GitHub backup repository."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# GitHub Professional Backup

Use this skill to transform a basic backup repository into a highly structured, emoji-enhanced, and professional vault. This workflow ensures that sessions, skills, memories, and workspace projects are organized logically.

## Structure

The recommended repository structure uses numerical prefixes and emojis for maximum clarity and aesthetics:

- `01_🧠_Knowledge/`: skills/ and memories/
- `02_💬_Conversations/`: sessions/ (transcripts)
- `03_🛠️_Tools_&_Config/`: scripts/ and config.yaml
- `04_🏗_Workspace/`: Active projects and documents
- `05_📊_System_Stats/`: System info and backup metadata

## Implementation Steps

1. **Initialize/Reorganize**: Move existing files into the structure above using a script or `execute_code`.
2. **Professional Script**: Update `~/.hermes/scripts/backup_script.sh` to use `mkdir -p` and `rsync` or `cp` into the new directories.
3. **Aesthetic README**: Create a `README.md` with a status table and clear instructions.

## Pitfalls

- **Embedded Repos**: Be careful when copying folders that contain their own `.git` directory. Use `rm -rf .git` in the backup destination or use `git submodule`.
- **Large Files**: Avoid backing up huge binary caches like `image_cache/` or `audio_cache/`.
- **User Consent**: NEVER install backup dependencies without explicit permission.
