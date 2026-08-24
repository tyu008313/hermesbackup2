#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERMES BRAIN BACKUP — Dashboard Generator
=========================================
Renders a self-contained dark HTML dashboard (brain.html) from the exported
markdown/JSON data. Pure Python string templating — no JS build step, no LLM.
GitHub Pages serves it at the repo root.
"""

import os
import re
import json
import html
from datetime import datetime, timezone

REPO = "/data/workspace/backup_repo"
OUT = os.path.join(REPO, "brain.html")


def esc(s):
    return html.escape(str(s or ""))


def load_sessions():
    rows = []
    root = os.path.join(REPO, "02_OPERATIONS", "sessions")
    for dirpath, dirnames, filenames in os.walk(root):
        if "02_METADATA.json" in filenames:
            try:
                m = json.load(open(os.path.join(dirpath, "02_METADATA.json"),
                                   encoding="utf-8"))
                m["_folder"] = os.path.relpath(dirpath, REPO)
                rows.append(m)
            except Exception:
                pass
    rows.sort(key=lambda x: x.get("started_at_utc", ""), reverse=True)
    return rows


def md_to_html_light(md_text):
    """Tiny markdown renderer good enough for MEMORY.md / README snippets."""
    t = esc(md_text)
    t = re.sub(r"^###### (.*)$", r"<h6>\1</h6>", t, flags=re.M)
    t = re.sub(r"^##### (.*)$", r"<h5>\1</h5>", t, flags=re.M)
    t = re.sub(r"^#### (.*)$", r"<h4>\1</h4>", t, flags=re.M)
    t = re.sub(r"^### (.*)$", r"<h3>\1</h3>", t, flags=re.M)
    t = re.sub(r"^## (.*)$", r"<h2>\1</h2>", t, flags=re.M)
    t = re.sub(r"^# (.*)$", r"<h1>\1</h1>", t, flags=re.M)
    t = re.sub(r"```(.*?)```", lambda m: f"<pre>{m.group(1)}</pre>", t, flags=re.S)
    t = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*\n]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*([^*\n]+)\*", r"<i>\1</i>", t)
    lines = t.split("\n")
    out, in_list = [], False
    for ln in lines:
        if re.match(r"^\s*[-*] ", ln):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + re.sub(r"^\s*[-*] ", "", ln) + "</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(ln)
    if in_list:
        out.append("</ul>")
    # tables (| a | b |)
    body = "\n".join(out)
    def table_repl(m):
        rows = [r for r in m.group(0).strip().split("\n") if r.strip()]
        if len(rows) < 2:
            return m.group(0)
        cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
        head = cells(rows[0])
        trs = []
        for r in rows[2:]:
            trs.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells(r)) + "</tr>")
        return ("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in head) +
                "</tr></thead><tbody>" + "".join(trs) + "</tbody></table>")
    body = re.sub(r"(?:^\|.*\|\s*$\n?){2,}", table_repl, body, flags=re.M)
    return body


def main():
    sessions = load_sessions()

    total_msgs = sum(s.get("message_count_db", 0) for s in sessions)
    total_in = sum(s.get("input_tokens", 0) for s in sessions)
    total_out = sum(s.get("output_tokens", 0) for s in sessions)
    total_cost = sum(s.get("estimated_cost_usd", 0) or 0 for s in sessions)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    session_cards = []
    for s in sessions[:100]:
        folder = s["_folder"].replace('"', '')
        gh = "https://github.com/tyu008313/hermesbackup2/tree/main/" + folder
        cards = f"""
