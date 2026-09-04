#!/usr/bin/env bash
# Monitors the Marzban customer tunnel (proc_29d3d292414c -> marie-delivery-durable-buzz).
# If the tunnel dies, restarts cloudflared for the Marzban panel and updates
# XRAY_SUBSCRIPTION_URL_PREFIX in the Marzban .env so subs keep working.
set -uo pipefail

PANEL_PORT=127.0.0.1:8000
CF_BIN=/data/vless/cloudflared
envfile=/data/workspace/Marzban/.env
log=/tmp/cf-marzban.log

# current tunnel URL (saved by us)
CUR=$(grep -o "https://[a-z-]*\.trycloudflare\.com" "$log" 2>/dev/null | tail -1)
[ -z "$CUR" ] && CUR="marie-delivery-durable-buzz.trycloudflare.com"

# alive if cloudflared process is running AND panel answers
alive=0
if pgrep -f "tunnel --url http://127.0.0.1:8000" >/dev/null 2>&1; then
  code=$(curl -s -o /dev/null -w "%{http_code}" "$CUR/dashboard/" --max-time 12 2>/dev/null)
  [ "$code" = "200" ] && alive=1
fi

if [ "$alive" = "1" ]; then
  echo "TUNNEL-OK $CUR"
  exit 0
fi

echo "TUNNEL-DEAD restarting..."
# kill any stale cloudflared for this url
pkill -f "tunnel --url http://127.0.0.1:8000" 2>/dev/null
sleep 3
setsid "$CF_BIN" tunnel --url "http://$PANEL_PORT" --no-autoupdate > "$log" 2>&1 &
sleep 22
NEW=$(grep -o "https://[a-z-]*\.trycloudflare\.com" "$log" 2>/dev/null | tail -1)
if [ -n "$NEW" ]; then
  # update sub prefix in Marzban env
  sed -i "s|^XRAY_SUBSCRIPTION_URL_PREFIX = .*|XRAY_SUBSCRIPTION_URL_PREFIX = \"$NEW\"|" "$envfile"
  pm2 restart marzban >/dev/null 2>&1
  echo "TUNNEL-RENEWED $NEW"
else
  echo "TUNNEL-RENEW-FAILED (no new url)"
fi
