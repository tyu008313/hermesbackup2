# Railway + Cloudflare Quick Tunnel Pattern

## مشکل اصلی
Quick Tunnel URL هر بار ریستارت **عوض میشه**! باید webhook + config.php + cron jobs همه آپدیت بشن.

## restart.sh اتوماتیک
یه اسکریپت `restart.sh` بساز که:
1. MariaDB + Apache + Cron رو استارت کنه
2. تونل قبلی رو kill کنه
3. تونل جدید بسازه و URL جدید رو بگیره
4. config.php رو آپدیت کنه (sed با regex)
5. webhook تلگرام رو آپدیت کنه
6. cron jobs رو با URL جدید آپدیت کنه

```bash
#!/bin/bash
BOT_TOKEN="TOKEN_HERE"
service mariadb start
service apache2 start
service cron start
pkill -9 cloudflared
sleep 2
cloudflared tunnel --url http://localhost:80 > /tmp/tunnel.log 2>&1 &
sleep 15
TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' /tmp/tunnel.log | head -1)
sed -i "s|https://[^'\"]*trycloudflare\.com|$TUNNEL_URL|g" config.php
curl -s "https://api.telegram.org/bot$BOT_TOKEN/deleteWebhook" > /dev/null
curl -s "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$TUNNEL_URL/index.php" > /dev/null
# cron jobs update with new URL...
```

## monitor.sh (چک خودکار)
هر ۵ دقیقه via cron اجرا بشه:
- Apache, MariaDB, cloudflared چک کنه
- اگه چیزی خاموش بود، restart.sh اجرا کنه
- لاگ بنویسه

## Railway Constraints
- `systemctl` نیست → همیشه `service` بزن
- `dig`/`nslookup`/`ss` ممکنه نباشن → از python3/netstat استفاده کن
- MariaDB خودکار استارت نمیشه → باید دستی start کنی
- فقط پورت‌های PORT env و 443 قابل دسترسی‌اند

## اطلاعات مورد نیاز (قبل از نصب!)
حتماً از کاربر بگیر:
- توکن ربات تلگرام (از @BotFather)
- آیدی عددی ادمین (از @userinfobot)
- نام ربات (بدون @)
