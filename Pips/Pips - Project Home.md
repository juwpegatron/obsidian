---
title: Pips — Project Home
aliases: [Pips, Productivity Widget, The Morning Paper, Pomodoro Widget]
tags: [project, widget, desktop, python, productivity, tkinter, maas]
status: published
created: 2026-10-23
updated: 2026-10-24
source: "[[Update Log]]"
---

# Pips — Project Home

> **"The Morning Paper"** — an always-on-top desktop widget that turns your day into a score.
> Pomodoro timer + soundscapes + live app-usage tracking + daily productivity score + coaching
> + **live MAAS AI-token usage**.

## At a glance

| | |
|---|---|
| Local path | `C:\Users\juwen_lie\Desktop\opencode_project\productivity-widget` |
| GitHub | `juwpegatron/projects` → `apps/pips` (published) |
| Live page | https://juwpegatron.github.io/projects/pips/ |
| Stack | Python 3 · Tkinter GUI · SQLite · standard library only (no third-party deps) |
| Run | `pythonw app.py` (or the **Pips** desktop shortcut / `Launch Widget.bat`) |
| Theme | The same "Morning Paper" newspaper theme as [[Portfolio — Project Home]] |

## Features

- **Pomodoro timer** — work → short break → long break (long break every 4th), auto-start next.
- **Soundscapes** — rain, thunder, brown noise, cafe, crickets, ocean, wind, fireplace, forest (procedurally generated at runtime).
- **Live app-usage tracking** — samples the foreground window ~1/s; tallies minutes per app.
- **Daily productivity score** with a 1–5 star rating; goals, streaks and XP.
- **Hour-of-day focus heatmap**, browsable history log.
- **Coach** — daily AI-style coach + weekly report.
- **Break & health reminders** — stand/stretch/water popups, 20-20-20 eye rest, hydration nudges.
- **AI token usage** — local OpenCode-log ingest (`tokens.py`).
- **MAAS account token usage** *(new, 2026-10-24)* — live daily total, a 7-day trend and a per-model split pulled from the Pegatron AICC **MAAS** gateway (`maas_tokens.py`).

## Structure

| File | Purpose |
|---|---|
| `app.py` | Main widget (Tkinter card + dashboard) |
| `audio.py` | Procedural soundscape generation |
| `tracker.py` / `scoring.py` | Foreground-app sampling + productivity scoring |
| `coach.py` / `diary.py` / `reminders.py` | Coaching, diary sync, break reminders |
| `tokens.py` | AI token-usage ingest (parses the OpenCode log) |
| `maas_tokens.py` | MAAS account token usage (AICC gateway REST API) |
| `daily_email.py` | Optional daily report email |
| `config.example.json` | Sample config — copy to `config.json` |
| `tests/` | Standard-library tests |

## Config & privacy (important)

- `config.json` is **git-ignored** — it holds the recipient email, local paths, settings and (optionally) MAAS credentials. A sanitised **`config.example.json`** is committed instead.
- `data/` (runtime: SQLite DB + generated soundscapes), `logs/`, and `output/` (generated reports) are **git-ignored** — they contain personal usage data.

## Publish status

- **Published** to `juwpegatron/projects` → `apps/pips`.
- **Live showcase page:** https://juwpegatron.github.io/projects/pips/
- Copied into the monorepo's `apps/` folder (per the `apps/<name>/` convention); the original still runs from the Desktop at `opencode_project\productivity-widget`.
- **Renamed** from **Productivity Widget** → **Pips** (2026-10-24); the Desktop, Start Menu and Startup shortcuts are now **Pips.lnk**.

## Links

- Update Log: [[2026-10-23 1026 Default Project]], [[2026-10-23 1045 Default Project]]

## Versions — App / Web / Mobile

- **App** (native desktop) — https://juwpegatron.github.io/projects/pips/
- **Web** — https://juwpegatron.github.io/projects/pips/web.html
- **Mobile** — https://juwpegatron.github.io/projects/pips/mobile.html
