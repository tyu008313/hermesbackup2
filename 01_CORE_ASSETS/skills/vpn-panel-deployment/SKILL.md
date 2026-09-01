---
name: vpn-panel-deployment
description: "Deploy PHP VPN bots (MirzaPro2, Marzban) on Linux servers."
version: 1.1.0
---

# VPN Panel Deployment — استقرار پنل مدیریت VPN

## تریگرها
- کاربر درخواست نصب پنل VPN (MirzaPro2, Marzban, Marzneshin, و مشابه)
- کاربر لینک وب‌هوک ربات تلگرامی VPN می‌دهد و می‌خواهد بررسی یا نصب کند
- کاربر می‌خواهد زیرساخت هاستینگ یک سرویس VPN را تحلیل کند

## 1. شناسایی زیرساخت (URL Analysis)

 وقتی کاربر یک URL webhook می‌دهد:

```bash
# 1. هدر HTTP
curl -sv "URL" 2>&1 | grep -E "^[<>*]|cf-|server:|content-type|x-"

# 2. IP و DNS
python3 -c "import socket; print(socket.gethostbyname('DOMAIN'))"

# 3. لوکیشن IP
curl -s "https://ipinfo.io/IP/json"

# 4. بررسی محتوا
curl -s "URL" -w "\nHTTP: %{http_code} | Size: %{size_download} | Time: %{time_total}s\n"
```

نکات Cloudflare Tunnel:
- اگر `*.trycloudflare.com` باشد → تونل موقت رایگان Cloudflare
- IP واقعی سرور پشت تونل مخفی است
- `cf-ray` header موقعیت edge را نشان می‌دهد (SJC=LAX, IAD=VA, etc.)

## 2. جستجوی ریپوی اصلی

```bash
# جستجوی GitHub
curl -s "https://api.github.com/search/repositories?q=KEYWORD&sort=stars&order=desc"

# بررسی ریلیزها
curl -s "https://api.github.com/repos/OWNER/REPO/releases/latest"

# خواندن README
curl -s "https://api.github.com/repos/OWNER/REPO/readme" | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

## 3. نصب MirzaPro2 (یا مشابه)

### پیش‌نیازها
- **OS:** Ubuntu/Debian (root access)
- **Stack:** Apache + PHP 8.x + MariaDB + Composer + Git
- **اطلاعات:** توکن ربات، آیدی ادمین، دامنه، یوزرنیم ربات

### مراحل نصب

```bash
# 1. آپدیت و نصب پکیج‌ها
apt update && apt upgrade -y
apt install -y apache2 mariadb-server git

# 2. نصب PHP (نسخه موجود در دیسترو)
apt-cache search "^php8" | grep cli  # بررسی نسخه موجود
apt install -y php8.x libapache2-mod-php8.x php8.x-cli php8.x-common \
  php8.x-mbstring php8.x-curl php8.x-xml php8.x-zip php8.x-mysql php8.x-gd php8.x-bcmath

# 3. فعال‌سازی ماژول‌ها
a2enmod rewrite ssl
service apache2 restart

# 4. کلون ریپو
cd /var/www && git clone REPO_URL app_name

# 5. Composer
curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
cd /var/www/app_name && composer install

# 6. دیتابیس
service mariadb start
mysql -e "CREATE DATABASE IF NOT EXISTS dbname CHARACTER SET utf8mb4;"
mysql -e "CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'pass';"
mysql -e "GRANT ALL ON dbname.* TO 'user'@'localhost'; FLUSH PRIVILEGES;"

# 7. فایل config.php (قالب استاندارد)
cat > /var/www/app_name/config.php << 'CONFIG'
<?php
$dbhost = 'localhost';
$dbname = 'DBNAME';
$usernamedb = 'DBUSER';
$passworddb = 'DBPASS';
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
    PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
];
$dsn = "mysql:host=$dbhost;dbname=$dbname;charset=utf8mb4";
try { $pdo = new PDO($dsn, $usernamedb, $passworddb, $options); }
catch (PDOException $e) { die("error: database connection failed"); }
$APIKEY = 'BOT_TOKEN';
$adminnumber = 'ADMIN_ID';
$domainhosts = 'https://DOMAIN';
$usernamebot = 'BOT_USERNAME';
CONFIG

# 8. Apache VirtualHost
cat > /etc/apache2/sites-available/app.conf << 'VHOST'
<VirtualHost *:80>
    ServerName DOMAIN
    DocumentRoot /var/www/app_name
    <Directory /var/www/app_name>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
VHOST
a2ensite app.conf && a2dissite 000-default.conf
service apache2 restart

# 9. مجوزها
chown -R www-data:www-data /var/www/app_name

