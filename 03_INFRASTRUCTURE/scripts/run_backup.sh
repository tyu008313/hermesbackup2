#!/usr/bin/env bash
# ============================================================
#  HERMES BRAIN BACKUP — Master Orchestrator
#  Full backup -> categorize -> dashboard -> git push (HTTPS)
#  Runs WITHOUT any LLM. Zero tokens. Exit code = health.
# ============================================================
set -uo pipefail

export HOME=/data
export GIT_TERMINAL_PROMPT=0
TOKEN="gh****REDACTED****"
REMOTE="https://x-access-token:${TOKEN}@github.com/tyu008313/hermesbackup2.git"
REPO_DIR="/data/workspace/backup_repo"
SCRIPTS="/data/workspace/backup_scripts"
LOCK="/tmp/hermes_backup.lock"
LOG="/data/workspace/backup.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

# Inject literal tokens to scrub (defense in depth)
export HERMES_SCRUB_LITERALS="gh****REDACTED****"

# ---------- single-instance lock ----------
if [ -f "$LOCK" ] && kill -0 "$(cat $LOCK)" 2>/dev/null; then
    log "SKIP: another backup is running"; exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

log "========== BACKUP RUN START =========="

mkdir -p "$REPO_DIR"

# ---------- 1) export sessions ----------
log "[1/5] exporting sessions from state.db ..."
if python3 "$SCRIPTS/export_sessions.py" >> "$LOG" 2>&1; then
    log "      sessions OK"
else
    log "      !! session exporter FAILED (continuing)"
fi

# ---------- 2) export core assets ----------
log "[2/5] exporting skills/memories/config/health ..."
if python3 "$SCRIPTS/export_assets.py" >> "$LOG" 2>&1; then
    log "      assets OK"
else
    log "      !! asset exporter FAILED (continuing)"
fi

# ---------- 3) static docs ----------
log "[3/5] writing README / docs ..."
python3 "$SCRIPTS/write_docs.py" >> "$LOG" 2>&1 \
    && log "      docs OK" || log "      !! docs writer failed"

# ---------- 4) dashboard ----------
log "[4/5] building brain.html dashboard ..."
python3 "$SCRIPTS/build_dashboard.py" >> "$LOG" 2>&1 \
    && log "      dashboard OK" || log "      !! dashboard FAILED"

# ---------- 5) commit + push ----------
cd "$REPO_DIR" || exit 1
git remote remove origin 2>/dev/null
git remote add origin "$REMOTE"
# adopt remote history AND stage true mirror-state:
# files removed locally get deleted remotely too (full sync, both directions)
git fetch origin main --quiet 2>>"$LOG" \
    && git reset --mixed FETCH_HEAD 2>>"$LOG"   # index=remote HEAD, worktree ours

git add -A
STAGED=$(git diff --cached --numstat | wc -l)
if [ "$STAGED" -eq 0 ]; then
    log "NOTHING NEW — repo already in sync. done."
    exit 0
fi

git commit -q -m "backup: auto-sync $(date -u '+%Y-%m-%d %H:%M UTC') — sessions/assets/dashboard [no-llm]" \
    || { log "nothing to commit after all"; exit 0; }
log "[5/5] pushing $STAGED changed files ..."
if git push origin main --quiet 2>>"$LOG"; then
    SHA=$(git rev-parse --short HEAD)
    log "PUSH OK → $SHA ($STAGED files)"
else
    # one retry with rebase for race conditions
    sleep 3
    git pull --rebase origin main >> "$LOG" 2>&1
    if git push origin main --quiet 2>>"$LOG"; then
        SHA=$(git rev-parse --short HEAD)
        log "PUSH OK (retry) → $SHA"
    else
        log "!! PUSH FAILED — will retry on next run"
        exit 1
    fi
fi
log "========== BACKUP RUN END =========="
