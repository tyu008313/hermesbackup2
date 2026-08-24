#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERMES BRAIN BACKUP — Session Exporter
=======================================
Reads the Hermes state.db (SQLite + FTS5) and renders every session as a
clean, human-readable Markdown transcript under 02_OPERATIONS/sessions/.

NO LLM. NO NETWORK. Pure deterministic file generation.

Output layout:
  02_OPERATIONS/sessions/
    00_INDEX.md                          <- master session index (table)
    YYYY-MM-DD/                          <- one folder per day (UTC)
      HHMMSS_<session-id-short>/         <- one folder per session
        01_TRANSCRIPT.md                 <- full readable conversation
        02_METADATA.json                 <- raw session row metadata
        03_TOOLS.md                      <- tool-call summary table
"""

import os
import sys
import re
import json
import sqlite3
from datetime import datetime, timezone

sys.path.insert(0, "/data/workspace/backup_scripts")
from scrub import scrub

HERMES_HOME = "/data/.hermes"
DB_PATH = os.path.join(HERMES_HOME, "state.db")
OUT_ROOT = "/data/workspace/backup_repo/02_OPERATIONS/sessions"

MAX_MSG_CHARS = 20000   # per-message hard cap for very long tool outputs
PREVIEW_CHARS = 300     # preview length inside tables


def safe_name(s: str) -> str:
    """Filesystem-safe slug."""
    s = re.sub(r'[^\w\-. ]+', '_', str(s or ''))
    s = re.sub(r'\s+', '_', s.strip())
    return s[:80] or "untitled"


def ts_to_dt(ts):
    """Hermes stores unix floats in most columns."""
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(float(ts), tz=timezone.utc)
    except Exception:
        return None


def fmt_dt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC") if dt else "—"


def clip(text, n):
    t = str(text or "")
    return t if len(t) <= n else t[:n] + f"\n… [clipped {len(t)-n} chars]"


def render_content(raw):
    """Message content can be a JSON array of content-blocks or plain text."""
    if raw is None:
        return ""
    raw = str(raw)
    try:
        parsed = json.loads(raw)
    except Exception:
        return raw

    parts = []
    if isinstance(parsed, list):
        for block in parsed:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    parts.append(block.get("text", ""))
                elif btype == "tool_use":
                    args = json.dumps(block.get("input", {}), ensure_ascii=False)[:1500]
                    parts.append(f"⚙️ **TOOL CALL → `{block.get('name','?')}`**\n```json\n{args}\n```")
                elif btype == "tool_result":
                    c = block.get("content", "")
                    if isinstance(c, list):
                        c = "\n".join(
                            b.get("text", "") for b in c if isinstance(b, dict))
                    parts.append(f"📤 **TOOL RESULT**\n```\n{clip(c, MAX_MSG_CHARS)}\n```")
                elif btype:
                    parts.append(f"[{btype} block]")
            elif isinstance(block, str):
                parts.append(block)
    elif isinstance(parsed, dict):
        parts.append(parsed.get("text", "") or json.dumps(parsed, ensure_ascii=False)[:MAX_MSG_CHARS])
    return "\n\n".join(parts) if parts else raw


ROLE_ICON = {"user": "🧑 **USER**", "assistant": "🤖 **ASSISTANT**",
             "tool": "🔧 **TOOL**", "system": "⚙️ **SYSTEM**"}


def export():
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sessions = cur.execute(
        "SELECT * FROM sessions ORDER BY started_at ASC").fetchall()
    stats = {"sessions": len(sessions), "messages": 0, "new_sessions": [],
             "skipped": 0}
    index_rows = []

    for sess in sessions:
        sid = sess["id"]
        start = ts_to_dt(sess["started_at"]) or datetime(1970, 1, 1, tzinfo=timezone.utc)
        day = start.strftime("%Y-%m-%d")
        time_s = start.strftime("%H%M%S")
        title = sess["title"] or "Untitled session"
        short_id = str(sid).replace("-", "")[:12]

        sess_dir = os.path.join(OUT_ROOT, day,
                                f"{time_s}_{safe_name(title)}_{short_id}")
        os.makedirs(sess_dir, exist_ok=True)

        # ---------- skip unchanged sessions (marker check) ----------
        meta_path = os.path.join(sess_dir, "02_METADATA.json")
        msg_count_db = cur.execute(
            "SELECT COUNT(*) FROM messages WHERE session_id=?", (sid,)).fetchone()[0]
        if os.path.exists(meta_path):
            try:
                prev = json.load(open(meta_path))
                if prev.get("_message_count") == msg_count_db and \
                   prev.get("_ended") is not None and sess["ended_at"] is not None:
                    index_rows.append((start, title, sess_dir, msg_count_db,
                                       prev.get("_last_msg_at", "")))
                    stats["skipped"] += 1
                    continue
            except Exception:
                pass

        msgs = cur.execute(
            "SELECT * FROM messages WHERE session_id=? AND active=1 "
            "ORDER BY id ASC", (sid,)).fetchall()

        # ---------- 01_TRANSCRIPT.md ----------
        L = []
        L.append(f"# 💬 {title}\n")
        L.append(f"> **Session ID:** `{sid}`  ")
        L.append(f"> **Source:** {sess['source'] or '?'} | "
                 f"**Platform chat:** `{sess['chat_id'] or '-'}`  ")
        L.append(f"> **Started:** {fmt_dt(start)}  ")
        L.append(f"> **Ended:** {fmt_dt(ts_to_dt(sess['ended_at']))}  ")
        L.append(f"> **Model:** `{sess['model'] or '?'}` | "
                 f"**Messages:** {len(msgs)} | "
                 f"**Tool calls:** {sess['tool_call_count'] or 0}\n")
        L.append("---\n")

        tool_rows = []
        for m in msgs:
            body = scrub(render_content(m["content"]))
            icon = ROLE_ICON.get(m["role"], m["role"])
            ts = fmt_dt(ts_to_dt(m["timestamp"]))
            L.append(f"<details>\n<summary>{icon} — {ts}"
                     + (f" (`{m['tool_name']}`)" if m["tool_name"] else "")
                     + "</summary>\n")
            L.append("")
            L.append(clip(body, MAX_MSG_CHARS) if body else "*(empty)*")
            L.append("\n</details>\n")
            if m["tool_name"]:
                tool_rows.append((ts, m["tool_name"],
                                  (body or "")[:PREVIEW_CHARS].replace("|", "\\|")))

            # token accounting
        in_t = (sess["input_tokens"] or 0) + (sess["cache_read_tokens"] or 0)
        out_t = (sess["output_tokens"] or 0)
        L.append("---\n### 📊 Token Usage\n")
        L.append(f"| Metric | Value |\n|---|---|")
        L.append(f"| Input tokens (+cache read) | {in_t:,} |")
        L.append(f"| Output tokens | {out_t:,} |")
        L.append(f"| API calls | {sess['api_call_count'] or 0} |")
        L.append(f"| Estimated cost | ${sess['estimated_cost_usd'] or 0:.4f} |\n")

        open(os.path.join(sess_dir, "01_TRANSCRIPT.md"), "w",
             encoding="utf-8").write("\n".join(L))

        # ---------- 03_TOOLS.md ----------
        T = ["# 🔧 Tool Call Log\n",
             "| Time | Tool | Preview |", "|---|---|---|"]
        if tool_rows:
            for ts, name, pv in tool_rows:
                pv = " ".join(pv.split())[:120]
                T.append(f"| {ts} | `{name}` | {pv or '—'} |")
        else:
            T.append("| — | *(no tool calls)* | — |")
        open(os.path.join(sess_dir, "03_TOOLS.md"), "w",
             encoding="utf-8").write("\n".join(T))

        # ---------- 02_METADATA.json ----------
        meta = {
            "session_id": sid,
            "title": title,
            "source": sess["source"],
            "chat_id": sess["chat_id"],
            "display_name": sess["display_name"],
            "model": sess["model"],
            "profile": sess["profile_name"],
            "cwd": sess["cwd"],
            "started_at_utc": fmt_dt(start),
            "ended_at_utc": fmt_dt(ts_to_dt(sess["ended_at"])),
            "message_count_db": msg_count_db,
            "tool_call_count": sess["tool_call_count"],
            "input_tokens": in_t,
            "output_tokens": out_t,
            "estimated_cost_usd": sess["estimated_cost_usd"],
            "_message_count": msg_count_db,
            "_ended": bool(sess["ended_at"]),
            "_exported_at": datetime.now(timezone.utc).isoformat(),
            "_last_msg_at": fmt_dt(ts_to_dt(sess["last_activity_at"])),
        }
        json.dump(meta, open(meta_path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

        index_rows.append((start, title, sess_dir, msg_count_db,
                           meta["_last_msg_at"]))
        stats["messages"] += len(msgs)
        stats["new_sessions"].append(sid)

    # ---------- 00_INDEX.md ----------
    I = ["# 📚 Master Session Index\n",
         "> Auto-generated by `export_sessions.py` — no LLM involved.\n",
         f"**Total sessions:** {len(sessions)} | "
         f"**Exported/updated this run:** {stats['sessions'] - stats['skipped']} | "
         f"**Unchanged (skipped):** {stats['skipped']} | "
         f"**Messages indexed:** {stats['messages']:,}\n",
         "| Date | Session | Msgs | Last activity | Folder |", "|---|---|---|---|---|"]
    for start, title, sess_dir, cnt, last in sorted(index_rows, reverse=True):
        rel = os.path.relpath(sess_dir, OUT_ROOT)
        I.append(f"| {start.strftime('%Y-%m-%d %H:%M')} | {title[:60]} | "
                 f"{cnt} | {last} | [`{rel}`]({rel}/01_TRANSCRIPT.md) |")
    open(os.path.join(OUT_ROOT, "00_INDEX.md"), "w",
         encoding="utf-8").write("\n".join(I))

    con.close()
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    export()
