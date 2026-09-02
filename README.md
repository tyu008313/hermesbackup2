# 🧠 HERMES BRAIN — مرکز مغز دیجیتال

![Status](https://img.shields.io/badge/backup-auto_12h-brightgreen?style=flat-square)
![Mode](https://img.shields.io/badge/LLM%20tokens-0-success?style=flat-square)
![Sessions](https://img.shields.io/badge/sessions-3-blue?style=flat-square)
![Messages](https://img.shields.io/badge/messages-1420-blueviolet?style=flat-square)
![Skills](https://img.shields.io/badge/skills-91-orange?style=flat-square)

> مخزن رسمی بکاپ کامل مغز **Hermes Agent** — جلسات، حافظه، مهارت‌ها، تنظیمات و داشبورد زنده.
> هر ۱۲ ساعت به‌صورت خودکار سینک می‌شود. کاملاً بدون مدل LLM (صفر توکن).

**🌐 داشبورد زنده:** https://tyu008313.github.io/hermesbackup2/brain.html

---

## 📂 ساختار مخزن

| پوشه | محتوا | توضیح |
|---|---|---|
| **`01_CORE_ASSETS/`** | 🧠 هسته هوش | مهارت‌ها (`skills/`) و حافظه ماندگار (`memories/`) |
| **`02_OPERATIONS/`** | 💬 عملیات | ترنسکریپت کامل جلسات به تفکیک روز + ایندکس |
| **`03_INFRASTRUCTURE/`** | ⚙️ زیرساخت | کانفیگ (رمزها حذف‌شده)، اسکریپت‌های بکاپ |
| **`04_PROJECTS_LAB/`** | 🧪 پروژه‌ها | پروژه‌های فعال |
| **`05_SYSTEM_INTELLIGENCE/`** | 🩺 هوش سیستمی | گزارش سلامت سیستم + مغز مهندسی پرامپت |

---

## 🔍 راهنمای مطالعه سریع

| می‌خوای بدونی... | برو سراغ |
|---|---|
| در همه جلسات چه گفتیم؟ | [`02_OPERATIONS/sessions/00_INDEX.md`](02_OPERATIONS/sessions/00_INDEX.md) |
| هرمس چه چیزهایی یاد گرفته؟ | [`01_CORE_ASSETS/memories/`](01_CORE_ASSETS/memories/) |
| چه مهارت‌هایی نصبه؟ | [`01_CORE_ASSETS/skills/`](01_CORE_ASSETS/skills/) |
| مغز و شخصیت هرمس چطور کار می‌کنه؟ | [`05_SYSTEM_INTELLIGENCE/BRAIN.md`](05_SYSTEM_INTELLIGENCE/BRAIN.md) |
| وضعیت لحظه‌ای سیستم؟ | [`05_SYSTEM_INTELLIGENCE/health/LATEST.md`](05_SYSTEM_INTELLIGENCE/health/LATEST.md) |
| نمای گرافیکی همه‌چیز | [داشبورد brain.html](https://tyu008313.github.io/hermesbackup2/brain.html) |

---

## 🔄 مکانیزم بکاپ خودکار

```
هر 12 ساعت:
  1️⃣ state.db → ترنسکریپت Markdown خوانا برای هر session
  2️⃣ skills + memories + config(رمززدایی‌شده) → کپی کامل
  3️⃣ README + docs → بازتولید با آمار زنده
  4️⃣ brain.html → داشبورد HTML تیره و زیبا
  5️⃣ git push (HTTPS) → قابل مشاهده در گیت‌هاب
```

- 🔒 هیچ Secret / Token / API Key هرگز آپلود نمی‌شود (فقط ساختار کلیدها)
- ♻️ Idempotent: فقط فایل‌های تغییریافته commit می‌شوند
- 🚫 بدون LLM: تمام مراحل با اسکریپت خالص Python/Bash اجرا می‌شوند

---
*آخرین سینک: 2026-09-02 12:38 UTC — توسط Hermes Brain Backup System v2*
