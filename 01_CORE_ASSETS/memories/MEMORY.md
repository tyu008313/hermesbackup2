[REZA] Persian speaker, Telegram @RG7YT. Design: dark, futuristic, interactive, bilingual FA+EN. Course: 7-day web security + vibe coding (Lesson 1 done). Repo: github.com/tyu008313/hermesbackup2. 9router API active (X-muse). Interests: VPN/anti-censorship tools, MirzaPro2, MHRV-RS. VPS: Debian 13 (trixie) on cloud. Prefers: quick execution without lengthy confirmations, backup before destructive ops, Persian replies.
§
MirzaPro2 VPN Bot on Railway (ports 8080/443):
- Bot: @OXINNET_BOT, token 8691766146:AAHf...NQ, admin 7025776524
- DB: mirza_pro / Mirza@2026!Secure (MariaDB 11.8)
- 3x-ui v3.7.0: user=8sfaIDPFiK pass=Ys8lzIA86c port=8080 basePath=/edVa7HUn6PhwR2MYGv
- Xray: VLESS+WS port=2083 UUID=8af924af-92ac-46c0-a9c0-6b4042534995
- Cloudflare Quick Tunnels: bot(80), panel(8080), xray(2083) — URLs change on restart!
- systemd unavailable — use `service` or background processes
- Fixes: checktelegramip() localhost, admin table, roll_Status=1
- restart.sh: auto-restarts all services + new tunnel + webhook + cron
- monitor.sh: every 5 min, checks all services, auto-restarts if needed
- GitHub: github.com/tyu008313/hermesbackup2 (HERMES_FULL_CONTEXT.md + BOT_INSTALL_GUIDE.md)
§
Bot auto-monitor: monitor.sh runs every 5 min via cron. Checks Apache, MariaDB, port 80, webhook, cloudflared. Auto-restarts via restart.sh if issues. Log: monitor.log
§
Reza uses Railway hosting, hits limits. Prefers emoji-filled warm casual tone (NOT robotic). Gets emotional about outages. Wants auto-monitoring. Bot install guide: BOT_INSTALL_GUIDE.md. Next Hermes session: load HERMES_FULL_CONTEXT.md first.
§
VPN Server Docker files created: Dockerfile.railway, docker-compose.yml, QUICK_START.md. Full access with --privileged, TUN device, OpenVPN, WireGuard, Cloudflare Tunnel. Files in GitHub repo: tyu008313/hermesbackup2
§
Minimal VPN Server Docker files: Dockerfile.vpn, docker-compose.vpn.yml, README.vpn.md. Clean Ubuntu 22.04 with full access (privileged), TUN device, all networking tools, Apache, MariaDB, SSH. User installs what they need. Files in GitHub repo: tyu008313/hermesbackup2