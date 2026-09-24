# Security and Release Gates

Use this reference when packaging a Python service with authentication, runtime state, network/proxy behavior, or a capability registry.

## Evidence ladder

| Evidence | Proves | Does not prove |
|---|---|---|
| Unit/config test | A function or generated structure matches its contract | Real process startup, auth wiring, or network behavior |
| Local HTTP integration | Routes, status codes, auth, and static serving work in one process | Public deployment, real proxy, or real client traversal |
| Protocol/network E2E | A real client and server traverse the deployed data path | Multi-region failover, geo correctness, or long-term operations |
| Deploy verification | The exact packaged artifact starts and answers in the target environment | Capabilities not exercised by the smoke path |

Label the highest achieved level explicitly. A generated Xray dictionary is config evidence, not live E2E; a heartbeat age is registry evidence, not node connectivity; a country label in metadata is not measured exit geo.

## Fail-closed checklist

- Management APIs require a real token by default. Parse `RIX_REQUIRE_ADMIN` and similar flags without `bool("0")`; use an explicit false set such as `{0, false, no, off}`.
- Public static serving is an exact allow-list, never a directory walk rooted at the application root. Reject source, data, key, config, and traversal paths with a regression test.
- Credential-bearing files use an atomic create/replace flow and owner-only mode (`0600` on POSIX). Test the persisted file mode after both creation and replacement.
- Node/proxy/join secrets never appear in successful public responses, audit payloads, capability registries, logs, or release archives.
- Join and lifecycle operations require a one-time or scoped credential; missing credentials fail with a JSON error, not a closed connection.
- A production bootstrap test must inspect the actual entrypoint wiring, not only a test fixture that manually injects every dependency.
- Health must distinguish process liveness from data-path health and must not report a static `ok` when a required supervisor is unavailable.

## Capability honesty

A registry is a contract, not evidence. Before setting a status to implemented, verify all of the following:

1. A reachable implementation exists in the shipped source.
2. The capability is wired into the production entrypoint, not only a standalone library.
3. A repeatable test exercises the relevant path and expected failure modes.
4. The registry reference points to files that exist in the current tree.
5. The release report states any missing external dependency or untested environment.

Never convert `partial` to `implemented` merely to satisfy a requested count. If external geo, UDP, mesh, failover, Docker, Railway, or live E2E evidence is unavailable, keep the capability partial and name the missing proof.

## Extracted-package gate

Build from an allow-list, extract the exact ZIP into a clean directory, then run from that extracted root:

```bash
python3 -m py_compile app.py server.py config_builder.py proxy_nodes.py node_lifecycle.py
node --check app.js
python3 -m unittest discover -s . -p 'test_*.py' -q
```

If the release intentionally omits tests, run a small HTTP smoke from the extracted package instead and document that limitation. Check `ZIP.namelist()` for flat/root-level shape and scan for test files, caches, binaries, logs, temporary files, keys, and generated data. Verify public UI, authenticated API, unauthenticated rejection, and non-public source paths with real requests; do not infer these from the working tree alone.
