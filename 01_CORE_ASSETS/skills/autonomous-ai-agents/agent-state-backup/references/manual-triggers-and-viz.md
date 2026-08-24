# Manual Triggers & Self-Documenting Repo

Session-proven additions (Aug 2026) to the backup pipeline class.

## 1. Manual keyword triggers alongside the cron

The 12h no_agent cron covers unattended sync; users also want on-demand
control from chat. Implement as a tiny skill whose body invokes two scripts:

- **Run command** (`BACKUP` / «بکاپ کن»): executes the orchestrator
  immediately — same script the cron uses, so lock/idempotency/scrub all
  apply. Report the log tail: `[5/5] pushing N files`, `PUSH OK → <sha>`,
  or `NOTHING NEW — repo already in sync`.
- **History command** (`BACKUP LIST`): NO push. Read-only report:

```bash
git -C "$REPO" log -1 --date=format-local:'%Y-%m-%d %H:%M UTC' --pretty=format:'%ad — %h'
git -C "$REPO" log -15 --pretty=format:'%ad | %h | %s'
git -C "$REPO" status --porcelain   # DIRTY = pending changes, CLEAN otherwise
```

Format the raw output as a table for chat. Live example skill:
`software-development/backup-trigger`; scripts:
`/data/workspace/backup_scripts/{run_backup.sh,list_backups.sh}`.

## 2. Self-documenting repo (pipeline copies itself into the mirror)

In the asset exporter, copy `backup_scripts/*.{py,sh}` into the mirror's
infrastructure folder AFTER scrubbing each copy (`scrub_file(dst)`). Result:
the repo documents its own architecture. CRITICAL: those repo copies are
credential-redacted by design (`TOKEN="gh****REDACTED****"` in the embedded
orchestrator) — never execute them; only live originals outside the repo run.
State this explicitly in the mirror's docs so nobody runs the sanitized copy.

## 3. Interactive brain visualizations (dashboard upgrade path)

When asked to visualize "the real brain" with rotation/bilingual labels,
a dependency-free Canvas sphere beats Three.js for GitHub Pages (no build,
no CDN risk). Proven artifact: `BRAIN3D.html` at the repo root.

- Golden-angle spiral places N nodes evenly on a sphere:
  `phi = acos(1-2*(i+.5)/N); theta = π*(1+√5)*(i+.5)`
- Rotate Y then X per frame; depth `(z+1)/2` drives node radius/glow/alpha;
  sort back→front before drawing; edges drawn behind nodes with depth-based alpha.
- Pointer capture drag = free 360° spin; click picking = nearest projected
  node within threshold → bilingual card (FA + EN paragraphs).
- Respect `prefers-reduced-motion: reduce` by starting paused; provide
  auto-rotate / pause / reset controls; FPS counter via rolling average.
- Bilingual convention the user expects: Persian in green accents (RTL),
  English in blue (LTR), side-by-side or paired rows — never mixed in one line.
