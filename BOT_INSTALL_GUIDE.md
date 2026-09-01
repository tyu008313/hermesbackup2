# 🤖 راهنمای نصب کامل ربات MirzaPro2 روی سرور جدید

سلام رفیق جان! 👋❤️
تو داری جای رضا (@RG7YT) کار میکنی. همیشه فارسی جواب بده، گرم و صمیمی باش 😎
از رضا بخواه اطلاعات زیر رو بهت بده قبل شروع:
- توکن ربات تلگرام (از @BotFather)
- آیدی عددی ادمین (آیدی عددی تلگرامش)

---

## مرحله ۱: آپدیت سیستم

```bash
apt update && apt upgrade -y
```

## مرحله ۲: نصب سرویس‌ها

```bash
apt install -y apache2 mariadb-server git software-properties-common curl cron
apt install -y php8.4 libapache2-mod-php8.4 php8.4-cli php8.4-common \
  php8.4-mbstring php8.4-curl php8.4-xml php8.4-zip php8.4-mysql \
  php8.4-gd php8.4-bcmath
a2enmod rewrite ssl
service apache2 restart
```

## مرحله ۳: نصب Composer

```bash
cd /tmp
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
rm composer-setup.php
```

## مرحله ۴: نصب MariaDB و ساخت دیتابیس

```bash
service mariadb start
mysql -e "
CREATE DATABASE mirza_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mirza_user'@'localhost' IDENTIFIED BY 'Mirza@2026!Secure';
GRANT ALL PRIVILEGES ON mirza_pro.* TO 'mirza_user'@'localhost';
FLUSH PRIVILEGES;
SELECT '✅ Database created!' AS Status;
"
```

## مرحله ۵: کلون و نصب ربات

```bash
cd /var/www
git clone https://github.com/mahdiMGF2/mirza_pro.git
cd /var/www/mirza_pro
composer install
```

## مرحله ۶: ساخت فایل config.php

⚠️ مقادیر `TOKEN` و `ADMIN_ID` و `TUNNEL_URL` رو از رضا بگیر و جایگزین کن:

```php
<?php
$dbhost = 'localhost';
$dbname = 'mirza_pro';
$usernamedb = 'mirza_user';
$passworddb = 'Mirza@2026!Secure';

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
    PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
];

$dsn = "mysql:host=$dbhost;dbname=$dbname;charset=utf8mb4";
try {
    $pdo = new PDO($dsn, $usernamedb, $passworddb, $options);
} catch (PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    die("error: database connection failed");
}

$APIKEY = 'TOKEN';
$adminnumber = 'ADMIN_ID';
$domainhosts = 'TUNNEL_URL';
$usernamebot = 'نام ربات بدون @';
?>
```

## مرحله ۷: ساخت جداول دیتابیس

```bash
cd /var/www/mirza_pro
php table.php
```

## مرحله ۸: فیکس‌های حیاتی

### ۸.۱ فیکس IP Check (برای Cloudflare Tunnel)

توی فایل `/var/www/mirza_pro/function.php` تابع `checktelegramip()` رو پیدا کن (حدود خط 1593) و این خطوط رو **قبلش** اضافه کن:

```php
function checktelegramip()
{
    $clientIp = $_SERVER['REMOTE_ADDR'] ?? '';
    if ($clientIp === '127.0.0.1' || $clientIp === '::1' || $clientIp === '::ffff:127.0.0.1') {
        return true;
    }
    // بقیه کد قبلی تابع اینجا بمونه
```

### ۸.۲ فیکس آیدی ادمین توی دیتابیس

```bash
mysql -e "USE mirza_pro; UPDATE admin SET id_admin = 'ADMIN_ID' WHERE id_admin = 'YOUR_TELEGRAM_ID_HERE';"
```

### ۸.۳ فیکس وضعیت کاربر ادمین

```bash
mysql -e "USE mirza_pro; UPDATE user SET roll_Status = 1, joinchannel = 'active' WHERE id = 'ADMIN_ID';"
```

## مرحله ۹: تنظیم مالکیت و مجوزها

```bash
chown -R www-data:www-data /var/www/mirza_pro
chmod -R 755 /var/www/mirza_pro
```

## مرحله ۱۰: تنظیم Apache VirtualHost

```bash
cat > /etc/apache2/sites-available/mirza-pro.conf << 'EOF'
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /var/www/mirza_pro
    <Directory /var/www/mirza_pro>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF
a2ensite mirza-pro.conf
a2dissite 000-default.conf 2>/dev/null
service apache2 restart
```

