---
tags: [feature, orbis, peers, guide, onboarding, affiliate]
date: 2026-10-23
repo: https://github.com/juwpegatron/projects
commit: 4925fcc
---

# Orbis + Peers — Guide, First-Run Tour, Affiliate Recommendations

## What shipped (commit `4925fcc`)
Both **Orbis** and **Peers**, on **desktop and mobile**, gained:

- **Guide view** — overview of the app + a detailed "How it works" walkthrough + a **Start tour** button.
- **First-run interactive tour** — an overlay with progress dots and **Skip / Back / Continue / Done** (Esc = skip). Auto-launches on first visit, once-only via a localStorage flag, and is re-runnable from the Guide.
- **Recommendations with affiliate links** — a single config array `GUIDE_RECOMMENDATIONS`; links render with `target="_blank" rel="sponsored noopener"` and an affiliate disclosure line.

## Keys & config
| App | Tour flag | Recommendations array |
| --- | --- | --- |
| Orbis | `orbis_guide_tour_v1` | `GUIDE_RECOMMENDATIONS` (Notion, Raycast, Superhuman, Obsidian, Readwise, Proton Mail) |
| Peers | `peers_guide_tour_v1` | `GUIDE_RECOMMENDATIONS` (6 items) |

## To swap in real affiliate links
Edit the single `GUIDE_RECOMMENDATIONS` array in each build's HTML:
- Orbis: `apps/orbis/web/app.html`, `app-mobile.html`
- Peers: `apps/peers/web/index.html`, `mobile.html`

Replace the placeholder URLs with your real affiliate tags.

## Notes
- Caught + fixed a **real JS syntax error** before merge (unescaped apostrophes in Orbis' Guide i18n strings) — server-only tests don't load the JS, so it was verified with `node --check` on all four builds.
- Also landed: Orbis **Learn** section, House of Articles **Ledger** + data-integrity drift guard, and the `/rea` skill wired to `/update`.

## Links
- Repo: https://github.com/juwpegatron/projects
- Commit: `4925fcc`
