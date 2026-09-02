# 3x-ui Panel — Installation and Configuration

## Quick Install
```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

## Credentials (post-install)
```bash
cat /etc/x-ui/install-result.env
# Output: XUI_USERNAME, XUI_PASSWORD, XUI_PANEL_PORT, XUI_WEB_BASE_PATH, XUI_ACCESS_URL, XUI_API_TOKEN
```

## Manual Start (no systemd)
```bash
cd /usr/local/x-ui && ./x-ui &
```

## Change Port via SQLite
```bash
apt install -y sqlite3
sqlite3 /etc/x-ui/x-ui.db "UPDATE settings SET value='8080' WHERE key='webPort';"
sqlite3 /etc/x-ui/x-ui.db "SELECT * FROM settings;"
```

## Change Port via CLI
```bash
/usr/local/x-ui/x-ui setting -port 8080
```

## Expose via Cloudflare Tunnel
```bash
cloudflared tunnel --url http://localhost:8080 2>&1 &
# URL appears in output: https://xxx-yyy.trycloudflare.com
```

## Access Panel
```
https://TUNNEL_URL/XUI_WEB_BASE_PATH/
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `open bin/.config-xxx.tmp: no such file or directory` | Run from /usr/local/x-ui: `cd /usr/local/x-ui && ./x-ui` |
| Port 502 on Railway Public Domain | Railway only routes main service; use Cloudflare Tunnel |
| `systemctl` exit 127 | Use `service` or manual `./x-ui &` |
| Tunnel error 1033 | cloudflared crashed; restart it |
