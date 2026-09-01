# 🤖 HERMES AGENT — FULL SESSION CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════
# این فایل رو اول هر جلسه جدید بخون تا کامل بدونی چه اتفاقی افتاده
# ═══════════════════════════════════════════════════════════════════════════════

## 👤 اطلاعات کاربر

| آیتم | مقدار |
|------|-------|
| **نام** | رضا (Reza) |
| **تلگرام** | @RG7YT |
| **آیدی عددی** | `7025776524` |
| **زبان** | فارسی (Persian) — همیشه فارسی جواب بده |
| **سبک پاسخ** | سریع، دقیق، بدون توضیحات اضافی |
| **پلتفرم** | Telegram |
| **هاست** | Railway (container-based) |

---

## 🖥️ اطلاعات سرور

| آیتم | مقدار |
|------|-------|
| **IP** | `152.55.176.108` |
| **OS** | Debian 13 (trixie) |
| **User** | root |
| **RAM** | ~3.5 GB |
| **Disk** | ~30 GB |
| **PHP** | 8.4.24 |
| **Apache** | 2.4.68 |
| **MariaDB** | 11.8.6 |
| **Composer** | 2.10.3 |
| **cloudflared** | 2026.8.3 |
| **3x-ui** | v3.7.0 |
| **Xray** | 26.7.28 |

⚠️ **مهم:** `systemctl` کار نمیکنه! همیشه از `service <name> <action>` استفاده کن.

---

## 🤖 ربات تلگرام MirzaPro2

| آیتم | مقدار |
|------|-------|
| **نام ربات** | `@OXINNET_BOT` |
| **توکن** | `8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ` |
| **آیدی ادمین** | `7025776524` |
| **مسیر نصب** | `/var/www/mirza_pro/` |
| **فایل کانفیگ** | `/var/www/mirza_pro/config.php` |
| **دیتابیس** | `mirza_pro` |
| **کاربر دیتابیس** | `mirza_user` |
| **پسورد دیتابیس** | `Mirza@2026!Secure` |
| **وب‌هوک** | `https://hottest-pace-pets-alexandria.trycloudflare.com/index.php` |

### فیکس‌های اعمال شده روی ربات:
1. **function.php — checktelegramip()** اصلاح شد تا درخواست‌های Cloudflare Tunnel (localhost) رو قبول کنه
2. **جدول admin** آیدی ادمین به `7025776524` تغییر کرد (قبلاً `YOUR_TELEGRAM_ID_HERE` بود)
3. **جدول user** — `roll_Status=1` و `joinchannel=active` برای ادمین تنظیم شد

### دستورات مدیریت ربات:
```bash
# ریستارت Apache
service apache2 restart

# استارت MariaDB
service mariadb start

# لاگ ربات
cat /var/www/mirza_pro/error_log

# ویرایش کانفیگ
nano /var/www/mirza_pro/config.php

# آپدیت webhook
curl -s "https://api.telegram.org/bot8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ/deleteWebhook"
curl -s "https://api.telegram.org/bot8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ/setWebhook?url=https://TUNNEL_URL/index.php"
```

---

## 🔐 پنل 3x-ui (VPN Panel)

| آیتم | مقدار |
|------|-------|
| **آدرس پنل** | `https://penguin-niagara-texture-sparc.trycloudflare.com/edVa7HUn6PhwR2MYGv` |
| **نام کاربری** | `8sfaIDPFiK` |
| **پسورد** | `Ys8lzIA86c` |
| **Web Base Path** | `edVa7HUn6PhwR2MYGv` |
| **API Token** | `0GX2FxPn56PQwkKbMkkpwNEdOZTgICRmBD5qwO1F3FCNWMt3` |
| **پورت پنل** | `8080` |
| **مسیر نصب** | `/usr/local/x-ui/` |
| **دیتابیس** | `/etc/x-ui/x-ui.db` (SQLite) |
| **فایل کانفیگ xray** | `/usr/local/x-ui/bin/config.json` |

### اطلاعات Inbound (Xray):

| آیتم | مقدار |
|------|-------|
| **ID** | `1` |
| **Remark** | `CloudFlare-VLESS` |
| **Port** | `2083` |
| **Protocol** | `vless` |
| **Network** | `ws` (WebSocket) |
| **Path** | `/` |
| **Host** | `federal-sharp-permitted-wyoming.trycloudflare.com` |
| **Security** | `none` (local) / `tls` (Cloudflare CDN) |

### اطلاعات Host (Cloudflare CDN):

