#!/bin/bash
# ============================================
# 🔧 اسکریپت خودکار راه‌اندازی مجدد ربات (MirzaBot Pro)
# ============================================

BOT_TOKEN="8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ"

echo "🔄 شروع راه‌اندازی مجدد..."

# ۱. استارت MariaDB
echo "📦 استارت MariaDB..."
service mariadb start 2>/dev/null || echo "⚠️ MariaDB خطا"

# ۲. استارت Apache
echo "🌐 استارت Apache..."
service apache2 start 2>/dev/null || echo "⚠️ Apache خطا"

# ۳. استارت Cron
echo "⏰ استارت Cron..."
service cron start 2>/dev/null || echo "⚠️ Cron خطا"

# ۴. Kill تونل‌های قبلی
echo "🧹 پاکسازی تونل‌های قبلی..."
pkill -9 cloudflared 2>/dev/null
sleep 2

# ۵. راه‌اندازی تونل جدید
echo "☁️ راه‌اندازی Cloudflare Tunnel..."
cloudflared tunnel --url http://localhost:80 > /tmp/tunnel_bot.log 2>&1 &
sleep 15

# ۶. دریافت آدرس جدید
TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' /tmp/tunnel_bot.log | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ خطا: آدرس تونل پیدا نشد!"
    echo "لاگ تونل:"
    cat /tmp/tunnel_bot.log
    exit 1
fi

echo "✅ آدرس جدید تونل: $TUNNEL_URL"

# ۷. آپدیت config.php
echo "⚙️ آپدیت config.php..."
sed -i "s|https://[^'\"]*trycloudflare\.com|$TUNNEL_URL|g" /var/www/mirza_bot/config.php

# ۸. آپدیت Webhook تلگرام
echo "🤖 آپدیت Webhook..."
curl -s "https://api.telegram.org/bot$BOT_TOKEN/deleteWebhook" > /dev/null
curl -s "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$TUNNEL_URL/index.php" > /dev/null

# ۹. آپدیت Cron Jobs
echo "⏰ آپدیت Cron Jobs..."
cat << EOF | crontab -u www-data -
# MirzaBot Pro Cron Jobs
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

# ۱۰. بررسی نهایی
echo ""
echo "=========================================="
echo "✅ راه‌اندازی مجدد با موفقیت انجام شد!"
echo "=========================================="
echo ""
echo "🔗 آدرس ربات: $TUNNEL_URL"
echo "🤖 آدرس webhook: $TUNNEL_URL/index.php"
echo ""
echo "📊 وضعیت سرویس‌ها:"
echo "  MariaDB: $(service mariadb status 2>&1 | grep -o 'running\|stopped' | head -1)"
echo "  Apache:  $(service apache2 status 2>&1 | grep -o 'running\|stopped' | head -1)"
echo "  Cron:    $(service cron status 2>&1 | grep -o 'running\|stopped' | head -1)"
echo ""
echo "⚠️ آدرس تونل رو به رضا بده: $TUNNEL_URL"
echo "=========================================="
