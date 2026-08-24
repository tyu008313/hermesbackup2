#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secret scrubber for agent-state backups (validated Aug 2026).
Usage:
    from secret_scrub import scrub, scrub_file, scrub_tree
    cleaned = scrub(text)                    # strings
    changed = scrub_file(path)               # one file in place
    n       = scrub_tree(repo_root)          # whole tree, returns files changed
Literal exact-match: set env HERMES_SCRUB_LITERALS="tok1 tok2" (space-separated,
>=12 chars each) before calling — e.g. the GitHub PAT driving the push.
Run scrub_tree as the LAST export step, before any commit/push.
"""

import os
import re

_EXTRA = [t for t in os.environ.get("HERMES_SCRUB_LITERALS", "").split()
          if len(t) >= 12]

PATTERNS = [
    # Version-control provider tokens
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{10,}\b"), "gh****REDACTED****"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{16,}\b"), "github_pat_REDACTED"),
    (re.compile(r"\bglsa_[A-Za-z0-9]{16,}\b"), "gls_REDACTED"),
    # AI providers
    (re.compile(r"\bsk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{16,}\b"), "sk-REDACTED"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b"), "sk-ant-REDACTED"),
    (re.compile(r"\bco_[A-Za-z0-9]{20,}\b"), "co_REDACTED"),
    # Cloud / SaaS
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AKIA_REDACTED"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"), "xox-REDACTED"),
    (re.compile(r"\bglpat-[A-Za-z0-9_-]{16,}\b"), "glpat-REDACTED"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"), "AIza_REDACTED"),
    (re.compile(r"\byandex_[A-Za-z0-9_]{16,}|\bag-[A-Za-z0-9_]{28,}\b"), "yandex_REDACTED"),
    (re.compile(r"\bbot\d{6,}:[A-Za-z0-9_-]{30,}\b"), "bot_token_REDACTED"),
    # Auth headers
    (re.compile(r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]{18,}"), r"\1 ****REDACTED****"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*)[\"']?[A-Za-z0-9._~+/=-]{18,}"), r'\1 "REDACTED"'),
]

# key=value style assignments of anything secret-looking (value >= 12 chars)
KV_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|apikey|access[_-]?token|auth[_-]?token|secret|passwd|password)"
    r"(\s*[=:]\s*)([\"']?)[A-Za-z0-9._~+/=\-]{12,}([\"']?)")
KV_REPL = r"\1\2\3****REDACTED****\4"


def scrub(text):
    if not text:
        return text
    t = str(text)
    for pat, rep in PATTERNS:
        t = pat.sub(rep, t)
    t = KV_PATTERN.sub(KV_REPL, t)
    for lit in _EXTRA:
        if lit in t:
            t = t.replace(lit, lit[:6] + "\u2026****REDACTED****")
    return t


def scrub_file(path, enc="utf-8"):
    """Scrub a text file in place. Returns True if modified."""
    try:
        with open(path, encoding=enc, errors="strict") as f:
            original = f.read()
    except (UnicodeDecodeError, IsADirectoryError, PermissionError):
        return False          # binary or unreadable — skip
    cleaned = scrub(original)
    if cleaned != original:
        with open(path, "w", encoding=enc) as f:
            f.write(cleaned)
        return True
    return False


def scrub_tree(root, extensions=(".md", ".txt", ".json", ".yaml", ".yml",
                                 ".html", ".py", ".sh", ".csv", ".log")):
    """Walk a directory and scrub every matching text file. Returns count."""
    changed = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(extensions):
                if scrub_file(os.path.join(dirpath, fn)):
                    changed += 1
    return changed


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "/data/workspace/backup_repo"
    print(f"scrubbed files: {scrub_tree(root)}")
