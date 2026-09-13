---
name: browser-automation
description: "Drive web pages and forms via the browser tool."
version: 1.0.0
---

# Browser Automation

Fill forms, click through flows, and read pages with `browser_exec`, typing identifiers yourself and resolving every secret through the vault tools — never type or accept a password in chat or in page scripts.

## Procedure

1. Open the page, then probe before acting: run one cheap read call and confirm the target elements exist before any fill or click.
2. Type non-secret identifiers (email, username) with `fill_input`; fill passwords only via `browser_vault_fill`, and save new logins only via `browser_vault_save_login`.
3. Submit, then verify the outcome by reading state (URL plus page text) — never assume a click succeeded.
4. On any login wall with no saved item, stop and route the user to `hermes vault add` or the vault save flow instead of working around it.

## Pitfalls

- Probe element presence after every navigation before filling — SPA hydration races make immediate fills fail even though the selector is correct.
- Keep `js()` expressions free of nested backticks and template literals — the harness misparses them and the whole call fails.
- Check result text explicitly (error strings and URL) after submitting a form — staying on the same URL can mean either a silent failure or a pending second factor.