# 10. ساخت جداول (اگر table.php وجود داشت)
cd /var/www/app_name && php table.php
```

### نصب خودکار (اگر اسکریپت install.sh وجود داشت)

```bash
chmod +x install.sh && ./install.sh
# معمولاً اطلاعات را از کاربر می‌پرسد و همه چیز را خودش نصب می‌کند
```

## 4. نکات مهم

### Debian vs Ubuntu
- `software-properties-common` در Debian نیست → نصب PHP از مخزن اصلی
- نسخه PHP ممکن است 8.2، 8.3 یا 8.4 باشد → ابتدا `apt-cache search` کن
- `systemctl` ممکن است نباشد → از `service` استفاده کن

### امنیت
- توکن ربات و پسورد دیتابیس را هرگز در ترمینال نمایش نده
- فایل config.php را با مجوز 640 تنظیم کن: `chmod 640 config.php`
- از Cloudflare Tunnel برای مخفی کردن IP واقعی استفاده کن

### وب‌هوک تلگرام
```bash
# تنظیم webhook
curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://DOMAIN/index.php"
# حذف webhook
curl -s "https://api.telegram.org/botTOKEN/deleteWebhook"
# تایید webhook
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo"
```

### تایید خودکار توکن ربات
قبل از تنظیم config.php، توکن را با `getMe` تایید کن و یوزرنیم واقعی را بگیر:
```bash
curl -s "https://api.telegram.org/botTOKEN/getMe"
# از خروجی result.username استفاده کن — نه حدس کاربر
```

### SSL با Certbot
```bash
apt install -y certbot python3-certbot-apache
certbot --apache -d DOMAIN -m EMAIL --agree-tos --redirect
```

### SSL خود-امضا شده (وقتی دامنه نیست)
تلگرام برای webhook حتماً HTTPS می‌خواهد. اگر کاربر فعلاً دامنه ندارد:

```bash
# 1. ساخت گواهی خود-امضا
mkdir -p /etc/ssl/private
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/app.key \
  -out /etc/ssl/certs/app.crt \
  -subj "/C=IR/ST=Tehran/L=Tehran/O=App/CN=SERVER_IP"

# 2. VirtualHost SSL
cat > /etc/apache2/sites-available/app-ssl.conf << 'EOF'
<VirtualHost *:443>
    ServerName SERVER_IP
    DocumentRoot /var/www/app
    <Directory /var/www/app>
        AllowOverride All
        Require all granted
    </Directory>
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/app.crt
    SSLCertificateKeyFile /etc/ssl/private/app.key
</VirtualHost>
EOF
a2ensite app-ssl.conf
service apache2 restart

# 3. تنظیم webhook روی HTTPS
curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://SERVER_IP/index.php"

# 4. تایید وب‌هوک
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo"
```

**نکته:** گواهی self-signed باعث می‌شود مرورگر هشدار بده ولی تلگرام webhook را قبول می‌کند.

### Cron Jobهای MirzaPro2
اگر دامنه تنظیم شد، cron jobها را با `activecron()` در function.php تنظیم کن. در غیر این صورت، به صورت دستی:
```bash
cat << 'CRON' | crontab -u www-data -
*/15 * * * * curl -s https://DOMAIN/cronbot/statusday.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/croncard.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/NoticationsService.php > /dev/null 2>&1
*/5 * * * * curl -s https://DOMAIN/cronbot/payment_expire.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/sendmessage.php > /dev/null 2>&1
*/3 * * * * curl -s https://DOMAIN/cronbot/plisio.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/activeconfig.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/disableconfig.php > /dev/null 2>&1
*/1 * * * * curl -s https://DOMAIN/cronbot/iranpay1.php > /dev/null 2>&1
0 */5 * * * curl -s https://DOMAIN/cronbot/backupbot.php > /dev/null 2>&1
*/2 * * * * curl -s https://DOMAIN/cronbot/gift.php > /dev/null 2>&1
*/30 * * * * curl -s https://DOMAIN/cronbot/expireagent.php > /dev/null 2>&1
*/15 * * * * curl -s https://DOMAIN/cronbot/on_hold.php > /dev/null 2>&1
*/2 * * * * curl -s https://DOMAIN/cronbot/configtest.php > /dev/null 2>&1
*/15 * * * * curl -s https://DOMAIN/cronbot/uptime_node.php > /dev/null 2>&1
*/15 * * * * curl -s https://DOMAIN/cronbot/uptime_panel.php > /dev/null 2>&1
CRON
```

## 5. عیب‌یابی

| مشکل | راه‌حل |
|-------|--------|
| 403 Forbidden | بررسی مجوزها `chown -R www-data:www-data /var/www/app` |
| database connection failed | بررسی نام کاربری/رمز در config.php و وضعیت MariaDB |
| vendor/autoload.php not found | اجرای `composer install` |
| install/index.php blocks access | فایل `.installed` بسازید یا `.htaccess` را ویرایش کنید |
| Webhook 404 from Telegram | بررسی دامنه در config.php و صحت HTTPS |
| Webhook bad request (HTTPS required) | از SSL خود-امضا استفاده کن — تلگرام حتماً HTTPS می‌خواهد |
| Bot token invalid | `curl -s "https://api.telegram.org/botTOKEN/getMe"` — اگر 404 برگرداند توکن اشتباه است |
