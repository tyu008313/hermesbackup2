---
name: web-reconnaissance
description: Identify web tech stack and hosting from URLs.
tags: [recon, web, investigation, hosting, cloudflare, telegram]
version: 1.1.0
---

# Web Reconnaissance

Systematically investigate unknown URLs to identify what they are, where they're hosted, and what technology powers them.

## Workflow

### Phase 1: Headers and HTTP Properties
```bash
curl -sv "https://TARGET" 2>&1 | grep -E "^[<>*]|cf-|server:|content-type|x-|set-cookie"
curl -s "URL" -w "\nHTTP: %{http_code} | Type: %{content_type} | Size: %{size_download}B | IP: %{remote_ip}\n" -o /dev/null
```

### Phase 2: Content Probing
Probe common paths: `/`, `/index.php`, `/config.php`, `/.env`, `/admin.php`, `/composer.json`, `/README.md`, `/logs/runtime.log`

| Response | Meaning |
|----------|---------|
| 200 + empty body | Catch-all route (tunnel/proxy) |
| 403 Forbidden | Access control (.htaccess, directory listing off) |
| 500 + custom msg | PHP app error |
| composer.json 200 | PHP/Composer project |

### Phase 3: DNS and IP
```bash
python3 -c "import socket; print(socket.gethostbyname('DOMAIN'))"
curl -s "https://ipinfo.io/IP/json"
```
- AS13335 = Cloudflare edge (real IP hidden)
- `*.trycloudflare.com` = Quick Tunnel (temporary, free)

### Phase 4: SSL Certificate
```bash
curl -sv "https://TARGET" 2>&1 | grep -A2 "Server certificate"
```

### Phase 5: GitHub Source Research
Search repos, check releases for binaries with sizes.

### Phase 6: Telegram Bot Verification
If the URL is a Telegram bot webhook, verify the bot:
```bash
# Get bot info (confirms token is valid)
curl -s "https://api.telegram.org/botTOKEN/getMe"
# Returns: {"ok":true,"result":{"id":...,"username":"BOT_NAME",...}}

# Check current webhook status
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo"
# Returns: {"ok":true,"result":{"url":"...","has_custom_certificate":false,...}}

# Delete webhook (if needed)
curl -s "https://api.telegram.org/botTOKEN/deleteWebhook"
```

**Key insight:** A webhook URL returning empty 200 on GET is normal — Telegram bots only accept POST from Telegram servers.

## Pitfalls
- Cloudflare Quick Tunnel IPs are edge IPs, not real server.
- Empty 200 on all paths = catch-all proxy route, use `curl -sv` for real info.
- `dig`/`nslookup` often missing — use python3 socket instead.
- `systemctl` may not exist in containers — use `service`.
- Telegram requires HTTPS for webhooks. Self-signed certs work for Telegram but not browsers.
- Bot token URLs that return 404 = invalid token or bot was deleted.
