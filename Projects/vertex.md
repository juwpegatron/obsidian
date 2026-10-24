---
title: "vertex — one local 3D app (build · repair · simulate · answers · reverse · drawing · automate)"
date: 2026-10-24
tags:
  - rea
  - project/vertex
  - status/active
source: "https://heyvector.co/"
repo: "https://github.com/juwpegatron/projects"
---

# vertex (Vertex)

> One local, offline, zero-dependency **3D app**. Its visuals mirror
> `heyvector.co` (dark, single-accent, hero + product panel + feature grid +
> numbered steps) — but it does **more**, locally and deterministically.

## What it does
- **Build** — parametric geometry (params + box/cylinder/cone/sphere/prism + holes), pure & deterministic.
- **Export** — **STL (ascii+binary), OBJ, glTF 2.0, 3MF, DXF**.
- **Repair** — ModelReport → typed Diagnosis + upstream-first Repair plan.
- **Assemble** — Assembly plan (base + insert/mate steps + structural checks).
- **Simulate** — kinematic motion, mass properties, clearance/interference.
- **Answers** — ask questions about the design → deterministic answers + evidence (failed features, dependencies, mates, how-to).
- **Reverse** — a point scan → editable parametric CAD (box/cylinder fit).
- **Drawing → CAD** — a drawing spec → a model (extents + holes).
- **Automation** — batch export / pattern / drawing sheets with totals.
- **Guide** — first-run onboarding overlay (auto-opens once, remembered in `localStorage`; reopen via the top-bar **Guide** button or "See how it works"); Esc/backdrop/Got-it to close; full text in `docs/vertex-guide.md`.
- **Universal** — 20 adapters (Fusion, SOLIDWORKS, FreeCAD, Blender, Onshape, Rhino, SketchUp, Inventor, AutoCAD, CATIA, Solid Edge, Creo, Maya + open formats + simulated).

## Why it exists
Vertices mirrors Vector's look and covers Vector's marketed functions (repair,
reverse engineering, drawing-to-CAD, answers/how-do-I, automation, assemblies,
control) — but **better on function**: local (no cloud/account/IP loss),
deterministic (no AI non-determinism), universal (any tool, open formats),
auditable (typed artifacts), and review-gated.

> **Honest constraint:** no CAD host/SDK runs here, so host adapters are
> import-safe templates (unverified against a real host); the tested path is the
> deterministic simulation core. Vertex is **not an AI/LLM** — its "Answers" are
> rule-based and deterministic (the copy was corrected to avoid the false
> "AI copilot" claim).

## Verification
- Engine **165** self-tests; `verify_bridge` all pass; `verify_static` **51** (incl. 6 guide checks across all 3 screens).
- Independent engine↔bridge **parity**: reverse/drawing/automate **identical**; answers match in **kind** (wording differs between the JS engine and the Python bridge — client-side string variance only).
- Gate: `build_site` ✓ · `check_site` **PASSED** (34 HTML, 0 errors) · `run_all_tests` **18/18**.
- Visual: headless screenshot → top bar, hero ("One 3D copilot. For every tool."), product panel, 8 feature cards, numbered steps, footer.

## Sync
- GitHub: https://github.com/juwpegatron/projects @ `main` (commit `649459c`; lineage `6e94994` ← `0b7eea7` ← `52acc15`).
- Portfolio: https://juwpegatron.github.io/portfolio/
- Legacy: [[Part Lab]] / [[chase]] / [[gantry]] all redirect to Vertex.

## Next steps
- Align the bridge's answer **wording** with the engine (cosmetic).
- Port the saved-parts library (SQLite CRUD) from the retired Part Lab.
- Add a real boolean/CSG kernel so holes are cut out of exported manifolds.
