Environment: Running on Railway; port 22 is closed. Use HTTPS for GitHub operations.
§
Trigger word "BACKUP" executes the backup script at ~/.hermes/scripts/backup_script.sh to sync to https://github.com/tyu008313/hermesbackup2.
§
کاربر در حال راه اندازی یک سایت فروشگاهی وردپرس بر روی پلتفرم Railway برای اهداف تست است. همچنین، وقتی کاربر درخواست اجرای کارهای پس زمینه (مانند بک آپ) را می دهد، ترجیح می دهد بلافاصله اجرا شوند و منتظر زمان زمان بندی شده نماند.
§
Railway API Token: 87c2a073-7eac-4a4a-9840-e826344fb699 (Use with caution: This token should ideally be set as an environment variable, not in memory. Access via RAILWAY_API_TOKEN).
§
Windows VPS target: 100.88.97.60 (user NvdAdmin) — a Tailscale CGNAT-range IP, not public; all direct ports filtered. Local Tailscale installed (userspace-networking, SOCKS5 localhost:1055); connection pending user approving a login.tailscale.com link. Pending task: speed test + remote admin once joined.
§
Telegram self-bot project (Miney game): single-file Telethon script; activates via '.ماین زمان X:Ym|Yh' sent in Saved Messages; auto-clicks green button «بفروشش بره» in group «ماین»; no logs allowed — only errors reported to Saved Messages. Note: telethon.errors has no MessageNotFoundError (ImportError bug in user's ff_bot.py).