| آیتم | مقدار |
|------|-------|
| **Address** | `federal-sharp-permitted-wyoming.trycloudflare.com` |
| **Port** | `443` |
| **Security** | `tls` |
| **SNI** | `federal-sharp-permitted-wyoming.trycloudflare.com` |
| **ALPN** | `h2, http/1.1` |
| **Fingerprint** | `chrome` |

### اطلاعات Client:

| آیتم | مقدار |
|------|-------|
| **UUID** | `8af924af-92ac-46c0-a9c0-6b4042534995` |
| **Email** | `x6727v0zyn` |
| **SubId** | `z09a7mxt0pv36w9s` |
| **Password** | `07cpd1y6fusjb0ub` |
| **Auth** | `9bcnrcqll5j5f620` |

### کانفیگ VLESS:
```
vless://8af924af-92ac-46c0-a9c0-6b4042534995@federal-sharp-permitted-wyoming.trycloudflare.com:443?encryption=none&security=tls&sni=federal-sharp-permitted-wyoming.trycloudflare.com&type=ws&host=federal-sharp-permitted-wyoming.trycloudflare.com&path=%2F#CloudFlare-VLESS
```

### دستورات مدیریت 3x-ui:
```bash
# استارت x-ui (از مسیر نصب)
cd /usr/local/x-ui && exec ./x-ui &

# ویرایش دیتابیس SQLite
sqlite3 /etc/x-ui/x-ui.db "SELECT * FROM inbounds;"
sqlite3 /etc/x-ui/x-ui.db "SELECT * FROM hosts;"
sqlite3 /etc/x-ui/x-ui.db "SELECT * FROM settings;"

# ریستارت x-ui
pkill -9 x-ui; sleep 2; cd /usr/local/x-ui && exec ./x-ui &

# لاگ xray
cat /usr/local/x-ui/bin/config.json
```

---

## 🌐 Cloudflare Quick Tunnels

⚠️ **مهم:** Quick Tunnel هربار ریستارت آدرسش عوض میشه! برای استفاده دائمی دامنه بخر.

### تونل‌های فعال (آخرین وضعیت):

| تونل | پورت مقصد | آدرس |
|------|----------|------|
| **ربات** | `80` (Apache) | `https://hottest-pace-pets-alexandria.trycloudflare.com` |
| **پنل** | `8080` (x-ui) | `https://penguin-niagara-texture-sparc.trycloudflare.com` |
| **Xray** | `2083` (xray) | `https://federal-sharp-permitted-wyoming.trycloudflare.com` |

### نحوه راه‌اندازی مجدد تونل‌ها:
```bash
# تونل ربات
cloudflared tunnel --url http://localhost:80 2>&1 &

# تونل پنل
cloudflared tunnel --url http://localhost:8080 2>&1 &

# تونل Xray
cloudflared tunnel --url http://localhost:2083 2>&1 &
```

بعد از هربار ریستارت تونل:
1. آدرس جدید از لاگ cloudflared بگیر
2. Webhook تلگرام رو آپدیت کن
3. config.php رو آپدیت کن
4. Cron jobs رو آپدیت کن
5. Hosts پنل 3x-ui رو آپدیت کن

---

## ⏰ Cron Jobs

```bash
# 16 cron job فعال برای www-data
crontab -u www-data -l

# فایل setup
/var/www/mirza_pro/setup_cron.sh
```

---

## 📁 ساختار فایل‌های مهم

```
/var/www/mirza_pro/          # ربات MirzaPro2
├── config.php               # کانفیگ اصلی (توکن، دیتابیس، دامنه)
├── index.php                # وب‌هوک تلگرام
├── function.php             # توابع اصلی (checktelegramip اصلاح شده)
├── botapi.php               # API تلگرام
├── keyboard.php             # کیبورد ربات
├── error_log                # لاگ خطاها
├── setup_cron.sh            # اسکریپت تنظیم cron jobs
└── cronbot/                 # فایل‌های cron

/usr/local/x-ui/            # پنل 3x-ui
├── x-ui                     # اجرایی اصلی
├── bin/
│   ├── xray-linux-amd64     # Xray core
│   └── config.json          # کانفیگ Xray
└── x-ui.sh                  # اسکریپت مدیریت

/etc/x-ui/
├── x-ui.db                  # دیتابیس SQLite پنل
└── install-result.env       # اطلاعات نصب اولیه
```

---

## 🔧 مشکلات رایج و راه‌حل‌ها

### 1. ربات کار نمیکنه (database connection failed)
```bash
service mariadb start
```

### 2. تونل Cloudflare خراب شده
```bash
pkill -9 cloudflared
# دوباره تونل‌ها رو راه بنداز
cloudflared tunnel --url http://localhost:80 2>&1 &
cloudflared tunnel --url http://localhost:8080 2>&1 &
cloudflared tunnel --url http://localhost:2083 2>&1 &
# آدرس‌های جدید رو از لاگ بگیر و همه چیز رو آپدیت کن
```

