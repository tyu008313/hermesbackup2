# 🚀 راهنمای سریع - VPN Server خام

## 📋 خلاصه

یه سرور **خام** ولی **کامل** با تمام دسترسی‌ها. هر چی بخوای روش نصب کن!

---

## 🎯 نصب سریع

### روش ۱: Docker Compose (پیشنهادی)

```bash
# کلون کردن ریپو
git clone https://github.com/tyu008313/hermesbackup2.git
cd hermesbackup2

# اجرا
docker-compose -f docker-compose.vpn.yml up -d

# چک کردن وضعیت
docker-compose -f docker-compose.vpn.yml logs -f
```

### روش ۲: Docker Build

```bash
# ساخت تصویر
docker build -t vpn-server -f Dockerfile.vpn .

# اجرا
docker run -d --privileged \
  --name vpn-server \
  -p 22:22 \
  -p 80:80 \
  -p 443:443 \
  -p 1194:1194/udp \
  -p 51820:51820/udp \
  vpn-server
```

---

## 🔐 اتصال

### SSH:

```bash
ssh root@localhost -p 22
```

### وضعیت سرویس‌ها:

```bash
# داخل container
/root/status.sh
```

---

## 📦 نصب ابزارها

### OpenVPN:

```bash
/root/install-openvpn.sh
/tmp/openvpn-install.sh
```

### WireGuard:

```bash
/root/install-wireguard.sh
```

### Cloudflared:

```bash
/root/install-cloudflare.sh
cloudflared tunnel --url http://localhost:80
```

---

## 📊 وضعیت پیش‌فرض

| سرویس | پورت | وضعیت |
|-------|------|--------|
| **SSH** | 22 | ✅ فعال |
| **HTTP** | 80 | ✅ فعال |
| **Apache** | - | ✅ فعال |
| **MariaDB** | - | ✅ فعال |
| **Cron** | - | ✅ فعال |
| **TUN Device** | - | ✅ فعال |

---

## 🛠️ دستورات مفید

| دستور | توضیح |
|-------|--------|
| `/root/status.sh` | وضعیت سرویس‌ها |
| `/root/restart.sh` | ریستارت سرویس‌ها |
| `/root/install-openvpn.sh` | نصب OpenVPN |
| `/root/install-wireguard.sh` | نصب WireGuard |
| `/root/install-cloudflare.sh` | نصب Cloudflared |

---

## 📁 فولدرهای کاری

| فولدر | توضیح |
|-------|--------|
| `/data` | داده‌ها |
| `/apps` | اپلیکیشن‌ها |
| `/logs` | لاگ‌ها |
| `/backup` | بکاپ‌ها |

---

## ⚠️ نکات مهم

1. **Docker با دسترسی کامل** - فقط برای سرور شخصی استفاده کن
2. **پسورد Root** - حتماً عوض کن!
3. **فایروال** - پورت‌های غیرضروری رو ببند
4. **بکاپ** - مرتب بکاپ بگیر

---

**🎉 موفق باشی!** 🔥
