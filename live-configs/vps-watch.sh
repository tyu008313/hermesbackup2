#!/bin/bash
# VPS watchdog (no_agent cron): quiet when healthy, speaks only on action.
# Keeps twbyt68-crypto/vps "Windows Cloud RDP" alive + verifies Tailscale SSH.
exec 9>/tmp/vps-watch.lock
flock -n 9 || exit 0

export GH_TOKEN
GH_TOKEN=$(cat /data/.gh_token)
REPO="twbyt68-crypto/vps"
WF_ID="340030765"
TS_SOCK="/data/.tailscale/tailscaled.sock"
export SSHPASS
SSHPASS=$(cat /data/.vps_ssh_pass)

ts_ips() {
  tailscale --socket="$TS_SOCK" status --json 2>/dev/null | python3 -c \
    "import json,sys
try:
  d=json.load(sys.stdin)
  print(' '.join(p['TailscaleIPs'][0] for p in d.get('Peer',{}).values() if p.get('HostName','').startswith('github-rdp-server')))
except Exception: print('')"
}

ssh_ok() {
  [ -n "$1" ] || return 1
  timeout 25 sshpass -e ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
    -o KexAlgorithms=curve25519-sha256 -o HostKeyAlgorithms=ssh-ed25519 -o CASignatureAlgorithms=ssh-ed25519 \
    -o ProxyCommand='nc -X 5 -x localhost:1055 %h %p' "NvdAdmin@$1" "hostname" 2>/dev/null | grep -qi .
}

ssh_any_ok() {
  for ip in $(ts_ips); do ssh_ok "$ip" && { echo "$ip"; return 0; }; done
  return 1
}

cancel_stale_runs() {
  local keep="$1"
  gh api "repos/$REPO/actions/workflows/$WF_ID/runs?per_page=5" \
    --jq '.workflow_runs[] | select(.status=="in_progress" or .status=="queued") | .id' 2>/dev/null \
    | grep -v "^$keep$" | while read -r rid; do
        gh api -X POST "repos/$REPO/actions/runs/$rid/cancel" >/dev/null 2>&1 \
          && echo "Cancelled stale run $rid"
      done
}

tailscale --socket="$TS_SOCK" status >/dev/null 2>&1 || { pm2 resurrect >/dev/null 2>&1; sleep 8; }

RUN_JSON=$(gh api "repos/$REPO/actions/workflows/$WF_ID/runs?per_page=1" \
  --jq '.workflow_runs[0] | {id, status, conclusion, created_at}' 2>/dev/null)
STATUS=$(echo "$RUN_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
RUN_ID=$(echo "$RUN_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
CREATED=$(echo "$RUN_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('created_at',''))" 2>/dev/null)
AGE_MIN=$(( ($(date +%s) - $(date -d "$CREATED" +%s 2>/dev/null || echo 0)) / 60 ))
GOOD_IP=$(ssh_any_ok)

if { [ "$STATUS" = "in_progress" ] || [ "$STATUS" = "queued" ]; } && [ "$AGE_MIN" -lt 15 ]; then
  [ -n "$GOOD_IP" ] && exit 0
  exit 0
fi

if [ -n "$GOOD_IP" ] && { [ "$STATUS" = "in_progress" ] || [ "$STATUS" = "queued" ]; }; then
  exit 0
fi

echo "DOWN detected (run=$STATUS age=${AGE_MIN}m). Dispatching fresh run..."
gh api "repos/$REPO/actions/workflows/$WF_ID/dispatches" -f ref=main >/dev/null 2>&1 \
  && echo "Dispatch OK, polling up to 12min for the new runner IP..." || { echo "Dispatch FAILED"; exit 1; }
GOOD_IP=""
for i in $(seq 1 12); do
  sleep 60
  GOOD_IP=$(ssh_any_ok)
  if [ -n "$GOOD_IP" ]; then break; fi
done
if [ -n "$GOOD_IP" ]; then
  echo "RECOVERED: SSH OK ($GOOD_IP)"
  NEWEST=$(gh api "repos/$REPO/actions/workflows/$WF_ID/runs?per_page=1" --jq '.workflow_runs[0].id' 2>/dev/null)
  cancel_stale_runs "$NEWEST"
else
  echo "NOT YET: SSH not ready, next tick retries"
fi
