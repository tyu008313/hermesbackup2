# Addendum — 2026-08-24 later turns (manual triggers, self-doc repo, brain viz)

Extends `session-log-2026-08-24.md` with what happened after the initial
validation run. Class-level takeaways are distilled in the
`agent-state-backup` skill (`references/manual-triggers-and-viz.md`); this
file records the deployment-specific facts.

## New artifacts added to the running instance

- `list_backups.sh` — read-only history reporter for the `BACKUP LIST`
  command: last commit (date + sha), last 15 commits, working-tree
  CLEAN/DIRTY status. No push, no lock needed.
- Asset exporter gained `export_own_scripts()`: copies the pipeline's own
  `.py/.sh` files into `03_INFRASTRUCTURE/scripts/`, each through
  `scrub_file()`. Verified: embedded orchestrator token reads
  `gh****REDACTED****` in the committed copy; full-length scan = 0 hits.
  The repo copy is therefore NON-RUNNABLE by design — live originals at
  `/data/workspace/backup_scripts/` remain the single source of truth.
- Skill `backup-trigger` (software-development) wires chat keywords:
  `BACKUP` → run orchestrator immediately; `BACKUP LIST` → run
  list_backups.sh and format as a table. Cron job `dd6bd38d99d4` unchanged;
  both paths converge on the same orchestrator so lock + scrub always apply.

## Push ledger after first validation

| Time (UTC) | SHA | Files | Trigger |
|---|---|---|---|
| 08-24 12:22 | 39ba36b | 557 | first full push |
| 08-24 12:28 | 5f430e6 | 9 | idempotency test |
| 08-24 13:13 | 62a3728 | 31 | skill creation + memory deltas |
| 08-24 13:14 | 3fd111c | 31 | own-scripts export fix (`scrub_file` import) |
| 08-24 16:28 | eaba411 | 13 | BRAIN3D.html deploy |

## BRAIN3D.html — interactive brain sphere

User asked for "the real brain, prompt-engineering designed, deployed,
beautiful, 360° rotation, FA+EN side-by-side explanations". Delivered as a
single dependency-free Canvas file at repo root (Pages-served, HTTP 200
verified). Technique notes live in
`agent-state-backup/references/manual-triggers-and-viz.md` §3.
JS validated with `node --check` on the extracted `<script>` body before
pushing. Bilingual pairing: green RTL Persian / blue LTR English blocks,
per-node popup card with both languages.

## Tooling notes

- `skill_manage(create)` enforces ≤60-char description; long text fails —
  put detail in the body.
- Background-curator writes require the exact SKILL.md/support file content
  to have been loaded via skill_view in the same review turn; re-view then
  retry, or add support files (write_file path under `references/`) which
  don't need prior load.
