# Cloudflare Workers Scripts API — condensed notes for deployer bots

Base: `https://api.cloudflare.com/client/v4` — auth: `Authorization: Bearer <token>`.

## Upload (service-worker format)

`PUT /accounts/{accountId}/workers/scripts/{scriptName}` — multipart/form-data:

- part `metadata` (application/json): `{"body_part": "script"}`
- part `script` (application/javascript): the raw source

Success: `{"success": true, ...}`. On failure, surface `errors[].message` verbatim to the user — it almost always names the missing token permission.

## workers.dev URL

1. Best-effort enable: `POST /accounts/{id}/workers/scripts/{name}/subdomain` body `{"enabled": true}`
2. Read: `GET /accounts/{id}/workers/subdomain` → `result.subdomain`
3. Login URL: `https://{scriptName}.{subdomain}.workers.dev`
4. If the account has no subdomain, report the dashboard link instead of a dead URL.

## Delete

`DELETE /accounts/{id}/workers/scripts/{name}` — same error surfacing as upload.

## Token permissions the user must tick (Edit Cloudflare Workers template + Account Settings Read)

- Workers Scripts → Edit
- Account Settings → Read (subdomain lookup)

Token creation link to hand users: `dash.cloudflare.com/profile/api-tokens`.

## Bot's own deployment checklist (tell the user every time)

1. Workers & Pages → Create → paste `worker.js` → Deploy
2. Create KV namespace (e.g. `vodi-deployer-db`), bind to the worker with variable name `DB`
3. Settings → Variables: `BOT_TOKEN` (Telegram token; optional `OWNER_ID`, `ADMIN_IDS`)
4. Webhook: open `https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<worker>.workers.dev/webhook`
5. Triggers → Cron (e.g. `30 4 * * *` for 08:00 Tehran) or `scheduled()` never fires
6. First `/start` user becomes owner automatically

## Local Node test-harness recipe

- `package.json` with `{"type": "module"}`, test file imports `./worker.js` directly.
- Stub `globalThis.addEventListener` to capture the fetch handler before import.
- Mock `globalThis.fetch` with routes in most-specific-first order; return `Response` objects (`.json()` / `.arrayBuffer()` both needed).
- Map-backed KV mock implementing `get` (honor `{type:'json'}`), `put`, `delete`, `list({prefix, limit})`.
- Standard assertions: owner bootstrap, exact CF PUT/DELETE URLs, user secret message deleted, secret string absent from all stored values, all `callback_data` ≤ 64 bytes, scheduled() delivers to owner + admins.
