---
name: php-webapp-deployment
description: Deploy PHP web apps on Linux with Apache, MariaDB, Composer.
tags: [php, apache, mariadb, composer, deployment, linux]
version: 1.1.0
---

# PHP Web Application Deployment

Deploy PHP web applications on Linux servers with full LAMP stack, Composer dependencies, SSL, and cron jobs.

## When to Use
- User asks to install a PHP web application on a server
- Setting up LAMP stack (Linux + Apache + MySQL/MariaDB + PHP)
- Deploying Telegram bot panels, CMS, or PHP-based web apps

## Prerequisites
- Root/sudo access on the server
- Domain name (optional, for SSL)

## Deployment Workflow

### Step 1: System Update and Package Installation
```bash
apt update && apt upgrade -y
```

**Debian vs Ubuntu differences:**
- `software-properties-common` may not exist on Debian — skip it
- Debian uses `mariadb-server` (not `mysql-server`)
- Check available PHP version: `apt-cache search "^php8" | grep cli`
- Debian 13 (trixie) ships PHP 8.4 natively

### Step 2: Install Stack
```bash
# Debian (no software-properties-common)
apt install -y apache2 mariadb-server git

# PHP (version may vary — check what's available)
apt install -y php8.4 libapache2-mod-php8.4 php8.4-cli php8.4-common \
  php8.4-mbstring php8.4-curl php8.4-xml php8.4-zip php8.4-mysql \
  php8.4-gd php8.4-bcmath

# Enable modules
a2enmod rewrite
a2enmod ssl
```

### Step 3: Install Composer
```bash
cd /tmp
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
```

### Step 4: Database Setup
```bash
service mariadb start
mysql -e "
  CREATE DATABASE IF NOT EXISTS app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD';
  GRANT ALL PRIVILEGES ON app_db.* TO 'app_user'@'localhost';
  FLUSH PRIVILEGES;
"
```

### Step 5: Deploy Application
```bash
cd /var/www
git clone https://github.com/OWNER/REPO.git app_name
chown -R www-data:www-data /var/www/app_name
cd /var/www/app_name
composer install
```

### Step 6: Configure Application
Edit `config.php` or `.env` with database credentials, API keys, domain.

### Step 7: Apache Virtual Host
```bash
cat > /etc/apache2/sites-available/app.conf << 'EOF'
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /var/www/app_name
    <Directory /var/www/app_name>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF
a2ensite app.conf
a2dissite 000-default.conf 2>/dev/null
service apache2 restart
```

### Step 8: Initialize Database Tables
```bash
cd /var/www/app_name
php table.php  # or equivalent migration script
mysql -e "USE app_db; SHOW TABLES;"  # verify
```

### Step 9: SSL with Certbot (if domain available)
```bash
apt install -y certbot python3-certbot-apache
certbot --apache -d yourdomain.com
```

### Step 9b: Self-Signed SSL (no domain — for Telegram webhooks)
Telegram requires HTTPS. Without a domain, use self-signed:
```bash
# Generate certificate
mkdir -p /etc/ssl/private
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/app.key \
  -out /etc/ssl/certs/app.crt \
  -subj "/C=IR/ST=Tehran/L=Tehran/O=App/CN=SERVER_IP"

# Apache SSL VirtualHost
cat > /etc/apache2/sites-available/app-ssl.conf << 'EOF'
<VirtualHost *:443>
    ServerName SERVER_IP
    DocumentRoot /var/www/app_name
    <Directory /var/www/app_name>
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
```

**Note:** Browsers will show a warning for self-signed certs, but Telegram accepts them for webhooks.

### Step 10: Cron Jobs
```bash
# Install cron if missing
apt install -y cron
service cron start

# Add jobs for www-data user
cat << 'CRON' | crontab -u www-data -
*/5 * * * * curl -s https://domain/cronjob1.php > /dev/null 2>&1
0 */6 * * * curl -s https://domain/cronjob2.php > /dev/null 2>&1
CRON
```

## Pitfalls

### .htaccess Install Gate
Many PHP apps (like MirzaPro2) have an `install/index.php` installer. The `.htaccess` blocks ALL access to the main site while `install/index.php` exists:
```
RewriteCond %{DOCUMENT_ROOT}/install/index.php -f
RewriteCond %{REQUEST_URI} !^/install/
RewriteRule ^ - [F,L]
```
**Fix:** Access `/install/` first to complete setup, OR modify `.htaccess` to check for `.installed` flag instead, OR remove `install/` directory after setup.

### First-Run Installer Removal
Some apps (e.g., MirzaPro2) call `mirzaEnsureInstallerRemoved()` on first `index.php` hit, which deletes the `install/` directory. This is intentional — the install directory is a one-time setup gate.

### systemctl Not Available in Containers
Use `service` instead:
```bash
service apache2 restart    # not systemctl restart apache2
service mariadb start
service cron start
```

### Composer Git Ownership Warning
```
fatal: detected dubious ownership in repository
```
Fix: `git config --global --add safe.directory /path/to/repo`

### Missing Tools in Containers
`dig`, `nslookup`, `file` may not be installed. Use python3 fallbacks:
```bash
python3 -c "import socket; print(socket.gethostbyname('domain'))"
ls -lh file  # instead of file command
```

## MirzaPro2 Specific Reference
- **Repo:** `github.com/mahdiMGF2/mirza_pro`
- **Auto-installer:** `github.com/iaghapour/MirzaPro2-Auto-Installer`
- **Config file:** `config.php` with DB creds + Telegram bot token + admin ID
- **DB tables:** Created via `php table.php` (uses `db/bootstrap.php`)
- **Webhook:** Set automatically by `table.php` via Telegram Bot API
- **Cron jobs:** 16 jobs hitting `cronbot/*.php` endpoints (notifications, payments, config management, backups)
- **Cron setup:** `activecron()` function in `function.php` defines all jobs
- **Supported panels:** Marzban, Marzneshin, Sanaei, S-UI, Hiddify, WGDashboard, MikroTik, IBSng

## Telegram Bot Verification
Always verify bot token before configuring:
```bash
curl -s "https://api.telegram.org/botTOKEN/getMe"
# Returns: {"ok":true,"result":{"id":...,"username":"BOT_NAME",...}}
# Use result.username for config — never guess
```
