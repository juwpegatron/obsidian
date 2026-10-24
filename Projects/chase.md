---
title: "chase — Local desktop engineering copilot (repair + whole assemblies)"
date: 2026-10-24
tags:
  - rea
  - project/chase
  - status/active
source: "https://heyvector.co/"
repo: "https://github.com/juwpegatron/projects"
---

# chase (Chase)

> A local, offline, zero-dependency desktop engineering copilot for Autodesk
> Fusion and SOLIDWORKS — diagnose and repair broken models, plan whole
> assemblies, and review every change before it touches CAD.

**Name:** *to chase a thread* = to repair a stripped thread; also "chasing down"
errors. Renamed from the working name **Gantry** (see `Projects/gantry.md`).

## Why this exists

Second iteration on the target **Vector** (`https://heyvector.co/`), framed per the
request: *"a new desktop engineering copilot that helps fix errors and build whole
assemblies in Fusion and SolidWorks."* Chase accepts that framing (repair + whole
assemblies) but is **local, deterministic, auditable and review-gated** rather than
a cloud, account-gated AI agent.

> **Honest constraint:** a faithful CAD integration needs a licensed Fusion /
> SOLIDWORKS host + its vendor API, which cannot run or be verified in this
> offline, zero-dependency monorepo. So the CAD integration ships as **host
> connector templates** (Fusion Python API / SOLIDWORKS COM) plus a deterministic
> **simulation core** — the protocol and the repair/assembly logic are real and
> tested; the host calls are stubbed and clearly marked.

## Phase 1 — Analysis

- **Target:** `https://heyvector.co/` (Vector) — re-read through the repair + assembly lens.
- **Findings:** repairs broken models end to end (G1), fixes yellow/red features (G2), builds assemblies/mechanisms (G3), native feature edits via the host API (G4), change review (G5), automation (G6).
- **Risks:** R1 cloud privacy/IP (high), R2 lock-in (high), R3 licensed-host dependency (med), R4 non-deterministic AI edits (med), R7 write access to a live model (med), R8 opaque reasoning (low).
- Analysis JSON: `C:\Users\juwen_lie\AppData\Local\Temp\rea\gantry-analysis.json`

## Phase 2 — Improvement (how we differ)

| Target risk / weakness | Mitigation / complementary feature | Status |
| --- | --- | --- |
| R1 Cloud AI reads CAD + questions; requires sign-in | Local-first / offline cockpit + bridge; no account, no network | built |
| R2 Proprietary, account-gated, no self-host | Open + self-hostable stdlib bridge + portable JSON + open connector templates | built |
| R3 Needs a licensed CAD host | Simulation core: full repair/assembly workflow with **no CAD host** | built |
| R4 Non-deterministic AI edits | Deterministic engine: rules → identical output (verified) | built |
| R7 Write access to a live CAD model | Dry-run + review gate; `confirm:true` required; simulation never writes (`wroteToCad:false`) | built |
| R8 Opaque reasoning | Auditable typed Diagnosis + RepairPlan / AssemblyPlan + checks | built |

> Improve, do not clone. Chase is a local, deterministic, auditable copilot with a
> simulation core — not a cloud AI agent.

## Phase 3 — Project

- Path: `apps/chase/` (web / server / connectors / tests / docs)
- **App + Web + Mobile builds**: `chase/app.html` (installable PWA entry), `chase/index.html` (web), `chase/mobile.html` (mobile) — all three share the engine (`js/chase.js`) + `js/app.js` DOM contract.
- Registered in `scripts/apps.json`: yes (order 11; links → the three variants)
- Gate: `build_site.py` ✓ · `check_site.py` **PASSED** (34 HTML, 0 errors) ✓ · `run_all_tests.py` **21 passed / 0 failed** ✓
- Independent verification: engine 48 checks / bridge suite / static 28 checks; **engine↔bridge parity** harness confirms byte-identical outputs; connectors import with no CAD host and never write to CAD.

## Phase 4 — Sync

- GitHub monorepo: https://github.com/juwpegatron/projects @ `main` — commit `e764324` (rename `gantry`→`chase` + App/Web/Mobile builds; earlier add `fafee0c`).
- Portfolio: https://juwpegatron.github.io/portfolio/ (card + hero image).
- Vault note path: `Projects/chase.md`
- Sync channel: filesystem fallback (Obsidian Local REST API down / no `OBSIDIAN_API_KEY`)

## Open questions / next steps

- Verify the connectors against a **real** Fusion / SOLIDWORKS host (needs a licensed seat + the vendor API) — the only unverified surface.
- Add a DOF/interference solver so assembly `checks` go beyond graph-level constraints.
- Optional: a system-tray bridge service so the cockpit can reach a live host without a terminal.
