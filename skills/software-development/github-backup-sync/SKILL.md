---
name: github-backup-sync
description: "GitHub-direct structured backups on a cron schedule."
version: 1.0.0
---

# GitHub Backup Sync

Push structured backups straight to GitHub on a cron schedule, with no local backup persistence.

## Procedure

1. Stage into a fresh temp dir with fixed folders: `core/`, `intelligence/`, `skills/`, `interactions/`, `enterprise/`.
2. Write `README.md` (structure + schedule) and `.gitignore` (secrets, locks, db/socket/pid files) into the staging dir.
3. Delete any token or credential file from staging before `git add` — never commit secrets.
4. Commit and push from staging only: `git init -b main`, commit, `git remote add origin` with an `oauth2:TOKEN@github.com` URL, `git push -f origin main`.
5. Remove the staging dir after a successful push; keep no backup copies locally.
6. Wire automation as a `no_agent` cron job whose `script` is a bare filename living under the scripts dir, with the repo URL baked into the wrapper — never pass CLI args via the `script` field.
7. Report run times in Asia/Tehran time alongside UTC.

## Pitfalls

- Pass only a bare script filename to a `no_agent` cron job — the scheduler resolves it under the scripts dir and treats extra tokens as part of the filename, so bake arguments into the wrapper script itself.
- Initialize new staging repos with `git init -b main` — the default `master` branch never matches a `main` push refspec and the push fails.
- Strip credential files from staging before committing — push protection rejects any push containing a personal access token, failing the whole run.
- Read the token from a local env file at runtime and keep that file out of both staging and git — the job needs the secret to push while the repo must never contain it.
