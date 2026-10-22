---
tags: [project, ai, learning, open-source, bilingual, rea]
app: ailene-open
repo: https://github.com/juwpegatron/projects
path: apps/ailene-open
status: shipped
created: 2026-10-22
---

# Ailene Open — Project Home

An **independent, open, vendor-neutral** reinterpretation of [ailene.id](https://ailene.id).
Not affiliated with ailene.id. Built with the `/rea` skill (REA → improve → project → sync).

## What it is
Offline-first, bilingual (ID/EN) AI-learning web app. Teaches AI *concepts*, not one vendor.
Zero dependencies (Python stdlib), static-first, works from `file://`.

## Why — risk mitigation vs ailene.id
| ailene.id risk | Ailene Open answer |
| --- | --- |
| Claude vendor lock-in | Vendor-neutral prompts with per-model adaptations (Claude / GPT / Gemini / Local) |
| Gated advanced content | Fully open spine `data/curriculum.json` — all levels free |
| Login + no offline | No-login progress in `localStorage`; works offline from `file://` |
| Unverifiable claims | Every lesson ships cited `sources[]` + a self-run safety/eval checklist |
| Indonesia-only | Bilingual ID / EN |
| New-brand trust | Open source, no signup, transparent provenance |

## Contents
- 4 levels · 8 modules · 9 lessons (bilingual, cited)
- 12-question "AI Type" quiz (5 personas: Professor / Builder / Detective / Guardian / All-Rounder)
- Vendor-neutral prompt library (core prompt + per-model adaptations)
- 8-point AI safety & evaluation checklist
- No-login progress tracking in `localStorage` (`ailene_open_v1`)

## Run
```powershell
python apps/ailene-open/server/server.py     # optional API + serves web/
```
Or just open `apps/ailene-open/web/index.html` (fully offline).

## Tests
```powershell
python apps/ailene-open/tests/test_data_schema.py
python apps/ailene-open/tests/test_static_integrity.py
python apps/ailene-open/tests/verify_api.py
```

## Links
- Repo: https://github.com/juwpegatron/projects (`apps/ailene-open`)
- Commit: `70c85c0`
- Skill: `/rea` (`~/.config/opencode/skills/rea/`)
