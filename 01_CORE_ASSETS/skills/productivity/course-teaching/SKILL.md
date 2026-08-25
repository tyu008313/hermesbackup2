---
name: course-teaching
description: "Teach courses one lesson per chat reply, never batch-build."
version: 1.0.0
---

# Course Teaching — درس‌به‌درس (Telegram)

Delivering multi-session courses to REZA inside the Telegram DM. He learns in Persian,
at intermediate level, and chose the format explicitly: **پروژه‌محور + با منبع + اسکیل + AI**
(project-driven, with sources, skill-building, AI tools).

## ⚠️ Core Rule (user-corrected 2026-08-25)
When he asks for a course, teach **ONE lesson per reply** in chat. Do NOT respond by
building a complete course website/artifact in one shot — he interrupted exactly that with
«درس به درس برو». A course site may be built later, incrementally, only if he asks.

## Lesson anatomy (every lesson, same shape)
1. Concept explained short (3-min read, plain Persian)
2. One **golden security rule** («قانون طلایی») tied to the topic
3. Hands-on mini-project — numbered steps he does himself (typing > pasting)
4. Homework (۲–۳ items), ending with one open security question
5. Gate line: «هر وقت تموم شد بگو *درس N تموم*»

Next lesson opens by answering the previous homework's security question.

## State files (read at session start when resuming)
- Plan: `/data/workspace/course_7day.md` (full curriculum)
- Progress checklist: `/data/workspace/course_progress.md` — tick boxes after each lesson,
  log date under گزارش درس. Backup copy of curriculum in `references/` of this skill.

## Pause/Resume protocol
REZA interrupts mid-flow with quick commands (`BACKUP`, `BACKUP LIST`, side questions).
Handle them, then stop — do NOT auto-resume the course. Resume only on his word
(«ادامه بده» / «درس بعدی»), picking up from the progress file.

## Active course
۷ روزه: امنیت جامع AI + پایه وب + Vibe Coding (روز۱=پایه وب/DevTools … روز۷=انتشار امن+اسکیل‌ها).
Lesson 1 (پایه وب) delivered 2026-08-25.