## مرحله ۱۱: نصب cloudflared

```bash
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
cloudflared --version
```

## مرحله ۱۲: راه‌اندازی Cloudflare Tunnel و دریافت آدرس

```bash
cloudflared tunnel --url http://localhost:80 2>&1 | tee /tmp/tunnel.log &
sleep 10
grep -oP 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' /tmp/tunnel.log
```

⚠️ آدرسی که از لاگ اومد رو یادداشت کن — `TUNNEL_URL` جدید

## مرحله ۱۳: آپدیت config.php با آدرس تونل جدید

```bash
sed -i "s|TUNNEL_URL|TUNNEL_URL_جدید|g" /var/www/mirza_pro/config.php
```

## مرحله ۱۴: تنظیم Webhook تلگرام

```bash
curl -s "https://api.telegram.org/botTOKEN/deleteWebhook"
curl -s "https://api.telegram.org/botTOKEN/setWebhook?url=https://TUNNEL_URL_جدید/index.php"
```

## مرحله ۱۵: تنظیم Cron Jobs

```bash
TUNNEL="https://TUNNEL_URL_جدید"

cat << EOF | crontab -u www-data -
# MirzaPro2 Cron Jobs
*/15 * * * * curl -s \$TUNNEL/cronbot/statusday.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/croncard.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/NoticationsService.php > /dev/null 2>&1
*/5 * * * * curl -s \$TUNNEL/cronbot/payment_expire.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/sendmessage.php > /dev/null 2>&1
*/3 * * * * curl -s \$TUNNEL/cronbot/plisio.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/activeconfig.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/disableconfig.php > /dev/null 2>&1
*/1 * * * * curl -s \$TUNNEL/cronbot/iranpay1.php > /dev/null 2>&1
0 */5 * * * curl -s \$TUNNEL/cronbot/backupbot.php > /dev/null 2>&1
*/2 * * * * curl -s \$TUNNEL/cronbot/gift.php > /dev/null 2>&1
*/30 * * * * curl -s \$TUNNEL/cronbot/expireagent.php > /dev/null 2>&1
*/15 * * * * curl -s \$TUNNEL/cronbot/on_hold.php > /dev/null 2>&1
*/2 * * * * curl -s \$TUNNEL/cronbot/configtest.php > /dev/null 2>&1
*/15 * * * * curl -s \$TUNNEL/cronbot/uptime_node.php > /dev/null 2>&1
*/15 * * * * curl -s \$TUNNEL/cronbot/uptime_panel.php > /dev/null 2>&1
EOF

service cron start
```

## مرحله ۱۶: بررسی نهایی و تست

```bash
echo "=== بررسی سرویس‌ها ==="
service apache2 status 2>&1 | head -3
service mariadb status 2>&1 | head -3
service cron status 2>&1 | head -3

echo "=== بررسی پورت‌ها ==="
ss -tlnp | grep -E "80|443"

echo "=== تست وب‌هوک ==="
curl -s "https://api.telegram.org/botTOKEN/getWebhookInfo" | grep -oP '"url":"[^"]*"'

echo "=== تست دیتابیس ==="
mysql -u mirza_user -p'Mirza@2026!Secure' mirza_pro -e "SELECT COUNT(*) as users FROM user;"

echo "✅ نصب تمام شد! به رضا بگو ربات رو تست کنه!"
```

---

## ⚠️ نکات مهم برای همسر بعدی

1. **systemctl کار نمیکنه** — همیشه `service` بزن
2. **Quick Tunnel موقتیه** — بعد از ریستارت آدرسش عوض میشه
3. **MariaDB خودکار استارت نمیشه** — باید دستی استارت کنی
4. **از رضا بخواه توکن و آیدی بده** — بدون اونها کار نمیکنه
5. **بعد از نصب تست کن** — یه پیام /start به ربات بفرست
6. **فقط فارسی جواب بده** و ایموجی زیاد بزن 😎🔥

## 🔄 فلوچارت ریستارت (وقتی Railway ریستارت کرد)

```
service mariadb start
service apache2 start
service cron start
cd /var/www/mirza_pro && (apachectl start)
cloudflared tunnel --url http://localhost:80 2>&1 &
sleep 10
# آدرس جدید از لاگ بگیر
# config.php آپدیت کن
# webhook آپدیت کن
# cron jobs آپدیت کن
```
