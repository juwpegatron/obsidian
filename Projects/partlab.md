---
title: "partlab — Local, offline-first parametric part builder"
date: 2026-10-24
tags:
  - rea
  - project/partlab
  - status/active
source: "https://heyvector.co/"
repo: "https://github.com/juwpegatron/projects"
---

# partlab (Part Lab)

> Local, offline-first parametric part builder — describe a mechanical part as
> parameters, preview it in 3D and export STL. No account, no cloud, no CAD licence.

## Why this exists

The analysed target **Vector** (`https://heyvector.co/`) is a proprietary,
account-gated **cloud AI copilot** that drives Autodesk Fusion / SOLIDWORKS: it
reads your open CAD document, requires a platform sign-in, and applies model
output to a live CAD model. Part Lab complements it by being **local, open,
deterministic, free and review-gated** — the opposite of every risk Vector carries.

## Phase 1 — Analysis (what we reverse-engineered)

- **Target:** `https://heyvector.co/` (url — Next.js marketing SPA fronting a closed desktop app)
- **Method:** manual (rea-agents@6.7.0 CLI returned no JS-app shape; the product's internals are not shipped in the page)
- **Findings:** in-CAD AI agent (Fusion + SOLIDWORKS), native feature create/edit via the host API, scan→CAD, drawing→CAD, broken-model repair, design Q&A, batch automation, dual-CAD, account-gated install.
- **Risks:** R1 cloud privacy/IP exposure (high), R2 vendor lock-in (high), R3 paid/Windows-locked CAD dependency (med), R4 non-deterministic AI edits (med), R5 unclear data portability (med), R6 no pricing/sign-in gate (low), R7 model writes to a live CAD model (med).
- Analysis JSON: `C:\Users\juwen_lie\AppData\Local\Temp\rea\partlab-analysis.json`

## Phase 2 — Improvement (how we differ)

| Target risk / weakness | Mitigation / complementary feature | Status |
| --- | --- | --- |
| R1 Cloud AI reads your CAD + questions; requires sign-in | Local-first / offline: no account, no network; geometry in the browser or a local stdlib server | built |
| R2 Proprietary, account-gated, no self-host | Open + self-hostable + zero-dependency; portable JSON part definitions | built |
| R3 Paid licensed CAD; SOLIDWORKS Windows-only; no browser path | Runs anywhere: any browser/OS, offline PWA; no CAD seat needed | built |
| R4 Non-deterministic AI edits | Deterministic parametric core: params → exact mesh (verified) | built |
| R5 Unclear data portability | Open export: ASCII STL + portable part JSON | built |
| R6 No pricing; sign-in + download gate | Free & instant: open and build; no pricing, no sign-in | built |
| R7 Model writes to a live CAD model | Human-in-the-loop review gate: preview → confirmed export | built |

> Improve, do not clone. Summary: a standalone, local, deterministic parametric
> part builder — not a Fusion/SOLIDWORKS plugin and not a chat copilot.

## Phase 3 — Project

- Path: `apps/partlab/` (web / server / tests / docs)
- Registered in `scripts/apps.json` (the monorepo's single source of truth consumed by both `build_site.py` and `publish_portfolio.py`): yes
- Gate: `python scripts/build_site.py` ✓ · `python scripts/check_site.py` **PASSED** ✓ · `python scripts/run_all_tests.py` **18 passed / 0 failed** ✓
- Docs: `docs/partlab-spec.md` (frozen interface contract) · `docs/risk-matrix.md`

## Phase 4 — Sync

- GitHub: https://github.com/juwpegatron/projects @ `main` (commit `741d4ed`)
- Vault note path: `Projects/partlab.md`
- Sync channel: filesystem fallback (Obsidian Local REST API was down / no `OBSIDIAN_API_KEY`)

## Open questions / next steps

- Add a real CSG boolean kernel so holes are cut out of the exported STL manifold (currently holes are analytic subtractive features; see residual risk in the risk matrix).
- Generate a `partlab-hero.svg` card asset for `publish_portfolio.py` (the `apps.json` entry references it; no card image exists yet in the portfolio repo).
- Optional: expose the renderer's `exportPNG()` in the UI as a "share preview" action.
