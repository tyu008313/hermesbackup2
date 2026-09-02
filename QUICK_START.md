# 🚀 راهنمای سریع نصب VPN Server روی Railway

## 📋 پیش‌نیازها

- [ ] Railway Account
- [ ] GitHub Account
- [ ] توکن ربات تلگرام
- [ ] آیدی عددی ادمین

---

## 🎯 مرحله ۱: آماده‌سازی

### ۱.۱ فایل‌ها رو کپی کن:

```
Dockerfile.railway  →  ریپوی گیت هاب
docker-compose.yml  →  ریپوی گیت هاب
```

### ۱.۲ تنظیمات رو ویرایش کن:

توی `Dockerfile.railway` مقادیر زیر رو عوض کن:

```dockerfile
{YOUR_BOT_TOKEN}  →  توکن ربات تلگرام
{YOUR_ADMIN_ID}   →  آیدی عددی ادمین
{YOUR_BOT_NAME}   →  نام ربات (بدون @)
```

---

## 🎯 مرحله ۲: ایجاد ریپوی گیت هاب

```bash
# ایجاد ریپوی جدید
gh repo create my-vpn-server --public

# آپلود فایل‌ها
git init
git add .
git commit -m "Initial VPN server setup"
git remote add origin https://github.com/YOUR_USERNAME/my-vpn-server.git
git push -u origin main
```

---

## 🎯 مرحله ۳: اتصال به Railway

1. برو به [railway.app](https://railway.app)
2. روی **New Project** کلیک کن
3. **Deploy from GitHub repo** رو انتخاب کن
4. ریپوی **my-vpn-server** رو انتخاب کن
5. Railway خودکار فایل `Dockerfile.railway` رو پیدا میکنه

---

## 🎯 مرحله ۴: تنظیمات Railway

### ۴.۱ Variable‌ها رو اضافه کن:

| Variable | مقدار |
|----------|--------|
| `BOT_TOKEN` | توکن ربات تلگرام |
| `ADMIN_ID` | آیدی عددی ادمین |
| `BOT_NAME` | نام ربات |

### ۴.۲ Custom Start Command:

```bash
bash /root/restart.sh && tail -f /dev/null
```

---

## 🎯 مرحله ۵: تست نصب

### ۵.۱ لاگ‌ها رو چک کن:

```bash
railway logs
```

### ۵.۲ آدرس تونل رو پیدا کن:

```bash
railway logs | grep "trycloudflare.com"
```

### ۵.۳ ربات رو تست کن:

به ربات تلگرام پیام بده و `/start` بزن!

---

## 🔧 عیب‌یابی

### مشکل ۱: TUN Device

```bash
# اگه خطای TUN اومد
railway run mknod /dev/net/tun c 10 200
railway run chmod 600 /dev/net/tun
```

### مشکل ۲: MariaDB

```bash
# اگه دیتابیس وصل نشد
railway run service mariadb start
railway run mysql -u root -e "SHOW DATABASES;"
```

### مشکل ۳: Apache

```bash
# اگه وب‌سرور کار نکرد
railway run service apache2 restart
railway run curl -s http://localhost/
```

---

## 📊 وضعیت سرویس‌ها

| سرویس | پورت | وضعیت |
|-------|------|--------|
| **SSH** | 22 | ✅ فعال |
| **HTTP** | 80 | ✅ فعال |
| **HTTPS** | 443 | ✅ فعال |
| **OpenVPN** | 1194/udp | ✅ فعال |
| **WireGuard** | 51820/udp | ✅ فعال |

---

## 🔐 اطلاعات اتصال

### OpenVPN:

```bash
# دانلود فایل کانفیگ
railway run cat /root/client.ovpn > client.ovpn

# اتصال
openvpn --config client.ovpn
```

### WireGuard:

```bash
# دانلود فایل کانفیگ
railway run cat /etc/wireguard/client.conf > client.conf

# اتصال
wg-quick up client
```

---

## 📞 پشتیبانی

اگه مشکلی داشتی:
1. لاگ‌ها رو چک کن: `railway logs`
2. سرویس‌ها رو ریستارت کن: `railway run /root/restart.sh`
3. از رضا کمک بگیر! 😊

---

**🎉 موفق باشی!** 🔥
