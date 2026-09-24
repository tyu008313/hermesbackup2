# Railway Archive and Public-Domain Defaults

Use this recipe when a local panel must be uploaded as a ZIP to Railway or another service. First determine the required package shape: a flat repository/root, or one selectable service subfolder. The user's explicit shape wins; do not infer a subfolder from an older deployment convention.

## Package-shape decision

- **Flat/root:** use when the target accepts the repository root or the user explicitly requests one folder. All deployable files are directly at the ZIP root; there is no application-directory prefix.
- **Service subfolder:** use only when the provider requires a Root Directory or the user requests a named service folder. Put the complete service under one explicit directory such as `rixpanel/`, with the manifest beside `app.py`.

## Flat/root shape

```text
release/
├── app.py
├── server.py
├── config_builder.py
├── railway.json
├── requirements.txt
├── index.html
├── app.js
├── styles.css
└── test_*.py
```

The ZIP root is the execution root. The start command must not reference a nested app folder; for example, use `python3 app.py ...`. Run tests from the extracted root with a root-aware discovery pattern, then inspect the archive entries for an unwanted wrapper.

## Service-subfolder shape

```text
release/
└── rixpanel/
    ├── app.py
    ├── railway.json
    ├── requirements.txt
    ├── web/
    ├── rixpanel/
    └── tests/
```

The provider must be able to select `rixpanel` as **Root Directory**. Keep `railway.json` inside `rixpanel/`, alongside `app.py`. A wrapping directory is acceptable only when it does not obscure the selectable service root.

## Manifest checklist

- Builder: `RAILPACK` or a provider-supported equivalent.
- Start command binds to `0.0.0.0` and reads the provider-provided port.
- Healthcheck path is same-origin and does not require a secret.
- No secret is committed in variables, source, sample data, or logs.
- Static files are served from a directory resolved relative to `app.py`, not the process working directory.

## Archive checklist

- Exclude `data/`, generated JSON, `__pycache__/`, `.pytest_cache/`, `.venv/`, `node_modules/`, `.env`, keys, and certificates.
- Include tests and the manifest.
- List ZIP entries and confirm the service directory exists.
- Extract to a fresh temporary directory and run the full test suite there.
- Re-run the manifest syntax check after extraction.

## Public-host recipe

If the UI is meant to be zero-argument, populate the public hostname from the browser URL and make the field read-only. The API should accept an explicit domain, but when it is absent it may fall back to the first sanitized `X-Forwarded-Host` value and then the first sanitized `Host` value. Validate DNS names/IPs and reject schemes, paths, control characters, and malformed forwarded values. Generate UUIDs on the server and keep the listener address separate from the advertised server.

## Minimal verification set

- Explicit domain sets server, SNI, and Host.
- Omitted domain with forwarded host sets the same values.
- Omitted domain with only Host sets the same values.
- Invalid domain, URL, path, and control-character values return 422.
- UUID parses as a valid UUID and is not a fixed UI placeholder.
- Subscription Base64 decodes to the exact generated URI.
- No local data or credentials are present in the archive.

## Pitfall

A passing API test suite does not make a package deployable. The common failure is a flat ZIP when the host UI requires a service subfolder; the next common failure is an internal listener address being copied into a client configuration instead of the public proxy hostname.
