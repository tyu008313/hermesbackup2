# Proven Patterns — Agent State Backup

Condensed, validated code from the Aug 2026 build. Copy-modify; do not
reinvent. Full working copies live on the server at
`/data/workspace/backup_scripts/` (export_sessions.py, export_assets.py,
build_dashboard.py, write_docs.py, run_backup.sh).

## 1. Session Exporter Core (state.db → Markdown)

```python
import sqlite3
from datetime import datetime, timezone

DB = "/data/.hermes/state.db"
con = sqlite3.connect(f"file:{DB}?mode=ro&immutable=1", uri=True)
con.row_factory = sqlite3.Row
sessions = con.execute("SELECT * FROM sessions ORDER BY started_at ASC").fetchall()
msgs = con.execute("SELECT * FROM messages WHERE session_id=? AND active=1 "
                   "ORDER BY id ASC", (sid,)).fetchall()
# timestamps are unix floats:
datetime.fromtimestamp(float(sess["started_at"]), tz=timezone.utc)
```

- `content` column may be a JSON array of blocks: iterate `type=='text'`,
  `tool_use` (render name+input), `tool_result`. Fall back to raw text.
- Per-message `<details><summary>ROLE — timestamp</summary>` keeps transcripts
  readable in GitHub UI.
- Idempotency marker: write `_message_count` + `_ended` into each session's
  `02_METADATA.json`; skip session if both unchanged.

## 2. Token Budget per Session

```python
in_t  = sess["input_tokens"] or 0) + (sess["cache_read_tokens"] or 0)
out_t = sess["output_tokens"] or 0
cost  = sess["estimated_cost_usd"]
```

## 3. Config Redaction (line-wise YAML)

```python
SECRET_KEYS = re.compile(r"(token|secret|password|api_key|apikey|key|authorization)", re.I)
def redact(line):
    k, _, v = line.partition(":")
    if SECRET_KEYS.search(k) and v.strip() not in ("", "null", "~", "{}"):
        return f"{k}: [REDACTED]\n"
    return line
```

.env backup exports KEY NAMES only (`KEY=<redacted>`), never values.

## 4. Health Snapshot

Uptime/mem/disk via `os.popen("free -h --si ...")`; gateway liveness via PID
file + `/proc/<pid>` check; cron job count from `cron/executions.db`
(read-only). Write BOTH `LATEST.md` and a timestamped copy for git history.

## 5. Dashboard (self-contained HTML)

Pure-python string templating; load all `02_METADATA.json` files, aggregate
totals (sessions/messages/tokens/cost), render stat cards + clickable session
cards linking to GitHub blob URLs. RTL Persian layout, dark theme, no JS deps.
Regenerate every run so it can never go stale.

## 6. Orchestrator Skeleton

```bash
#!/usr/bin/env bash
set -uo pipefail
export HOME=/data GIT_TERMINAL_PROMPT=0
LOCK=/tmp/hermes_backup.lock
[ -f "$LOCK" ] && kill -0 "$(cat $LOCK)" 2>/dev/null && exit 0   # single instance
echo $$ > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
python3 export_sessions.py  || echo "session exporter failed"
python3 export_assets.py    || echo "asset exporter failed"      # runs final scrub
python3 write_docs.py       || echo "docs writer failed"
python3 build_dashboard.py  || echo "dashboard failed"
cd /data/workspace/backup_repo
git fetch origin main && git reset --soft FETCH_HEAD        # adopt remote history
git add -A
[ -z "$(git diff --cached --numstat)" ] && exit 0            # nothing new → silent
git commit -q -m "backup: auto-sync $(date -u '+%F %H:%M UTC') [no-llm]"
git push origin main || { sleep 3; git pull --rebase origin main; git push origin main; }
```
Exit non-zero ONLY on push failure (so cron retries matter). Quiet on success
(`no_agent=True` cron delivers stdout verbatim; empty = silent).

## 7. Enable GitHub Pages

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/pages \
  -d '{"source":{"branch":"main","path":"/"}}'
# Dashboard then at https://OWNER.github.io/REPO/brain.html
```

## 8. Cron Job Payload (zero tokens)

```
cronjob(action=create, name="hermes-brain-backup",
        schedule="12h",
        script="/data/workspace/backup_scripts/run_backup.sh",
        no_agent=True, deliver="local")
```
Keep pipeline < ~3 min (hard interrupt). Current runtime: seconds.

## 9. Repo Layout Contract (user-mandated, keep in sync)

```
README.md (regenerated w/ live counts)   brain.html (dashboard)
BRAIN.md + BRAIN.html (agent brain/prompt-engineering doc)
01_CORE_ASSETS/skills|memories     02_OPERATIONS/sessions/<date>/<time_title_id>/
03_INFRASTRUCTURE/config|scripts   04_PROJECTS_LAB/   05_SYSTEM_INTELLIGENCE/health|metadata
```
All sections update together EVERY run — user explicitly rejected partial sync.
