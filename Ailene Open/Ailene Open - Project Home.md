---
tags: [project, ai, learning, open-source, bilingual, rea, dashboard]
app: ailene-open
repo: https://github.com/juwpegatron/projects
path: apps/ailene-open
status: shipped
created: 2026-10-22
updated: 2026-10-22
---

# Ailene Open — Project Home

An **independent, open, vendor-neutral** reinterpretation of [ailene.id](https://ailene.id).
Not affiliated with ailene.id. Built with the `/rea` skill (REA → improve → project → sync).

## What it is
Offline-first, bilingual (ID/EN) AI-learning web app. Teaches AI *concepts*, not one vendor.
Zero dependencies (Python stdlib), static-first, works from `file://`, no login.

## Why — risk mitigation vs ailene.id
| ailene.id risk | Ailene Open answer |
| --- | --- |
| Claude vendor lock-in | Vendor-neutral prompts w/ per-model adaptations (Claude / GPT / Gemini / Local) |
| Gated advanced content | Fully open spine `data/curriculum.json` — all levels free |
| Login + no offline | No-login progress in `localStorage`; works offline from `file://` |
| Unverifiable claims | Every lesson ships cited `sources[]` + a self-run safety/eval checklist |
| Indonesia-only | Bilingual ID / EN |
| New-brand trust | Open source, no signup, transparent provenance |

## Dashboard (added 2026-10-22)
Modeled on the ailene.id in-app dashboard (inspiration only; original copy). The
dashboard is now the default landing view and adds:
- Greeting + overall progress (X/Y lessons, %)
- **Passport** 4-level progression — all levels FREE (vs the reference's locked tiers)
- Per-level & per-module progress bars
- **7-day learning streak** widget (local activity dates)
- Rotating **tip of the day**
- Quick actions to Quiz / Prompt Library / Glossary / Safety
- New **Glossary** view (bilingual terms) and per-lesson **Notes** (localStorage)

localStorage keys: `ailene_open_v1` (progress), `ailene_open_streak_v1`, `ailene_open_notes_v1`.

## Contents
- 4 levels · 8 modules · 9 lessons (bilingual, cited) + 10 tips + 10 glossary terms
- 12-question "AI Type" quiz (5 personas)
- Vendor-neutral prompt library · 8-point safety/eval checklist

## Run / test
```powershell
python apps/ailene-open/server/server.py
python apps/ailene-open/tests/test_data_schema.py
python apps/ailene-open/tests/test_static_integrity.py
python apps/ailene-open/tests/verify_api.py
```

## Links
- Repo: https://github.com/juwpegatron/projects (`apps/ailene-open`)
- Commit: `4decc6b`
- Reference: https://www.ailene.id/dashboard
- Skill: `/rea` (`~/.config/opencode/skills/rea/`)
