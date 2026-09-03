# Auto-Monitor & Restart Pattern — اسکریپت‌های خودکار

## overview
دو اسکریپت ایجاد کن که بعد از هر restart Railway خودکار ربات رو بالا بیاره و وضعیتش رو مانیتور کنه.

## restart.sh — ریستارت خودکار

این اسکریپت رو بعد از هر restart Railway اجرا کن:

```bash
#!/bin/bash
BOT_TOKEN="TOKEN_HERE"

service mariadb start 2>/dev/null
service apache2 start 2>/dev/null
service cron start 2>/dev/null

pkill -9 cloudflared 2>/dev/null
sleep 2

cloudflared tunnel --url http://localhost:80 > /tmp/tunnel_bot.log 2>&1 &
sleep 15

TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' /tmp/tunnel_bot.log | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ خطا: آدرس تونل پیدا نشد!"
    exit 1
fi

# آپدیت config.php
sed -i "s|https://[^'\"]*trycloudflare\.com|$TUNNEL_URL|g" /var/www/APP_DIR/config.php

# آپدیت webhook
curl -s "https://api.telegram.org/bot$BOT_TOKEN/deleteWebhook" > /dev/null
curl -s "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$TUNNEL_URL/index" > /dev/null

# آپدیت cron jobs
cat << EOF | crontab -u www-data -
*/15 * * * * curl -s $TUNNEL_URL/cronbot/statusday.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/croncard.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/NoticationsService.php > /dev/null 2>&1
*/5 * * * * curl -s $TUNNEL_URL/cronbot/payment_expire.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/sendmessage.php > /dev/null 2>&1
*/3 * * * * curl -s $TUNNEL_URL/cronbot/plisio.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/activeconfig.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/disableconfig.php > /dev/null 2>&1
*/1 * * * * curl -s $TUNNEL_URL/cronbot/iranpay1.php > /dev/null 2>&1
0 */5 * * * curl -s $TUNNEL_URL/cronbot/backupbot.php > /dev/null 2>&1
*/2 * * * * curl -s $TUNNEL_URL/cronbot/gift.php > /dev/null 2>&1
*/30 * * * * curl -s $TUNNEL_URL/cronbot/expireagent.php > /dev/null 2>&1
*/15 * * * * curl -s $TUNNEL_URL/cronbot/on_hold.php > /dev/null 2>&1
*/2 * * * * curl -s $TUNNEL_URL/cronbot/configtest.php > /dev/null 2>&1
*/15 * * * * curl -s $TUNNEL_URL/cronbot/uptime_node.php > /dev/null 2>&1
*/15 * * * * curl -s $TUNNEL_URL/cronbot/uptime_panel.php > /dev/null 2>&1
EOF

echo "✅ آدرس جدید: $TUNNEL_URL"
```

**نکته webhook:** برای MirzaBot Pro از URL بدون `.php` استفاده کن (چون `.htaccess` پسوند `.php` رو strip میکنه):
```bash
# ❌ اشتباه
curl -s ".../setWebhook?url=https://domain/index.php"
# ✅ درست
curl -s ".../setWebhook?url=https://domain/index"
```

## monitor.sh — مانیتورینگ خودکار

هر ۵ دقیقه چک کنه و اگه مشکلی بود ریستارت کنه:

```bash
#!/bin/bash
BOT_TOKEN="TOKEN_HERE"
LOG_FILE="/var/www/APP_DIR/monitor.log"
RESTART_SCRIPT="/var/www/APP_DIR/restart.sh"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

check_bot() {
    # چک Apache
    pgrep -x "apache2" > /dev/null || { log "❌ Apache خاموش"; return 1; }
    # چک MariaDB
    pgrep -x "mariadbd" > /dev/null || { log "❌ MariaDB خاموش"; return 1; }
    # چک پورت 80
    ss -tlnp | grep -q ":80 " || { log "❌ پورت 80 بسته"; return 1; }
    # چک webhook
    local pending=$(curl -s "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo" 2>/dev/null | grep -oP '"pending_update_count":\K[0-9]+')
    [ -z "$pending" ] || [ "$pending" -gt 5 ] && { log "❌ webhook خطا"; return 1; }
    # چک cloudflared
    pgrep -x "cloudflared" > /dev/null || { log "❌ cloudflared خاموش"; return 1; }
    # تست درخواست
    [ "$(curl -s http://localhost:80/ -w '%{http_code}' -o /dev/null 2>/dev/null)" != "200" ] && { log "❌ ربات پاسخ نمیده"; return 1; }
    
    log "✅ ربات سالمه"
    return 0
}

log "🔍 شروع بررسی..."
if ! check_bot; then
    log "⚠️ ریستارت خودکار..."
    bash "$RESTART_SCRIPT" >> "$LOG_FILE" 2>&1
fi
```

## cron job مانیتورینگ

```bash
(crontab -l 2>/dev/null; echo "*/5 * * * * /var/www/APP_DIR/monitor.sh") | crontab -
```

## نکات مهم

- `monitor.sh` باید `chmod +x` باشه
- `restart.sh` باید `chmod +x` باشه
- هر دو فایل باید در GitHub backup هم باشن
- MirzaBot Pro webhook بدون `.php` (چون .htaccess rewrite داره)
- `sed -i` برای آپدیت config.php از regex استفاده میکنه — مراقب باش URL قبلی کامل پاک بشه