### 3. x-ui کار نمیکنه
```bash
pkill -9 x-ui
pkill -9 xray
cd /usr/local/x-ui && exec ./x-ui 2>&1 &
```

### 4. پورت اشغال شده
```bash
ss -tlnp | grep PORT_NUMBER
pkill -9 PROCESS_NAME
```

### 5. Railway ریستارت کرده و همه چیز خاموش شده
```bash
# 1. MariaDB
service mariadb start

# 2. Apache
service apache2 start

# 3. x-ui
cd /usr/local/x-ui && exec ./x-ui 2>&1 &

# 4. Cloudflare Tunnels
cloudflared tunnel --url http://localhost:80 2>&1 &
cloudflared tunnel --url http://localhost:8080 2>&1 &
cloudflared tunnel --url http://localhost:2083 2>&1 &

# 5. Webhook
curl -s "https://api.telegram.org/bot8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ/deleteWebhook"
curl -s "https://api.telegram.org/bot8691766146:AAHfGJUkGNeqWrfn7zpmoRye9-2i-EU0DnQ/setWebhook?url=https://NEW_BOT_TUNNEL/index.php"
```

---

## 📋 گیت هاب بکاپ

| آیتم | مقدار |
|------|-------|
| **ریپو** | `https://github.com/tyu008313/hermesbackup2` |
| **توکن** | `ghp_HN....` (از فایل .git/config بخون) |
| **فایل بزرگ‌ترین** | `BRAIN3D.html` (24KB) |

### دستورات گیت هاب:
```bash
cd /data/workspace/backup_repo
git add .
git commit -m "Update: $(date +%Y-%m-%d)"
git push origin main
```

### ساختار ریپو:
```
backup_repo/
├── 01_CORE_ASSETS/          # فایل‌های اصلی
├── 02_OPERATIONS/           # عملیات
├── 03_INFRASTRUCTURE/       # زیرساخت
├── 05_SYSTEM_INTELLIGENCE/  # هوش سیستم
├── BRAIN.html               # داشبورد اصلی
├── BRAIN3D.html             # داشبورد سه‌بعدی
├── HERMES_FULL_CONTEXT.md   # کانتکست کامل
└── README.md                # راهنما
```

---

## 🎯 وظیفه Hermes Agent

1. **خواندن این فایل** در ابتدای هر جلسه جدید
2. **بررسی وضعیت سرویس‌ها** و راه‌اندازی مجدد در صورت نیاز
3. **مدیریت تونل‌ها** — آدرس‌های جدید رو شناسایی و آپدیت کن
4. **پاسخ به سوالات رضا** به فارسی و سریع
5. **عیب‌یابی** مشکلات ربات و پنل
6. **بکاپ‌گیری** منظم از گیت هاب

---

## 🔄 فلوچارت ریستارت کامل

```
Railway ریستارت
    ↓
service mariadb start
    ↓
service apache2 start
    ↓
cd /usr/local/x-ui && exec ./x-ui &
    ↓
cloudflared tunnel --url http://localhost:80 &
    ↓
cloudflared tunnel --url http://localhost:8080 &
    ↓
cloudflared tunnel --url http://localhost:2083 &
    ↓
آدرس‌های جدید رو از لاگ بگیر
    ↓
Webhook تلگرام آپدیت کن
    ↓
config.php آپدیت کن
    ↓
Cron jobs آپدیت کن
    ↓
Hosts پنل آپدیت کن
    ↓
✅ همه چیز آماده!
```

---

## ⚠️ نکات حیاتی

1. **هرگز پسورد رو در چت نفرست** مگر اینکه رضا بخواد
2. **systemctl کار نمیکنه** — همیشه `service` استفاده کن
3. **Quick Tunnel موقتیه** — آدرس هربار عوض میشه
4. **Railway پورت‌ها رو محدود میکنه** — فقط 80, 443, 8080 از بیرون بازه
5. ** MariaDB خودکار استارت نمیشه** — بعد از ریستارت باید دستی استارت کنی
6. **فایل error_log** در `/var/www/mirza_pro/error_log` لاگ‌های ربات رو نگه میداره

---

## 📞 اطلاعات تماس

| پلتفرم | آدرس |
|---------|------|
| **تلگرام** | @RG7YT |
| **آیدی عددی** | 7025776524 |
| **گیت هاب** | https://github.com/tyu008313 |

---

**آخرین آپدیت:** 2026-09-01 16:30 UTC
**ایجاد شده توسط:** Hermes Agent (session: default)
**برای:** رضا (@RG7YT)
