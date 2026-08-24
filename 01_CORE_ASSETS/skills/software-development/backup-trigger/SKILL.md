---
name: backup-trigger
description: "Instant backup on BACKUP; history on BACKUP LIST."
version: 1.0.0
---

# Backup Trigger — دستور فوری بکاپ

## تریگرها
- پیام کاربر دقیقاً `BACKUP` (یا «بکاپ کن» / «بک آپ») → اجرای فوری بکاپ کامل
- پیام کاربر `BACKUP LIST` (یا «لیست بکاپ‌ها») → فقط گزارش تاریخچه، بدون push

## BACKUP — اجرای فوری

```bash
bash /data/workspace/backup_scripts/run_backup.sh
```

- خروجی را با tail نشان بده؛ خطوط کلیدی: `[1/5]..[5/5]`، `PUSH OK → <sha> (N files)`
- اگر `NOTHING NEW — repo already in sync` بود یعنی چیزی برای فرستادن نبود
- اگر `PUSH FAILED` بود: لاگ کامل `/data/workspace/backup.log` را چک کن و دوباره اجرا کن (retry داخلی دارد)
- بعد از اتمام به کاربر sha کامیت و تعداد فایل‌ها را گزارش بده
- هرگز توکن را در پاسخ یا خط فرمان نمایش نده (داخل اسکریپت است)

## BACKUP LIST — گزارش بدون تغییر

```bash
bash /data/workspace/backup_scripts/list_backups.sh
```

خروجی شامل: آخرین آپدیت (تاریخ + sha)، ۱۵ بکاپ اخیر، وضعیت working tree.
خام آن را گزارش بده ولی خوانا فرمت کن (جدول یا لیست).

## نکات
- اسکریپت قفل تک‌نمونه دارد؛ اگر همزمان با کرون ۱۲ ساعته بخورد SKIP می‌شود — عادی است
- کرون خودکار: job `dd6bd38d99d4` هر ۱۲ ساعت (no_agent) — این اسکیل فقط برای اجرای دستی فوری است
- ریپو: github.com/tyu008313/hermesbackup2 — داشبورد: https://tyu008313.github.io/hermesbackup2/brain.html
- نسخه‌ی داخل ریپوی اسکریپت‌ها (`03_INFRASTRUCTURE/scripts/`) توکن‌شان scrub شده — آن نسخه را برای اجرا استفاده نکن؛ فقط نسخه‌ی `/data/workspace/backup_scripts/` معتبر است
