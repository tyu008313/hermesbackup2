---
name: local-service-hosting
category: software-development
description: 'Use when running a local web service or bot on this host.'
---

# Local Service Hosting

Build small host-local services (web UIs, downloader APIs, Telegram bots) so they run immediately with zero installs, under writable paths, as tracked background processes, verified over HTTP before reporting success.

## Procedure

1. Scaffold the project under `/data/workspace/<name>/` — that tree is writable by file tools; the login home may not be. If the user expects files in their home, sync with `cp` via terminal afterwards.
2. Prefer stdlib-only implementations (e.g. `http.server` + `urllib` in Python) so the service starts with no package installs. Reach for a framework only when stdlib genuinely cannot do the job.
3. Start daemons with `terminal(background=true, notify=true)` — never shell-level wrappers (`nohup`, `&`, `disown`); the runner rejects those and only tracks processes it started itself.
4. Read the REAL bound address from the process startup log (`process_manage` poll/log), then verify with `curl` (`/`, then each API route with a real-world input) before telling the user it is up.
5. Stop by exact PID (`ps` + `grep "[p]attern"`, then kill that PID) — never a broad pattern kill; the pattern matches your own invoking shell's command line and kills it too.
6. When the user supplies a bot/API token in chat: validate it first against the provider's identity endpoint (e.g. Telegram `getMe`), persist it to a `chmod 600` dotfile inside the project dir, inject via environment at launch, and never repeat the secret back in replies.
7. Report briefly: what runs, where (host:port), what was verified by real requests, and what is still missing (e.g. tokens the user must supply).

## Pitfalls

- Assume the port only after reading the startup line — a `PORT` env var on the host silently overrides code defaults, and probing the wrong port looks like a dead server.
- Parse URL path segments by splitting on `/`, never with non-greedy regex groups — a lazy `([^/]+?)` matches minimally and truncates the segment (the mechanism: the regex engine satisfies the overall match with the fewest characters, dumping the remainder into the trailing `(.*)`).
- A `curl` probe that returns empty with exit 0 means connection failure, not an empty API response — check the server log before blaming application code.
- When an API call fails inside the server but succeeds in a one-off shell test with identical headers, suspect request construction (wrong path parameter from parsing), not the network — add one temporary log line of the exact outbound values, then remove it.
- After redeploying a UI, prove what the server actually serves before debating it — `curl` the page and grep for a marker only the new version contains (or compare byte size). If the marker is present, the staleness is browser cache, so tell the user to hard-refresh instead of redeploying again.