<div class="card" onclick="window.open('{gh}','_blank')">
  <div class="card-top"><span class="badge">{esc(s.get('source','?'))}</span>
  <span class="date">{esc(s.get('started_at_utc','')[:16])}</span></div>
  <h3>{esc(s.get('title'))}</h3>
  <div class="meta">
    <span>💬 {s.get('message_count_db',0)} msgs</span>
    <span>🔧 {s.get('tool_call_count',0)} tools</span>
    <span>📥 {(s.get('input_tokens',0) or 0):,} tok in</span>
    <span>📤 {(s.get('output_tokens',0) or 0):,} tok out</span>
    <span>${(s.get('estimated_cost_usd',0) or 0):.3f}</span>
  </div>
  <div class="model">{esc(s.get('model'))}</div>
</div>"""
        session_cards.append(cards)

    memory_md = ""
    mem_path = os.path.join(REPO, "01_CORE_ASSETS", "memories", "MEMORY.md")
    user_path = os.path.join(REPO, "01_CORE_ASSETS", "memories", "USER.md")
    for p, label in ((mem_path, "MEMORY"), (user_path, "USER")):
        if os.path.exists(p):
            memory_md += f"\n<h2 class='sec'>🧠 {label}</h2>\n"
            memory_md += md_to_html_light(open(p, encoding="utf-8").read())

    skills_root = os.path.join(REPO, "01_CORE_ASSETS", "skills")
    skill_list = []
    for dp, dn, fn in os.walk(skills_root):
        if "SKILL.md" in fn:
            rel = os.path.relpath(dp, REPO)
            name = os.path.basename(dp)
            skill_list.append(
                f'<div class="skill"><a href="https://github.com/tyu008313/'
                f'hermesbackup2/tree/main/{rel.replace(os.sep, "/")}" target="_blank">'
                f'⚡ {esc(name)}</a></div>')
    skills_html = "\n".join(skill_list)

    html_doc = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🧠 HERMES BRAIN — Command Center</title>
<style>
  :root {{
    --bg:#0a0e14; --panel:#111722; --panel2:#0d1320; --line:#1d2839;
    --gold:#f0b429; --green:#2dd4a7; --blue:#5aa2ff; --txt:#dbe4f0; --dim:#7d8ca3;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--txt);
    font-family:'Segoe UI',Tahoma,Vazirmatn,sans-serif; padding:24px; }}
  .wrap {{ max-width:1200px; margin:auto; }}
  header {{ text-align:center; padding:34px 10px 22px;
    border-bottom:1px solid var(--line); margin-bottom:26px; }}
  h1 {{ font-size:2.3em; color:var(--gold);
    text-shadow:0 0 26px rgba(240,180,41,.35); letter-spacing:1px; }}
  header p {{ color:var(--dim); margin-top:8px; font-size:.95em; }}
  .stats {{ display:flex; gap:14px; flex-wrap:wrap; justify-content:center; margin:20px 0 30px; }}
  .stat {{ background:linear-gradient(160deg,var(--panel),var(--panel2));
    border:1px solid var(--line); border-radius:14px; padding:18px 30px;
    text-align:center; min-width:150px; transition:.25s; }}
  .stat:hover {{ transform:translateY(-4px); border-color:var(--gold); }}
  .stat b {{ display:block; font-size:1.9em; color:var(--gold); }}
  .stat span {{ color:var(--dim); font-size:.85em; }}
  h2.sec {{ color:var(--gold); border-right:4px solid var(--gold);
    padding-right:12px; margin:34px 0 14px; font-size:1.35em; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(330px,1fr)); gap:16px; }}
  .card {{ background:linear-gradient(165deg,var(--panel),var(--panel2));
    border:1px solid var(--line); border-radius:14px; padding:16px 18px;
    cursor:pointer; transition:.22s; }}
  .card:hover {{ border-color:var(--blue); transform:translateY(-3px);
    box-shadow:0 10px 30px rgba(0,0,0,.45); }}
  .card-top {{ display:flex; justify-content:space-between; margin-bottom:9px; }}
  .badge {{ background:rgba(90,162,255,.15); color:var(--blue); padding:2px 10px;
    border-radius:99px; font-size:.75em; border:1px solid rgba(90,162,255,.3); }}
  .date {{ color:var(--dim); font-size:.78em; direction:ltr; }}
  .card h3 {{ font-size:1.02em; margin-bottom:10px; color:var(--txt); line-height:1.5; }}
  .meta {{ display:flex; gap:12px; flex-wrap:wrap; color:var(--dim); font-size:.78em; }}
  .model {{ margin-top:9px; color:var(--green); font-size:.76em;
    font-family:monospace; direction:ltr; text-align:left; }}
  .skills {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .skill a {{ display:inline-block; background:var(--panel); border:1px solid var(--line);
    color:var(--txt); padding:6px 13px; border-radius:99px; font-size:.82em;
    text-decoration:none; transition:.2s; }}
  .skill a:hover {{ border-color:var(--gold); color:var(--gold); }}
  .brain-doc {{ background:var(--panel2); border:1px solid var(--line); border-radius:14px;
    padding:22px 26px; line-height:1.95; font-size:.92em; }}
  .brain-doc h1,.brain-doc h2 {{ color:var(--gold); font-size:1.15em; margin:14px 0 8px; }}
  .brain-doc h3 {{ color:var(--blue); font-size:1.02em; margin:11px 0 6px; }}
  .brain-doc pre {{ background:#070a10; border:1px solid var(--line); border-radius:8px;
    padding:11px; overflow-x:auto; direction:ltr; text-align:left; font-size:.84em; }}
  .brain-doc code {{ color:var(--green); direction:ltr; unicode-bidi:embed; }}
  .brain-doc table {{ width:100%; border-collapse:collapse; margin:10px 0; font-size:.86em; }}
  .brain-doc th {{ background:var(--panel); color:var(--gold); }}
  .brain-doc th,.brain-doc td {{ border:1px solid var(--line); padding:7px 10px; text-align:right; }}
  footer {{ text-align:center; color:var(--dim); padding:36px 0 14px; font-size:.82em; }}
  footer b {{ color:var(--gold); }}
</style>
</head>
<body><div class="wrap">
<header>
  <h1>🧠 HERMES BRAIN</h1>
  <p>مرکز فرماندهی — مغز دیجیتال هرمس | آخرین به‌روزرسانی: <span style="direction:ltr;display:inline-block">{now}</span></p>
</header>

<div class="stats">
  <div class="stat"><b>{len(sessions)}</b><span>جلسات ثبت‌شده</span></div>
  <div class="stat"><b>{total_msgs:,}</b><span>پیام‌ها</span></div>
  <div class="stat"><b>{total_in + total_out:,}</b><span>توکن مصرفی</span></div>
  <div class="stat"><b>${total_cost:.2f}</b><span>هزینه تخمینی</span></div>
  <div class="stat"><b>{len(skill_list)}</b><span>مهارت‌ها</span></div>
</div>

<h2 class="sec">💬 جلسات اخیر <small style="color:var(--dim);font-size:.6em">(کلیک = باز شدن در گیت‌هاب)</small></h2>
<div class="grid">{''.join(session_cards) or '<p style="color:var(--dim)">هنوز جلسه‌ای اکسپورت نشده.</p>'}</div>

<h2 class="sec">⚡ مهارت‌ها ({len(skill_list)})</h2>
<div class="skills">{skills_html}</div>

<div class="brain-doc">{memory_md}</div>

<footer>
  🤖 تولید خودکار توسط <b>Hermes Brain Backup System v2</b> — بدون مدل LLM، صفر توکن<br>
  <a href="https://github.com/tyu008313/hermesbackup2" target="_blank" style="color:var(--blue)">github.com/tyu008313/hermesbackup2</a>
</footer>
</div></body></html>"""

    open(OUT, "w", encoding="utf-8").write(html_doc)
    print(f"dashboard written: {OUT} ({os.path.getsize(OUT):,} bytes, "
          f"{len(sessions)} sessions)")


if __name__ == "__main__":
    main()
