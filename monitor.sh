#!/bin/bash
# ============================================
# 🔍 اسکریپت مانیتورینگ خودکار ربات
# هر ۵ دقیقه چک میکنه اگه ربات قطع شده باشه، خودکار ریستارت میکنه
# ============================================

BOT_TOKEN="8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ"
LOG_FILE="/var/www/mirza_pro/monitor.log"
RESTART_SCRIPT="/var/www/mirza_pro/restart.sh"

# تابع لاگ
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# تابع بررسی ربات
check_bot() {
    # ۱. بررسی Apache
    if ! pgrep -x "apache2" > /dev/null; then
        log "❌ Apache خاموش شده!"
        return 1
    fi
    
    # ۲. بررسی MariaDB
    if ! pgrep -x "mariadbd" > /dev/null; then
        log "❌ MariaDB خاموش شده!"
        return 1
    fi
    
    # ۳. بررسی پورت ۸۰
    if ! ss -tlnp | grep -q ":80 "; then
        log "❌ پورت ۸۰ بسته شده!"
        return 1
    fi
    
    # ۴. بررسی webhook
    local webhook_status=$(curl -s "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo" 2>/dev/null)
    local pending=$(echo "$webhook_status" | grep -oP '"pending_update_count":\K[0-9]+')
    local last_error=$(echo "$webhook_status" | grep -oP '"last_error_message":"[^"]*"')
    
    if [ -z "$pending" ]; then
        log "❌ webhook چک نشد!"
        return 1
    fi
    
    if [ "$pending" -gt 5 ]; then
        log "⚠️ pending updates: $pending (بیش از حد)"
        return 1
    fi
    
    if [ -n "$last_error" ] && [ "$last_error" != '"last_error_message":""' ]; then
        log "⚠️ آخرین خطا: $last_error"
        return 1
    fi
    
    # ۵. بررسی cloudflared
    if ! pgrep -x "cloudflared" > /dev/null; then
        log "❌ cloudflared خاموش شده!"
        return 1
    fi
    
    # ۶. تست درخواست به ربات
    local test_response=$(curl -s "http://localhost:80/" -w "%{http_code}" -o /dev/null 2>/dev/null)
    if [ "$test_response" != "200" ]; then
        log "❌ ربات پاسخ نمیده! HTTP: $test_response"
        return 1
    fi
    
    log "✅ ربات سالمه"
    return 0
}

# تابع ریستارت
restart_bot() {
    log "🔄 شروع ریستارت خودکار..."
    bash "$RESTART_SCRIPT" >> "$LOG_FILE" 2>&1
    log "✅ ریستارت انجام شد"
}

# اجرای اصلی
log "🔍 شروع بررسی..."

if ! check_bot; then
    log "⚠️ ربات مشکل داره! ریستارت میکنم..."
    restart_bot
else
    log "✅ ربات سالمه - نیازی به ریستارت نیست"
fi
