---
name: web-watchdog
description: "Use when polling a webpage for a condition change."
version: 1.0.0
---

# Web Watchdog

Poll a public webpage on a script-only (`no_agent`) cron schedule and announce only when a watched condition flips. No LLM runs per tick; the script itself decides silence vs alert. See `templates/watchdog.sh` for the starter script.

## Procedure

1. Prove the condition is curl-visible first: fetch the page in the foreground and confirm both the present-state marker and the flipped-state absence in raw HTML — curl sees a different DOM than browser-rendered text, so never schedule off `innerText` alone.
2. Copy `templates/watchdog.sh` into the scripts dir and set URL, sanity anchor, unavailable pattern, state path, and alert text.
3. Run the script once in the foreground and confirm it exits silent with the state file written.
4. Create the cron job as `no_agent` with `script` set to the bare filename only — bake every argument into the script itself.
5. Confirm the job is scheduled; the first alert fires only on a real transition.

## Pitfalls

- Treat every failed or truncated fetch as unknown: exit silent and never touch the state file — an error page missing the marker looks exactly like the flipped condition and fires a false alert.
- Anchor each fetch with a sanity marker proving the right page loaded before evaluating the condition — a length check alone still passes on block or captcha pages.
- Alert only on transitions (stored state differs), never on every tick in the flipped state — otherwise each run re-announces.
- Pass only a bare script filename to a `no_agent` cron job — the scheduler resolves it under the scripts dir and treats extra tokens as part of the filename.
