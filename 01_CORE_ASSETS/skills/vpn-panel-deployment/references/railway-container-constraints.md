# Railway Container Deployment — محدودیت‌ها و راه‌حل‌ها

## محدودیت‌های کلیدی Railway

### 1. systemd موجود نیست
```bash
# ❌ این کار نمی‌کند
systemctl start apache2
systemctl enable x-ui

# ✅ این کار می‌کند
service apache2 start
cd /usr/local/x-ui && ./x-ui &
```

### 2. فقط یک سرویس اصلی دارد
- Railway یک `PORT` env var تعیین می‌کند (مثلاً 8080)
- Railway Public Domain فقط به این پورت route می‌کند
- سرویس‌های دیگر (مثل 3x-ui) از طریق Public Domain قابل دسترسی نیستند

### 3. راه‌حل: Cloudflare Quick Tunnel
هر سرویس جداگانه نیاز به tunnel جداگانه دارد:

```bash
# سرویس 1: ربات تلگرام (Apache پورت 80)
cloudflared tunnel --url http://localhost:80 &

# سرویس 2: پنل VPN (x-ui پورت 8080)
cloudflared tunnel --url http://localhost:8080 &
```

**نکته مهم:** Quick Tunnel موقتی است. بعد از هر restart:
1. URL جدید از لاگ cloudflared بگیر
2. Webhook تلگرام را آپدیت کن
3. Cron job ها را آپدیت کن
4. config.php را آپدیت کن

### 4. شناسایی Environment Variables
```bash
echo "PORT: $PORT"
echo "RAILWAY_PUBLIC_DOMAIN: $RAILWAY_PUBLIC_DOMAIN"
echo "RAILWAY_STATIC_URL: $RAILWAY_STATIC_URL"
echo "RAILWAY_PROJECT_NAME: $RAILWAY_PROJECT_NAME"
```

## الگوی استقرار MirzaPro2 + 3x-ui روی Railway

```
Railway Container
├── Apache (port 80) ──→ Cloudflare Tunnel 1 ──→ ربات تلگرام
├── x-ui (port 8080) ─→ Cloudflare Tunnel 2 ──→ پنل VPN
├── MariaDB (localhost:3306)
└── Hermes Agent (سرویس اصلی)
```

## عیب‌یابی Railway

| مشکل | دلیل | راه‌حل |
|-------|------|--------|
| 502 Application failed | پورت اشتباه یا service خاموش | بررسی `ss -tlnp` و restart service |
| systemctl exit 127 | systemd نیست | از `service` یا `./binary &` استفاده کن |
| Cloudflare tunnel error 1033 | cloudflared خاموش شده | دوباره اجرا کن |
| URL تونل عوض شد | Quick Tunnel موقتی است | webhook و cron را آپدیت کن |
