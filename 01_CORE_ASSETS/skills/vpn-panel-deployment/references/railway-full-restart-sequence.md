# Railway Full Restart Sequence — فلوچارت ریستارت کامل

بعد از هر بار restart شدن Railway container، این مراحل رو به ترتیب اجرا کن:

## مراحل ریستارت

```bash
# 1. MariaDB (خودکار استارت نمیشه!)
service mariadb start

# 2. Apache
service apache2 start

# 3. x-ui + Xray
cd /usr/local/x-ui && exec ./x-ui 2>&1 &

# 4. Cloudflare Tunnels (هر کدام جداگانه)
cloudflared tunnel --url http://localhost:80 2>&1 &     # ربات
cloudflared tunnel --url http://localhost:8080 2>&1 &   # پنل
cloudflared tunnel --url http://localhost:2083 2>&1 &   # Xray inbound

# 5. آدرس‌های جدید رو از لاگ بگیر

# 6. Webhook تلگرام
curl -s "https://api.telegram.org/botTOKEN/deleteWebhook"
curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://NEW_BOT_TUNNEL/index.php"

# 7. config.php ($domainhosts آپدیت شود)
# 8. Cron jobs (bash /var/www/mirza_pro/setup_cron.sh)
# 9. Hosts پنل (SQLite → hosts table)
```

## نکته حیاتی
MariaDB بعد از ریستارت خودکار استارت نمیشه — اولین قدم همیشه `service mariadb start` باشد!

## ابزار مفید
```bash
# بررسی وضعیت همه سرویس‌ها
ss -tlnp | grep -E "80|8080|2083|3306"

# بررسی cloudflared
ps aux | grep cloudflared | grep -v grep

# بررسی webhook
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo"
```
