# MirzaPro2 — اطلاعات تکمیلی

## ریپوی اصلی
- **GitHub:** github.com/mahdiMGF2/mirza_pro (ممکن است خصوصی باشد)
- **Auto Installer:** github.com/iaghapour/MirzaPro2-Auto-Installer (58 stars)
- **کانال تلگرام:** @mirzapanel
- **گروه تلگرام:** @mirzapanelgroup

## ساختار فایل‌ها
```
/var/www/mirza_pro/
├── index.php          ← Webhook اصلی تلگرام (370KB!)
├── config.php         ← تنظیمات دیتابیس + ربات
├── table.php          ← ساخت جداول (نیاز به bootstrap.php)
├── admin.php          ← پنل ادمین وب (589KB)
├── function.php       ← توابع اصلی (91KB)
├── botapi.php         ← API ربات تلگرام
├── keyboard.php       ← کیبوردهای تلگرام
├── panels.php         ← مدیریت پنل‌ها (116KB)
├── composer.json      ← وابستگی‌ها (endroid/qr-code, phpoffice/phpspreadsheet)
├── db/                ← Schema, tables, migrations
├── vpnbot/            ← نسخه‌های مختلف ربات
├── install/           ← اسکریپت نصب وب (بعد از نصب حذف می‌شود)
└── vendor/            ← Composer packages
```

## پنل‌های پشتیبانی شده
- Marzban, Marzneshin
- Sanaei / Alireza, S-UI
- Hiddify
- WGDashboard (WireGuard)
- MikroTik
- IBSng, Pasarguard

## درگاه‌های پرداخت
- کارت به کارت (تایید دستی)
- NowPayments, Plisio, cubpay (ارز دیجیتال)
- زرین‌پال، آقای پرداخت، ایران‌پی (پرداخت آنلاین)

## نکات نصب MirzaPro2

### فایل install.sh
- اسکریپت نصب خودکار 123KB است
- شامل مراحل: نصب Apache, PHP, MySQL, SSL, Webhook, Cron
- پشتیبانی از نصب Non-Interactive (CLI mode)

### table.php
- نیاز به `vendor/autoload.php` (باید اول `composer install` اجرا شود)
- از `db/bootstrap.php` استفاده می‌کند
- Schema.php جداول را می‌سازد

### .htaccess اصلی
```apache
# اگر install/index.php وجود داشته باشد، دسترسی به صفحه اصلی را مسدود می‌کند
RewriteCond %{DOCUMENT_ROOT}/install/index.php -f
RewriteCond %{REQUEST_URI} !^/install/
RewriteRule ^ - [F,L]
```
**راه‌حل:** فایل `.installed` بسازید یا شرط را تغییر دهید

### نصب خودکار از ریپوی iaghapour
```bash
git clone https://github.com/iaghapour/MirzaPro2-Auto-Installer.git
cd MirzaPro2-Auto-Installer
chmod +x install_mirza.sh
sudo ./install_mirza.sh
# اطلاعات درخواست می‌شود: دامنه، ایمیل، دیتابیس، توکن، آیدی ادمین
```

## مشکل رایج: install.sh در Debian
- اسکریپت اصلی برای Ubuntu نوشته شده
- `software-properties-common` در Debian نیست
- `systemctl` ممکن است در контینر نباشد → از `service` استفاده کن
- PHP version متفاوت است → `apt-cache search` قبل از نصب
