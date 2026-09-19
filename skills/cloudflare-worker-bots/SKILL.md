---
name: cloudflare-worker-bots
description: 'Build Telegram bots and VPN management panels as single-file Cloudflare Workers.'
---

# Cloudflare Worker Bots

Build Telegram bots and VPN management panels (VLESS/Trojan) as one self-contained `worker.js` (ESM, `export default { fetch }`).

## Procedure

1. Scaffold `worker.js` + `package.json` (`{"type":"module"}`) under `/data/workspace/<name>/` so Node can import the worker directly for tests.
2. VPN Panels: Handle all WebSocket traffic (VLESS/Trojan) with `cloudflare:sockets`, upgrade HTTP 101 immediately, and process traffic in `ctx.waitUntil`.
3. Admin UI (SPA): Manage dashboard routes via internal SPA states (hidden/active sections) to avoid page refreshes. Use `localStorage` for theme state (Dark/Light).
4. Clean IP Handling: For VPN panels, add a `cleanIPs` KV key to store lists of clean IPs. Inject these dynamically into the VLESS/Trojan links returned by `buildLinks` to keep subscriptions optimized.
5. Third-party Secrets: Keep user-provided tokens/secrets in request memory only. Never `KV.put` secrets.
6. Verify: Use a Node harness that stubs `fetch` and KV.
7. Enforce Telegram/Cloudflare limits: every `callback_data` ≤ 64 bytes.

## Pitfalls

- SPA Routing: In `adminHtml`, use a central JS dispatcher for tab navigation to avoid logic overlaps.
- Clean IP Injection: Ensure `buildLinks` iterates over provided IP lists and updates link names (e.g., `NAME (Clean)`) for clarity in clients.
- Styling: When implementing Light/Dark modes, ensure styles are scoped to a body class (e.g., `body.light`) and use CSS variables for full palette swapping.
- Security: Never expose sensitive settings (like `panelPass`) in API responses (`getSettings`).
- Syntax: Use a linter or `node --check` after every patch of the UI; template literals in large JS files often break on mismatched braces.

## References
- `references/cf-workers-api.md`: API, quotas, deployment.
- `references/esm-worker-harness.md`: Test scaffolding for ESM workers.
