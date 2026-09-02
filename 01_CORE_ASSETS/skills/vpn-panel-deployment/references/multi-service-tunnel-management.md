# Multi-Service Cloudflare Tunnel Management

## Pattern: Multiple Services on Same Server

When running multiple services (e.g., Telegram bot + VPN panel) on one server without a domain, each needs its own Cloudflare Quick Tunnel.

```bash
# Service 1: Telegram bot (Apache port 80)
cloudflared tunnel --url http://localhost:80 2>&1 &
# URL: https://aaa-bbb.trycloudflare.com

# Service 2: VPN panel (x-ui port 8080)
cloudflared tunnel --url http://localhost:8080 2>&1 &
# URL: https://ccc-ddd.trycloudflare.com
```

**IMPORTANT:** Each tunnel gets a RANDOM URL. URLs change on every restart.

## Post-Restart Checklist

When ANY service restarts (container restart, process crash):

1. Check if cloudflared tunnels are running: `ps aux | grep cloudflared`
2. If tunnels died, restart them and get NEW URLs
3. Update Telegram webhook with new bot URL:
   ```bash
   curl -s "https://api.telegram.org/botTOKEN/deleteWebhook"
   curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://NEW_BOT_URL/index.php"
   ```
4. Update config.php `$domainhosts` with new bot URL
5. Update cron jobs with new bot URL:
   ```bash
   bash /var/www/mirza_pro/setup_cron.sh
   ```
6. Update any client configs that reference the panel URL

## Getting Tunnel URL from Logs

```bash
# Find the URL in cloudflared output
ps aux | grep cloudflared
# Look for "https://xxx-yyy.trycloudflare.com" in the log

# Or check process output:
# The URL appears as: "Your quick Tunnel has been created! Visit it at: https://..."
```

## Quick Tunnel Limitations

- URLs are RANDOM and CHANGE on restart
- No uptime guarantee
- Not suitable for production
- Cloudflare may throttle or block abuse

## Production Alternative

For permanent setup:
1. Buy a domain
2. Point DNS to server IP
3. Use Certbot for SSL
4. Or use Cloudflare Named Tunnel (requires Cloudflare account)

## Railway-Specific Notes

- Railway Public Domain only routes to the main process PORT
- Other services MUST use Cloudflare Tunnel
- `systemctl` is unavailable; use `service` or manual process management
- After container restart, all background processes (cloudflared, x-ui) die
