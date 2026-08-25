---
name: llm-api-integration
description: "Wire up and load-test OpenAI-compatible LLM API endpoints."
version: 1.0.0
---

# LLM API Integration & Testing (OpenAI-compatible routers)

For tasks like "bring up a site/app on this token + base URL, set model X, run N tests".

## Workflow
1. **Token hygiene FIRST**: write the token to a file (e.g. `/data/workspace/.secrets/<provider>_token`,
   chmod 600). Never put it on a terminal command line — the security scanner holds such
   commands for approval and the token can leak into transcripts/backups.
2. **Discover**: `GET {BASE}/models` with Bearer auth — confirm the exact model id
   (routers often expose several similar ids; pick precisely what the user named).
3. **Smoke test**: 1 tiny completion asking for an exact fixed string; verify round-trip.
4. **Load test**: N requests, mixed verifiable prompts (math/lang/json/count), thread pool
   (~8 workers), per-request PASS/FAIL with sanity assertions, report pass-rate + avg latency.
5. Report honestly; never fabricate results for failed runs.

## Robust client rules (Python stdlib urllib is enough)
- Retry 3x w/ backoff on 429/500/502/503/504 — routers throw intermittent 503s.
- Parse leniently: some routers serve the JSON body as `text/event-stream` and append a
  trailing `data: [DONE]` chunk to it, so plain `json.loads` fails with "Extra data".
  Use `json.JSONDecoder().raw_decode(text.strip())` to take the leading JSON object.
  More quirks: `references/router-quirks.md`.
- Working example kept at `/data/workspace/test_xmuse.py` (smoke + 100-test runner).

## Front-end rule
A browser-facing page must NOT embed the token. If the site needs the model, proxy through
a backend/serverless function holding the key server-side.
