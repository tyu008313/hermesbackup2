#!/bin/bash
# Starter: script-only webpage condition watchdog.
# Copy into the scripts dir, fill the CONFIG block, run once to verify silence.
set -euo pipefail

# ---- CONFIG ----
URL="https://example.com/"                 # page to poll
SANITY='"price":"2.49"'                     # must-match anchor proving the right page loaded (grep -qi)
ABSENT_PATTERN="currently unavailable"  # condition flips when this text DISAPPEARS (grep -qi)
STATE_FILE="/data/.hermes/state/example_watch.state"
ALERT_MSG="Condition flipped! Check: ${URL}"
# ----------------

PAGE=$(curl -s -m 30 -A "Mozilla/5.0 (X11; Linux x86_64)" "$URL")

# Unknown on failed/truncated/wrong fetch: silent, keep old state.
if [ -z "$PAGE" ] || [ "${#PAGE}" -lt 20000 ]; then
  exit 0
fi
if ! echo "$PAGE" | grep -qi "$SANITY"; then
  exit 0
fi

PREV=$(cat "$STATE_FILE" 2>/dev/null || echo "UNKNOWN")

if echo "$PAGE" | grep -qi "$ABSENT_PATTERN"; then
  echo "UNAVAILABLE" > "$STATE_FILE"
  exit 0
else
  if [ "$PREV" != "AVAILABLE" ]; then
    echo "AVAILABLE" > "$STATE_FILE"
    echo "$ALERT_MSG"
  fi
  exit 0
fi
