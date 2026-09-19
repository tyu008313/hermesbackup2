# PTB polling: mock harness, API notes, Railway

## Mock-harness recipe (no network)

- Set `BOT_TOKEN=DUMMY` before importing the bot so module init never touches the network.
- Fake classes, all async methods: `User(id, username, first_name)`; `Message` with `reply_text/reply_html` (capture text AND `reply_markup`), `edit_text` (capture), `delete` (flag); `CallbackQuery(data, from_user)` with `answer()` (flag) and `edit_message_text` (capture text + markup); `Bot` with `send_message` (log) and `get_chat_member` (scriptable membership); uploaded-file stub with `download_to_drive(path)` writing bytes.
- Build a bare-namespace update object per call (`type("U", (), {...})`) exposing exactly what the handler reads (`effective_user`, `message`, `callback_query`).
- Zero out flood/cooldown constants in the harness so rapid sequential calls are not throttled.
- Assert provider calls by monkeypatching them (validate/deploy/delete) and checking arguments; assert exact deploy URLs.
- Assert secret hygiene: the test secret string must appear in no reply, edit, stored history entry, audit record, error record, or daily report.
- Verify `q.answer()` was called on every callback query exercised.

## PTB v21 notes

- `Application.handlers` is a dict of lists; total handler count is `sum(len(h) for h in app.handlers.values())`. Error handlers live in `app.error_handlers` (plural).
- `run_polling` performs `getMe` during initialize, so a run with a dummy token fails with `telegram.error.InvalidToken` — that failure location proves boot reached polling. Catch it in `__main__` for a clean message.
- `CallbackQueryHandler(on_callback)` with no pattern plus `MessageHandler(filters.TEXT & ~filters.COMMAND, router)` and a final `MessageHandler(filters.COMMAND, unknown)` covers the whole surface.
- Always `answer()` a callback query first and tolerate old/invalid-query exceptions; never let one update kill polling — the global error handler must only send user-safe messages with short `ERR-XXXX` ids.

## HTTP / upload notes

- Every external request gets an explicit timeout; retry with backoff only transient failures (timeout, 429, 5xx) and never auth failures (401/403).
- ZIP uploads: validate extension, size cap, and UTF-8 decoding; run the zip-slip guard over ALL namelist entries before reading any member; require a worker marker in the extracted source; manage the result internally under the fixed logical name `worker.js` regardless of the uploaded filename.
- For Cloudflare Workers deploy-target endpoints and multipart shape, see `cloudflare-worker-bots` `references/cf-workers-api.md`.

## Live provider verification (real credentials)

- Pass secrets only via env vars; they must never appear in code, files, logs, tool output, or chat. Any credential the user pasted in chat is compromised — tell them to roll it after the test.
- Order: provider token-verify → deploy a canary script → poll the served URL with retries → DELETE the canary → report the real URL and timings.
- workers.dev needs 30–60s propagation: an immediate 4xx on a fresh deploy usually means 'not propagated yet', not 'deploy failed' — wait and re-poll before concluding.
- A single provider 400 against valid credentials proves nothing — re-hit the provider's token-verify endpoint several times, since transient auth failures happen; only consistent rejection means a bad credential.

## Railway notes

- `Procfile`: `worker: python bot.py`. Start Command setting: `python bot.py`.
- Variables: `BOT_TOKEN` required, `OWNER_ID` optional (empty means first `/start` claims owner).
- No public domain, no webhook, one replica. Memory-only state is wiped on restart — say so in the delivery notes.
