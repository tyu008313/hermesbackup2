Backup repo: github.com/tyu008313/hermesbackup2 (owner tyu008313). Full Hermes mirror (sessions, memories, skills, config, dashboard) synced every 12h; sections 01_CORE_ASSETS..05_SYSTEM_INTELLIGENCE + brain.html.
§
GitHub: SSH port 22 blocked on relay - push via HTTPS+token only (token in backup_repo remote URL). Scripts: /data/workspace/backup_scripts/ (run_backup.sh orchestrator + exports/dashboard/scrub); repo /data/workspace/backup_repo; log backup.log.
§
Security: transcripts may contain GitHub token - scrub.py runs before every push; tokens never in public repos nor on terminal command lines (scanner holds them for approval) - keep in files.
§
STATUS: LIVE. Pages serve brain.html + BRAIN3D.html (ui-ux-pro-max skill under creative/). Cron dd6bd38d99d4 every 12h no_agent=True -> ~/.hermes/scripts/hermes_brain_backup.sh -> execs run_backup.sh (edit THAT file).
§
Landing reza-landing DELETED 2026-08-24. Private repos lack Pages (422) - publish sites in PUBLIC repos only. CTA handle: @RG7YT.
§
User profile: REZA, Persian speaker - reply in Persian. Telegram handle @RG7YT. Design taste: dark, neon-glow, futuristic, interactive (360-degree rotation), bilingual FA+EN outputs. Expects every repo section kept in sync and human-readable; recurring jobs run script-only (no LLM tokens); gives quick decisive commands.
§
REZA is mid-way through a 7-day course (web basics + security + vibe coding) taught lesson-by-lesson in chat; started lesson 1 on 2026-08-25. Teaching style he asked for: ELI5-simple Persian, everyday analogies, small hands-on homework. Plan + progress: course_7day.md / course_progress.md in /data/workspace.
§
9router AI API: https://9router-production-df048.up.railway.app/v1, custom model X-muse (smoke-tested OK). Token lives in /data/workspace/.secrets/9router_token (never inline). Router quirks: JSON reply served as text/event-stream with trailing 'data: [DONE]' → parse with json raw_decode; intermittent 503s → retry. Tester script: /data/workspace/test_xmuse.py.