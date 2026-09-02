# 3x-ui Inbound + Hosts Configuration for Cloudflare CDN

## Port Conflict: Panel vs Inbound

x-ui panel (web UI) and xray inbound (VLESS WS) must use **DIFFERENT ports**.
Both defaulting to 8080 causes `address already in use` errors.

```bash
# Panel: port 8080 (web UI)
# Inbound: port 2083 (or any other free port)
sqlite3 /etc/x-ui/x-ui.db "UPDATE inbounds SET port=2083 WHERE id=1;"
```

## Update Hosts Table (Cloudflare CDN)

The hosts table tells x-ui what address/SNI to put in generated client configs.

```bash
# Check schema
sqlite3 /etc/x-ui/x-ui.db ".schema hosts"

# Update host for Cloudflare CDN
sqlite3 /etc/x-ui/x-ui.db "
UPDATE hosts SET
  address='YOUR-CF-TUNNEL.trycloudflare.com',
  port=443,
  security='tls',
  sni='YOUR-CF-TUNNEL.trycloudflare.com',
  alpn='[\"h2\",\"http/1.1\"]',
  fingerprint='chrome'
WHERE id=1;
"
```

## Update Inbound Stream Settings

```bash
sqlite3 /etc/x-ui/x-ui.db "
UPDATE inbounds SET stream_settings='{\"network\":\"ws\",\"security\":\"none\",\"wsSettings\":{\"acceptProxyProtocol\":false,\"path\":\"/\",\"host\":\"YOUR-CF-TUNNEL.trycloudflare.com\",\"headers\":{}}}'
WHERE id=1;
"
```

## After Changes: Restart x-ui

```bash
pkill -9 x-ui; pkill -9 xray
sleep 2
cd /usr/local/x-ui && exec ./x-ui 2>&1 &
```

## Generate VLESS Config

```
vless://UUID@CF-TUNNEL:443?encryption=none&security=tls&sni=CF-TUNNEL&type=ws&host=CF-TUNNEL&path=%2F#LABEL
```

## 3-Tunnel Architecture (Railway)

```
Tunnel 1: localhost:80    → Telegram Bot (Apache)
Tunnel 2: localhost:8080  → x-ui Panel (web UI)
Tunnel 3: localhost:2083  → Xray Core (VLESS WS inbound)
```

Each tunnel needs its own cloudflared process and gets a RANDOM URL on restart.
When any tunnel URL changes: update webhook, config.php, cron jobs, and hosts table.
