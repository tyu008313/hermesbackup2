#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERMES BRAIN BACKUP — Core Assets Exporter
==========================================
Copies skills + memories + config into the repo, deterministic and idempotent.
NO LLM. NO NETWORK.

Layout:
  01_CORE_ASSETS/skills/<category>/<skill>/...   (SKILL.md + references)
  01_CORE_ASSETS/memories/MEMORY.md, USER.md
  03_INFRASTRUCTURE/config/config.yaml           (secrets redacted)
  05_SYSTEM_INTELLIGENCE/health/LATEST.md        (system health snapshot)
"""

import os
import sys
import re
import json
import shutil
import sqlite3
from datetime import datetime, timezone

sys.path.insert(0, "/data/workspace/backup_scripts")
from scrub import scrub_tree, scrub_file

HERMES_HOME = "/data/.hermes"
REPO = "/data/workspace/backup_repo"

# ---------------- Skills & memories ----------------

def export_skills():
    src = os.path.join(HERMES_HOME, "skills")
    dst = os.path.join(REPO, "01_CORE_ASSETS", "skills")
    if not os.path.isdir(src):
        return {"skills": 0}
    # wipe + re-copy for perfect sync (deletions propagate)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))
    n = sum(1 for r, _, fs in os.walk(dst) for f in fs if f == "SKILL.md")
    return {"skills": n}


def export_memories():
    out = []
    mroot = os.path.join(HERMES_HOME, "memories")
    dst = os.path.join(REPO, "01_CORE_ASSETS", "memories")
    os.makedirs(dst, exist_ok=True)
    # flat memory files (MEMORY.md / USER.md / *.md)
    for root, _, files in os.walk(mroot):
        for f in files:
            if f.endswith((".md", ".json")):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, mroot)
                tgt = os.path.join(dst, rel)
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                shutil.copy2(full, tgt)
                out.append(rel)
    return {"memory_files": len(out)}


# ---------------- Config (redacted) ----------------
SECRET_KEYS = re.compile(
    r"(token|secret|password|api_key|apikey|key|authorization)", re.I)


def redact_yaml_line(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#") or ":" not in line:
        return line
    k, _, v = line.partition(":")
    key = k.strip().strip('"\'')
    v = v.strip()
    if SECRET_KEYS.search(key) and v and v not in ('null', '~', '""', "''", '{}', '[]'):
        indent = line[:len(line) - len(stripped)]
        return f"{indent}{k.split(':')[0]}: 🔒 [REDACTED]\n"
    return line


def export_config():
    src = os.path.join(HERMES_HOME, "config.yaml")
    dst_dir = os.path.join(REPO, "03_INFRASTRUCTURE", "config")
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "config.yaml")
    if os.path.exists(src):
        lines = open(src, encoding="utf-8").readlines()
        open(dst, "w", encoding="utf-8").writelines(redact_yaml_line(l) for l in lines)
    return {"config": os.path.exists(src)}


def export_env_structure():
    """Structure of .env (keys only, never values)."""
    src = os.path.join(HERMES_HOME, ".env")
    dst_dir = os.path.join(REPO, "03_INFRASTRUCTURE", "config")
    os.makedirs(dst_dir, exist_ok=True)
    rows = ["# .env structure — KEY NAMES ONLY (values never leave the machine)\n"]
    if os.path.exists(src):
        for ln in open(src):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k = ln.split("=", 1)[0]
                rows.append(f"{k}=🔒")
    open(os.path.join(dst_dir, ".env.structure.txt"), "w").write("\n".join(rows) + "\n")


# ---------------- System health snapshot ----------------

def export_health():
    out_dir = os.path.join(REPO, "05_SYSTEM_INTELLIGENCE", "health")
    os.makedirs(out_dir, exist_ok=True)

    host_rows = []
    try:
        import platform as pl
        uptime = os.popen("uptime -p 2>/dev/null").read().strip() or "?"
        mem = os.popen("free -h --si 2>/dev/null | awk '/Mem:/{print $3\" used / \"$2\" total\"}'").read().strip()
        disk = os.popen("df -h / | awk 'NR==2{print $3\" used / \"$2\" total (\"$5\")\"}'").read().strip()
        load1 = os.getloadavg()[0]
        host_rows = [
            ("Host OS", f"{pl.system()} {pl.release()}"),
            ("Python", pl.python_version()),
            ("Uptime", uptime),
            ("Memory", mem or "?"),
            ("Disk /", disk or "?"),
            ("Load avg (1m)", f"{load1:.2f}"),
        ]
    except Exception:
        pass

    # gateway status from pid file + process check
    gw = "?"
    pid_file = os.path.join(HERMES_HOME, "gateway.pid")
    try:
        pid = int(open(pid_file).read().split()[0])
        gw = "RUNNING ✅" if os.path.exists(f"/proc/{pid}") else "DOWN ❌"
    except Exception:
        pass
    host_rows.append(("Gateway", gw))

    # cron jobs count
    jobs = "?"
    try:
        con = sqlite3.connect(f"file:{os.path.join(HERMES_HOME,'cron','executions.db')}?mode=ro", uri=True)
        jobs = str(con.execute("SELECT COUNT(*) FROM jobs WHERE enabled=1").fetchone()[0])
        con.close()
        host_rows.append(("Enabled cron jobs", jobs))
    except Exception:
        pass

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = [f"# 🩺 System Health — {now}\n",
         "> Snapshot at backup time. History kept in git.\n",
         "| Component | Status |", "|---|---|"]
    for k, v in host_rows:
        L.append(f"| {k} | {v} |")

    # logs tail
    log_dir = os.path.join(HERMES_HOME, "logs")
    tails = []
    for lf in ("gateway.log", "agent.log", "errors.log"):
        p = os.path.join(log_dir, lf)
        if os.path.exists(p):
            tail = os.popen(f"tail -n 15 '{p}'").read()
            tails.append(f"<details>\n<summary><code>{lf}</code> (last 15 lines)</summary>\n\n"
                         f"```\n{tail}```\n</details>\n")
    if tails:
        L.append("\n## 📜 Recent Log Tails\n")
        L.extend(tails)

    open(os.path.join(out_dir, "LATEST.md"), "w", encoding="utf-8").write("\n".join(L))
    # timestamped history copy
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    open(os.path.join(out_dir, f"health_{stamp}.md"), "w", encoding="utf-8").write("\n".join(L))


# ---------------- own scripts (self-documenting repo) ----------------

def export_own_scripts():
    """Copy the backup system itself into the repo (token-scrubbed)."""
    src_dir = "/data/workspace/backup_scripts"
    dst_dir = os.path.join(REPO, "03_INFRASTRUCTURE", "scripts")
    os.makedirs(dst_dir, exist_ok=True)
    n = 0
    for fn in os.listdir(src_dir):
        if not fn.endswith((".py", ".sh")):
            continue
        src = os.path.join(src_dir, fn)
        dst = os.path.join(dst_dir, fn)
        shutil.copy2(src, dst)
        # hard-scrub: kills any embedded tokens regardless of env vars
        if scrub_file(dst):
            pass
        n += 1
    return {"own_scripts": n}


# ---------------- main ----------------

if __name__ == "__main__":
    result = {}
    result.update(export_skills())
    result.update(export_memories())
    result.update(export_config())
    result.update(export_own_scripts())
    export_env_structure()
    export_health()
    # FINAL DEFENSE: scrub entire repo for any leaked secrets
    result["scrubbed_files"] = scrub_tree(REPO)
    print(json.dumps(result))
