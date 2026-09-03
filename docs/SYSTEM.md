# 📖 مستندات فنی سیستم بکاپ

*بازتولید خودکار — 2026-09-03 00:38 UTC*

## اجزا

| فایل | نقش |
|---|---|
| `run_backup.sh` | ارکستراتور اصلی — قفل تک‌نمونه، لاگ، push با retry |
| `export_sessions.py` | خواندن `state.db` و تولید ترنسکریپت Markdown |
| `export_assets.py` | سینک skills/memories/config + اسنپ‌شات سلامت |
| `write_docs.py` | بازتولید README و همین فایل با آمار زنده |
| `build_dashboard.py` | ساخت داشبورد `brain.html` |

## آمار فعلی

- Sessions در دیتابیس: **3**
- پیام‌های فعال: **1,091**
- مهارت‌های نصب‌شده: **91**

## نکات امنیتی

1. توکن گیت‌هاب فقط داخل `run_backup.sh` روی سرور است؛ هرگز وارد ریپو نمی‌شود.
2. `config.yaml` قبل از آپلود رمززدایی می‌شود (`🔒 [REDACTED]`).
3. از `.env` فقط «نام کلیدها» ذخیره می‌شود، بدون مقدار.
4. دیتابیس با حالت read-only و immutable باز می‌شود تا هرگز خراب نشود.

## عیب‌یابی

```bash
tail -50 /data/workspace/backup.log     # لاگ آخرین اجرا
bash /data/workspace/backup_scripts/run_backup.sh   # اجرای دستی
```
