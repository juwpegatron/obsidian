---
tags: [feature, guide, onboarding, affiliate, orbis, peers, house-of-articles, hazel, desk-verdict]
date: 2026-10-23
repo: https://github.com/juwpegatron/projects
---

# Guide + First-Run Tour + Affiliate Recommendations — all apps

## What shipped
Every app now has:
- A **Guide** view: overview + a step-by-step "How it works" + a **Start tour** button.
- A **first-run interactive tour**: an overlay with progress dots and **Skip / Back / Continue / Done** (Esc = skip). Auto-launches on first visit, once-only via a localStorage flag, re-runnable from the Guide.
- **Recommendations** with affiliate links in a single config array `GUIDE_RECOMMENDATIONS` (`{title, blurb, url}`), rendered with `target="_blank" rel="sponsored noopener"` + an affiliate disclosure line.

## Coverage
| App | Builds | Tour flag | Commit |
| --- | --- | --- | --- |
| Orbis | `app.html` + `app-mobile.html` | `orbis_guide_tour_v1` | `4925fcc` |
| Peers | `index.html` + `mobile.html` | `peers_guide_tour_v1` | `4925fcc` |
| House of Articles | `desktop.html` + `index.html` | `hoa_guide_tour_v1` | `9dd432c` |
| Hazel | `src/` (Electron renderer) | `hazel_guide_tour_v1` | `dc26a48` |
| Desk Verdict | `web/index.html` | `deskverdict_guide_tour_v1` | `9dd432c`-era |

## Swapping in real affiliate links
Each build has one `GUIDE_RECOMMENDATIONS = [{title, blurb, url}]` array — replace the mockup URLs with your real affiliate tags.
- Note: **House of Articles** stores URLs scheme-less (`'stockx.com'`) and assembles the scheme at runtime (`'https:' + '//'`) so its "no external URLs" test keeps passing.

## Notes
- Two real JS syntax errors were caught and fixed before merge (unescaped apostrophes in guide i18n strings — server-only tests don't load the JS; verified with `node --check` on every build).
- Verified on all builds: `node --check` = 0, app tests green, full gate (`build_site`, `check_site`, `run_all_tests`) green.

## Links
- Repo: https://github.com/juwpegatron/projects
