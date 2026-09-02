[REZA] Persian speaker, Telegram @RG7YT. Design: dark, futuristic, interactive, bilingual FA+EN. Course: 7-day web security + vibe coding (Lesson 1 done). Repo: github.com/tyu008313/hermesbackup2. 9router API active (X-muse). Interests: VPN/anti-censorship tools, MirzaPro2, MHRV-RS. VPS: Debian 13 (trixie) on cloud. Prefers: quick execution without lengthy confirmations, backup before destructive ops, Persian replies.
§
MirzaPro2 VPN Bot on Railway (ports 8080/443):
- Bot: @OXINNET_BOT, token 8691766146:AAHf...NQ, admin 7025776524
- DB: mirza_pro / Mirza@2026!Secure (MariaDB 11.8)
- 3x-ui v3.7.0: user=8sfaIDPFiK pass=Ys8lzIA86c port=8080 basePath=/edVa7HUn6PhwR2MYGv
- Xray: VLESS+WS port=2083 UUID=8af924af-92ac-46c0-a9c0-6b4042534995
- Cloudflare Quick Tunnels for bot(80), panel(8080), xray(2083) — URLs change on restart!
- Railway restart: re-launch MariaDB, Apache, x-ui, 3x cloudflared tunnels
- systemd unavailable — use `service` or background processes
- Fixes: checktelegramip() localhost, admin table, roll_Status=1
- Full context: github.com/tyu008313/hermesbackup2/blob/main/HERMES_FULL_CONTEXT.md
§
Full context: github.com/tyu008313/hermesbackup2/blob/main/HERMES_FULL_CONTEXT.md + HERMES_QUICK_START.md
Next session: load context file first.