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

## Deployment Packaging for PaaS and Root-Directory Uploaders

Treat the archive shape as an explicit decision, not a default. Determine whether the target accepts a flat repository/root or requires a selectable service subfolder, and honor the user's stated shape. Never convert a requested flat package into a nested package because an earlier convention suggested it.

For every PaaS archive:

1. Create a clean staging directory, not the live working directory.
2. Copy only source, tests, dependency manifests, and deployment configuration.
3. Exclude local databases, generated data, virtual environments, caches, credentials, and secret files.
4. Add a repository-level README that states the exact package shape, build command, start command, healthcheck path, and required environment variables.
5. Validate the deployment manifest and the extracted archive itself; run the test suite from the extracted copy at the package's documented execution root, not only from the original workspace.
6. List ZIP entries and verify the shape matches the request before reporting delivery: flat means no application-directory prefix; subfolder means the selected service directory exists.
7. Report the archive path, checksum, package shape, and exact root-directory setting.

### Flat/root package

Use this when the user says “بدون subfolder,” “همه‌چیز در یک فولدر,” or the target accepts the repository root. Put `app.py`, the manifest, dependency files, static assets, and tests directly at the archive root. Keep imports, start commands, and static paths relative to that root; do not leave an extra wrapper or service directory. Run tests from the extracted root, for example `python3 -m unittest discover -s . -p 'test_*.py' -v`, then smoke-test the extracted service.

### Service-subfolder package

Use this only when the target UI explicitly requires a Root Directory or the user requests a named service folder. Put the complete service under one explicit directory such as `rixpanel/`, keep `railway.json` beside `app.py`, and make its start command relative to that selected service root. A wrapping directory is optional only when the provider can select the service directory; inspect the resulting entries to avoid an accidental extra level.

**Pitfall:** package shape is a contract, not a cosmetic choice: a flat ZIP with an unwanted `rixpanel/` prefix fails a user who asked for one folder, while a service subfolder can be required by a provider that exposes no root selection. Re-read the request and inspect `ZIP.namelist()` before sending the artifact.

## Automatic Domain and Configuration Defaults

For a public self-service panel, derive connection parameters from the request's public host when the user should not manually configure technical fields. Resolve the browser/public hostname in the UI, and let the API accept an explicit `domain` or, when absent, derive it from `X-Forwarded-Host` and then `Host`. Keep the derivation centralized and validate the result before using it in links or configuration output.

Generate per-record values such as UUIDs on the server, not as fixed UI placeholders. Keep the UI's required fields minimal: a read-only, auto-filled public hostname plus one action is preferable to exposing duplicated technical fields. Add tests for the happy path, invalid URL/path/control-character domains, explicit-domain precedence, forwarded-host behavior, and the exact generated subscription decoding to the generated URI.

**Pitfall:** treating an internal listener address as the advertised proxy server makes locally valid configs fail in production. Always separate the bind address from the public server/SNI/Host values and test the public-host path explicitly.

## Security and Release Gates

For a service that can be exposed beyond a local process, treat security and release claims as fail-closed:

1. Default management APIs to authentication required. Parse boolean environment flags with an explicit truth table; test missing or invalid credentials as `401` and valid credentials as a successful response.
2. Keep runtime state and secrets outside the public static root. Serve an allow-list of named UI assets, and regression-test source, traversal, config, key, and registry requests as non-public.
3. Write credential-bearing files atomically with owner-only permissions (`mkstemp` + `fchmod` + `fsync` + `os.replace`); test the modes of the actual persisted files, not only the in-memory object.
4. Separate evidence levels: unit/config generation, local HTTP integration, real protocol/network E2E, and deployed-service verification. Never describe a lower level as live E2E or production readiness.
5. Treat capability registries as claims. Every implemented status needs a reachable implementation and a repeatable test; a record count is not proof of complete functionality.
6. When an asynchronous or external review arrives after edits, re-open the current tree and reproduce every finding against the current entrypoint and package; classify it as current, fixed, stale, or unproven before changing code. Run file-backed registry/import checks in a fresh interpreter because a persistent Python kernel can retain stale modules and report false counts or permissions.
7. After packaging, extract the exact archive and run syntax/import, auth, static-exposure, secret-leak, and smoke checks from the extracted root. Report test output and unresolved blockers separately.

For the detailed reconciliation checklist, see `references/release-evidence-reconciliation.md`.

**Pitfall:** a green unit suite can coexist with a production-bootstrap bug because unit fixtures instantiate dependencies that `main()` forgets to wire. Add a production-bootstrap integration test and test environment parsing in a fresh process.

For a compact evidence table and release checklist, see `references/security-release-gates.md`.

## Fast Iterative Delivery

When the user says to be quick, stop expanding scope after the requested vertical slice is working. Finish the smallest complete artifact, run the real tests and smoke checks, package it, and state limitations plainly. Do not keep an optional reviewer or research subtask running just to produce a more exhaustive report.


- Assume the port only after reading the startup line — a `PORT` env var on the host silently overrides code defaults, and probing the wrong port looks like a dead server.
- Parse URL path segments by splitting on `/`, never with non-greedy regex groups — a lazy `([^/]+?)` matches minimally and truncates the segment (the mechanism: the regex engine satisfies the overall match with the fewest characters, dumping the remainder into the trailing `(.*)`).
- A `curl` probe that returns empty with exit 0 means connection failure, not an empty API response — check the server log before blaming application code.
- When an API call fails inside the server but succeeds in a one-off shell test with identical headers, suspect request construction (wrong path parameter from parsing), not the network — add one temporary log line of the exact outbound values, then remove it.
- After redeploying a UI, prove what the server actually serves before debating it — `curl` the page and grep for a marker only the new version contains (or compare byte size). If the marker is present, the staleness is browser cache, so tell the user to hard-refresh instead of redeploying again.
