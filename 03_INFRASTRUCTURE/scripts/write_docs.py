#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERMES BRAIN BACKUP — Docs Writer
=================================
Regenerates README.md + docs so they ALWAYS reflect the latest data.
Counts are computed live from the repo — never stale. No LLM.
"""

import os
import json
import sqlite3
from datetime import datetime, timezone

REPO = "/data/workspace/backup_repo"
HERMES = "/data/.hermes"


def count_sessions():
    n_msgs = 0
    n_sess = 0
    try:
        con = sqlite3.connect(f"file:{HERMES}/state.db?mode=ro&immutable=1", uri=True)
        n_sess = con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        n_msgs = con.execute("SELECT COUNT(*) FROM messages WHERE active=1").fetchone()[0]
        con.close()
    except Exception:
        pass
    return n_sess, n_msgs


def count_skills():
    root = os.path.join(REPO, "01_CORE_ASSETS", "skills")
    return sum(1 for dp, dn, fn in os.walk(root) if "SKILL.md" in fn)


def main():
    n_sess, n_msgs = count_sessions()
    n_skills = count_skills()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    readme = f"""# 🧠 HERMES BRAIN — مرکز مغز دیجیتال

![Status](https://img.shields.io/badge/backup-auto_12h-brightgreen?style=flat-square)
![Mode](https://img.shields.io/badge/LLM%20tokens-0-success?style=flat-square)
![Sessions](https://img.shields.io/badge/sessions-{n_sess}-blue?style=flat-square)
![Messages](https://img.shills-placeholder/{n_msgs}/x) <!-- replaced below -->
![Skills](https://img.shields.io/badge/skills-{n_skills}-orange?style=flat-square)

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
| نمای گرافیکی همه‌چیز | [داشبورد brain.html]({'https://tyu008313.github.io/hermesbackup2/brain.html'}) |

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
*آخرین سینک: {now} — توسط Hermes Brain Backup System v2*
"""
    # fix the broken placeholder badge line properly
    readme = readme.replace(
        f'![Messages](https://img.shills-placeholder/{n_msgs}/x) <!-- replaced below -->',
        f'![Messages](https://img.shields.io/badge/messages-{n_msgs}-blueviolet?style=flat-square)')

    open(os.path.join(REPO, "README.md"), "w", encoding="utf-8").write(readme)

    docs = f"""# 📖 مستندات فنی سیستم بکاپ

*بازتولید خودکار — {now}*

## اجزا

| فایل | نقش |
|---|---|
| `run_backup.sh` | ارکستراتور اصلی — قفل تک‌نمونه، لاگ، push با retry |
| `export_sessions.py` | خواندن `state.db` و تولید ترنسکریپت Markdown |
| `export_assets.py` | سینک skills/memories/config + اسنپ‌شات سلامت |
| `write_docs.py` | بازتولید README و همین فایل با آمار زنده |
| `build_dashboard.py` | ساخت داشبورد `brain.html` |

## آمار فعلی

- Sessions در دیتابیس: **{n_sess}**
- پیام‌های فعال: **{n_msgs:,}**
- مهارت‌های نصب‌شده: **{n_skills}**

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
"""
    os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
    open(os.path.join(REPO, "docs", "SYSTEM.md"), "w", encoding="utf-8").write(docs)
    print(f"docs written: sessions={n_sess} msgs={n_msgs} skills={n_skills}")


if __name__ == "__main__":
    main()
