---
name: python-telegram-bots
description: 'Single-file Python Telegram bots via PTB polling on Railway.'
---

# Python Telegram Bots

Build Telegram bots as one self-contained `bot.py` (python-telegram-bot v21, long-polling) that runs as a single Railway worker — verified locally with a mocked async harness before delivery.

## Procedure

1. Scaffold `bot.py` + `requirements.txt` (pinned: `python-telegram-bot==21.6`, `httpx==0.28.1`) + `Procfile` (`worker: python bot.py`) under `/data/workspace/<name>/`. Test locally in a venv (`uv venv`, `uv pip install -r requirements.txt`); delete the venv before delivery so the upload folder stays clean.
2. Architecture is polling-only: `run_polling(drop_pending_updates=True)`, no webhook, no web server, no external DB in v1 (memory-only state; document that a Railway restart wipes it). Read `BOT_TOKEN`/`OWNER_ID` from env; refuse to start with a clear message when the token is missing, and exit cleanly on `InvalidToken`. First `/start` claims owner under an `asyncio.Lock` so two simultaneous starters cannot both win.
3. Keep third-party user secrets strictly in handler-local variables: delete the user's message on receipt, never store/echo/log them, rebind and `del` after use, and mask them in the logging filter. Assert this in tests by scanning history, logs, and reports for the test secret.
4. Verify with a mocked async harness (see `references/ptb-polling.md`): fake User/Message/CallbackQuery/Bot classes, drive full flows (owner bootstrap, force-join gate, token flow, deploy, upload, admin matrix, search, ban, daily report), and finish with a live smoke run that must reach `run_polling` (an `InvalidToken` failure on a dummy token proves the polling path executes). When the user supplies real provider credentials, also verify the provider path end-to-end (see `references/ptb-polling.md` § Live provider verification): secrets from env vars only, deploy a canary, confirm it serves, then delete it.
5. Deliver the finished file as a native file attachment when it exceeds chat message limits; follow with the Railway checklist: GitHub repo → New Project → Variables (`BOT_TOKEN`, `OWNER_ID`) → Start Command `python bot.py` → single replica, no public domain, no webhook.

## Pitfalls

- When mocked PTB tests fail, suspect fixture/contract mismatch first (input formats, fixture size limits, multi-recipient counts) — reproduce against the real handler contract before editing bot code.
- Capture `reply_markup` in fake messages — PTB menus live in buttons, so asserting only message text silently misses the whole UI.
- Track every fake Message instance in a class registry — handlers create progress messages internally and their edits are unobservable otherwise.
- Guard the test entry point with `if __name__ == "__main__"` — importing the test module for debugging re-runs the suite and its `sys.exit` kills your debug snippet.
- A daily-report fan-out reaches the owner plus every admin with log permission — assert delivery to the owner, never an exact total of one.
- Skip `JobQueue` (needs the `job-queue` extra): an `asyncio` task spawned in `post_init` is a dependency-free scheduler that is polling-compatible.
- Never run two pollers on the same token — state the single-replica requirement in the deploy checklist every time.
