# Cloudflare Quick Tunnel — راه‌حل اصلی برای Telegram Webhook بدون دامنه

## وقتی استفاده کنیم
- کاربر دامنه ندارد
- `getWebhookInfo` خطای `Connection timed out` برمی‌گرداند
- پورت 443 توسط Cloud Security Group بسته شده

## مراحل

### 1. نصب cloudflared
```bash
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
```

### 2. اجرای تونل
```bash
cloudflared tunnel --url http://localhost:80 2>&1 &
# خروجی: https://something-words.trycloudflare.com
```

**نکته:** URL در لاگ ظاهر می‌شود. منتظر بمان تا ببینی.

### 3. تنظیم config.php
```php
$domainhosts = 'https://TUNNEL_URL';
```

### 4. تنظیم webhook
```bash
curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://TUNNEL_URL/index.php"
```

### 5. تایید
```bash
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo"
# باید ok:true و pending_update_count:0 باشد
```

## مقایسه با Self-Signed SSL

| ویژگی | Cloudflare Tunnel | Self-Signed SSL |
|-------|-------------------|-----------------|
| نیاز به دامنه | ❌ نه | ❌ نه |
| HTTPS معتبر | ✅ بله | ❌ خیر |
| مخفی کردن IP | ✅ بله | ❌ خیر |
| مشکل firewall | ✅ حل می‌کند | ❌ ممکنه حل نکنه |
| پایداری | ⚠️ موقتی | ✅ دائمی |
| نیاز به تنظیمات | ✅ کم | ⚠️ متوسط |

## عیب‌یابی

### `Connection timed out` در getWebhookInfo
- Cloud Security Group پورت 443 را بسته
- **راه‌حل:** Cloudflare Tunnel (نه self-signed SSL!)

### URL تونل عوض شد
- Quick Tunnel موقتی است و URL هر بار تغییر می‌کند
- **راه‌حل:** بعد از هر بار ریستارت، webhook را دوباره تنظیم کن
- یا از دامنه اختصاصی استفاده کن

### `webhook: true` ولی پیام نمی‌رسد
- بررسی کن که `checktelegramip()` در function.php IP تلگرام را قبول کند
- تونل از IP Cloudflare edge استفاده می‌کند (نه IP تلگرام)
- **راه‌حل:** بررسی کن که تونل ترافیک را صحیح مسیریابی می‌کند
