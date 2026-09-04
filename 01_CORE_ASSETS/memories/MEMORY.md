Cron 'git-backup-daily' (0be211d06240) runs backup_daily.sh EVERY 12H (per user 2026-09-04, not daily-9am).
§
This Hermes host container has no /dev/net/tun and mknod is not permitted (Operation not permitted) — OpenVPN server cannot run here. Public IP seen 152.55.184.188 via curl. Prefer userspace VPN (Xray/VLESS + cloudflared) which needs no TUN.
§
Cron job 'git-backup-daily' (0be211d06240) is PAUSED by user request — do not resume without asking. Manual backups run via BACKUP skill (git-backup-manual).
§
VLESS /data/vless (pm2 xray-vless, Xray 26.3.27, UUID 1e423f99-2136-4af4-870f-62428403d088): WS 38003 /reza-vless-77 via CF flight-depending-castle-frame.trycloudflare.com (live), WS 8080 /reza-rail-ws via Railway domain (live), Reality :443 SNI www.microsoft.com pubkey 3M0GerrOvfS-rvZFFd7ndtkxItQR6txoxYFr2wBG9W8 sid ed739404 (local OK, inbound 443 filtered from internet). client.txt (3 links) + sub.txt + 3 QRs.
§
PLAIN XRAY + multi_router.py (Marzban REMOVED 2026-09-04): single pm2 xray-vless serves WS /reza-rail-ws :8080 (Railway) + /reza-vless-77 :38003 (CF) + VMess/Trojan/SS inners :8102/8103/8104 with RANDOM ws paths (CF edge flaky on plain words). Router :8095 (pm2 multi-router, Connection:close fix for tunnel keep-alive) + ONE CF tunnel serves all 3 protos. 5 links in /data/vless/client.txt + sub.txt. Chat :3000 + CF tunnel. Kill strays by exact PID (no pkill/pgrep on box); beware duplicate xray/routers fighting over ports.
§
Reza prefers plain Xray links over management panels — explicitly asked to remove Marzban and keep it simple like before.