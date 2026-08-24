# Hermes Mirror Backup — Live Install Notes (2026-08-24)

Concrete state of the validated deployment. Paths are environment-specific —
treat as an example, re-derive equivalents on other machines.

## Layout

| Path | Role |
|---|---|
| `/data/workspace/backup_scripts/` | **source of truth** for the pipeline |
| ├─ `run_backup.sh` | orchestrator (lock → export → docs → dashboard → scrub+push) |
| ├─ `export_sessions.py` | SQLite `state.db` → per-session Markdown transcripts + index |
| ├─ `export_assets.py` | skills/memories copytree + redacted config + health snapshot; runs repo-wide scrub at end |
| ├─ `write_docs.py` | regenerates README.md + docs/SYSTEM.md from live DB counts |
| ├─ `build_dashboard.py` | builds self-contained dark HTML dashboard (`brain.html`) |
| └─ `scrub.py` | secret-scrub module (`scrub()` text / `scrub_tree()` dir); patterns incl. partially-masked tokens |
| `/data/workspace/backup_repo/` | local git mirror (5 top-level dirs + brain.html) |
| `/data/workspace/backup.log` | append-only run log |
| `~/.hermes/scripts/hermes_brain_backup.sh` | cron entrypoint — THIN WRAPPER: `exec bash /data/workspace/backup_scripts/run_backup.sh` |

## Cron job

- id `dd6bd38d99d4`, name "Hermes Brain Backup — 12h mirror sync"
- schedule every 720m, `no_agent=True`, deliver origin
- edit pipeline logic ONLY in `backup_scripts/run_backup.sh`, never the wrapper

## Remote

- repo `github.com/tyu008313/hermesbackup2` (public), branch `main`
- GitHub Pages enabled: source main/root → dashboard at
  `https://tyu008313.github.io/hermesbackup2/brain.html`
- push auth: PAT embedded in remote URL inside run_backup.sh; also injected to
  scrubber via `HERMES_SCRUB_LITERALS`

## Token rotation procedure (when the PAT is replaced)

1. Edit the `TOKEN=` line in `run_backup.sh`.
2. Update the same literal in `export HERMES_SCRUB_LITERALS="..."` (it scrubs the
   OLD token out of transcripts; add the new one too so a future leak of the new
   token is also caught).
3. Run once by hand: `bash /data/workspace/backup_scripts/run_backup.sh`
4. Confirm log shows `PUSH OK`; then check Pages still serves.

## Extending the pipeline

- New data class (e.g. kanban.db): write exporter #5 producing deterministic
  files under a numbered top-level dir, call it from run_backup.sh between
  stages 2 and 3, keep metadata sidecars for skip-if-unchanged.
- Keep every stage fail-open: a failed exporter logs `!! ... FAILED` and the run
  continues so one broken stage never blocks the mirror.
- Dashboard is regenerated wholesale each run — cheap (<20KB) and always fresh.

## Known-good verification snapshot (2026-08-24)

- first push `39ba36b` (557 files), second `5f430e6` (9 files)
- remote HEAD matched local after each push
- leak audit: 0 hits (word-boundary scan + literal grep)
- Pages probe: HTTP 200 on brain.html
