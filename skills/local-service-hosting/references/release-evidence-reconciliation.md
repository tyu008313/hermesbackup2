# Release evidence and review reconciliation

Use this checklist when an external reviewer, subagent, or stale build report describes a release blocker.

## Re-anchor the claim

Before accepting a finding, inspect the files and exact artifact named by the report. A review produced before later edits is a lead, not a current fact. Re-run the smallest reproduction from the current working tree; do not apply a historical audit wholesale.

Classify every finding as:

- **current blocker** — reproduced against the current entrypoint or package;
- **already fixed** — the current code has the correction, with a passing regression check;
- **stale** — the cited line, symbol, or snapshot no longer exists;
- **unproven** — the claim is plausible but the available test does not establish it.

Only the first category warrants a code change. Keep unresolved external claims in the release report.

## Avoid stale interpreter evidence

Long-lived Python kernels can retain an imported module after its source or JSON snapshot changes. For file-backed registries, generated config, and release metadata, run verification in a fresh subprocess with bytecode writing disabled. Print the module path and source snapshot identity alongside the result. A disagreement between a persistent kernel and a fresh process is evidence of stale state, not evidence that either release claim is true.

## Reconcile capability registries

Use one machine-readable registry as the source of truth and check the loader against it in a fresh process. Verify:

1. exact record count and unique IDs;
2. loader counts equal JSON counts;
3. every implementation and roadmap reference exists in the current tree;
4. `implemented` has reachable source, entrypoint/API wiring, and a repeatable test;
5. `partial` names the missing proof or narrower behavior;
6. `planned` has no implementation/test reference and does have a roadmap reference;
7. provenance points to the active implementation, not a legacy parallel module.

A source-only archive may omit tests for size or provider policy, but that omission must be explicit; it does not make a historical test reference prove current coverage.

## Gate the extracted artifact

Build from a clean allow-list, extract the exact archive into a fresh directory, and run checks from that extracted root. Verify root/flat shape and the absence of tests (if the policy excludes them), caches, binaries, secrets, runtime data, backups, and temporary files. Run syntax/import checks, authenticated and unauthenticated API probes, static-exposure probes, registry validation, and an HTML/JSON-aware smoke test. Do not assume every endpoint returns JSON; inspect the declared content type or use separate parsers.

## Keep evidence levels separate

A unit test proves a function contract. A local HTTP test proves routing and auth in one process. A generated Xray/edge configuration proves structure, not traversal. Only a real client/server/network or deployed smoke proves the corresponding E2E level. Never let a passing lower-level test upgrade a capability or release claim.

## Migrate credential verifiers safely

When changing a persisted authentication-verifier format, new writes should use a memory-hard KDF with a fresh random salt and bounded parameters. Keep legacy formats readable only through a deliberate migration path, reject attacker-controlled parameters, compare the final verifier in constant time, and test both legacy and new records. Never store the secret itself to make migration work; redact verifier material from public responses, logs, audit payloads, and release artifacts.
