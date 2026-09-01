# Cloudflare Tunnel — شناسایی و تحلیل

## Cloudflare Quick Tunnel
- دامنه: `*.trycloudflare.com`
- رایگان و موقت (URL هر بار تغییر می‌کند)
- IP واقعی سرور پشت تونل مخفی است

## شناسایی از هدرها

```
server: cloudflare
cf-ray: a33cf99fdb29e8cc-SJC    ← SJC = San Jose, SFO = San Francisco
cf-cache-status: DYNAMIC
```

### موقعیت‌های رایج Cloudflare Edge
| کد | موقعیت |
|----|--------|
| SJC | San Jose, CA |
| SFO | San Francisco, CA |
| LAX | Los Angeles, CA |
| SEA | Seattle, WA |
| IAD | Ashburn, VA (Virginia) |
| ORD | Chicago, IL |
| ATL | Atlanta, GA |
| DFW | Dallas, TX |
| FRA | Frankfurt, Germany |
| AMS | Amsterdam, Netherlands |
| LHR | London, UK |
| NRT | Tokyo, Japan |

## تحلیل IP

```bash
# IP Cloudflare (Anycast)
python3 -c "import socket; print(socket.gethostbyname('DOMAIN'))"

# لوکیشن ((edge سرور، نه واقعی)
curl -s "https://ipinfo.io/IP/json"
```

**نکته:** IP برگشتی مال edge سرور Cloudflare است، نه سرور واقعی پشت تونل.

## Cloudflare Tunnel vs Cloudflare CDN
- **CDN:** دامنه اختصاصی + DNS records + SSL
- **Quick Tunnel:** `trycloudflare.com` + URL موقت + بدون تنظیم DNS

## مسیریابی غیرفعال (Catch-all)
- وقتی `curl -s URL` خروجی خالی برمی‌گرداند ولی HTTP 200 است
- یعنی سرور پشت تونل درخواست را پردازش می‌کند ولی محتوایی برنمی‌گرداند
- معمولاً webhook تلگرام است که فقط POST را قبول دارد

## الگوی تحلیل URL
1. `curl -sv` برای هدرها و TLS info
2. `python3 socket.gethostbyname` برای IP
3. `ipinfo.io` برای لوکیشن edge
4. `curl -s` برای بررسی محتوا و status code
5. جستجوی مسیرها (`/config.php`, `/.env`, `/admin.php`) برای یافتن ساختار
