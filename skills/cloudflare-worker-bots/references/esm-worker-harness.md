# Node harness for ESM `export default` workers (incl. embedded frontend)

Use when the worker is an ES module that Node cannot import directly — typically
because of `import ... from "cloudflare:sockets"` — or when it embeds its admin UI
as a template literal. Complements the bot-style harness in `cf-workers-api.md`.

## Export hook

Gate a test export on an env flag so production is unaffected:

```js
if (typeof globalThis.process !== "undefined" && globalThis.process.env.WORKER_TEST) {
  globalThis.__w = { pureFn1, pureFn2, apiRoute, subHandler };
}
```

Tests set the flag, then `await import("./worker.js")` and read `globalThis.__w`.

## Syntax checks (two passes)

1. Worker: copy to `worker.check.mjs` and run `node --check` (catches ESM parse errors).
2. Embedded browser JS: extract the `<script>...</script>` block to a temp file and
   `node --check` it as a classic script (catches errors inside the template literal
   that the worker check cannot see).

## Stubbing the unimportable

For a render/behavior smoke test, copy the worker to `/tmp`, replace the
`cloudflare:sockets` import line with a throwing stub, swap `export default {`
for a global assignment, append access to the internal render functions, and import
the copy. Assert on the rendered HTML: structure markers present (`id="nav"`, API
route strings), new-CSS markers present, deep-link formats intact.

Stub live third-party calls (`fetch` to registration/subscription APIs) with canned
`Response` objects and assert the parsed fields, not just HTTP 200.

## Verifying hand-rolled crypto (SHA, X25519)

Single-file workers often embed pure-JS crypto because WebCrypto lacks primitives
like X25519. Never trust a from-memory implementation — or a from-memory vector:

- Cross-check random inputs against the platform native: `node:crypto` subtle for
  X25519 (export raw public key vs your ladder on the same private key), and both
  `node:crypto` and `python3 hashlib` for hashes. 5/5 agreement beats any single vector.
- Localize ladder/formula bugs with algebraic edge cases first (e.g. identity element
  through the path) to find WHICH formula is wrong before rewriting.
- When a published known-answer vector disagrees with your code, re-derive the vector
  from two independent sources BEFORE touching the code — a vector copied for the
  wrong input sends you 'fixing' a correct implementation.

## Embedded-frontend pitfalls

- Never `location.reload()` on HTTP 401: the first unauthenticated visit then loops
  forever. Show the login screen instead; only boot the app after a successful
  `/api/me`.
- Read checkbox state with `.checked`, never `.value` (an unchecked box still has
  a value and the setting saves as always-on).
- Give QR `<img>` tags an `onerror` fallback message — the QR CDN is a runtime
  dependency that can be offline.
- Auto-refresh must be opt-in (default off), interval-gated, and skipped when the
  tab is hidden or the user navigated away; clear the timer on tab switch/logout.

## Proving a styling-only change

When the change must not touch logic, verify with `diff` hunk headers: every
changed line range must fall inside the `<style>...</style>` blocks, and the full
test suite must pass unmodified. State the hunk range in the delivery report.
