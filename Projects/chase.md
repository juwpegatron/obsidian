---
title: "chase — universal 3D engineering copilot (v2)"
date: 2026-10-24
tags:
  - rea
  - project/chase
  - status/active
source: "https://heyvector.co/"
repo: "https://github.com/juwpegatron/projects"
---

# chase (Chase) — v2

> A local, offline, zero-dependency **universal 3D engineering copilot**: repair
> broken models and plan whole assemblies in **any** 3D software, **generate 3D
> files** (STL/OBJ/glTF/3MF/DXF) and run **deterministic simulations**.

**Name:** *to chase a thread* = repair a stripped thread; also "chasing down"
errors. (Renamed from the working name **Gantry** → `Projects/gantry.md`.)

## v2 — what changed

| Capability | What it does |
| --- | --- |
| **Universal adapters** | A registry of **20** adapters (Fusion, SOLIDWORKS, FreeCAD, Blender, Onshape, Rhino, SketchUp, Inventor, AutoCAD, CATIA, Solid Edge, Creo, Maya + open formats STEP/STL/OBJ/glTF/3MF/DXF + simulated) — one ModelReport in, many tools out. |
| **3D file generation** | `buildMesh(buildSpec)` builds geometry from parameters/primitives; exports **STL (ascii+binary), OBJ, glTF 2.0, 3MF (store-only ZIP), DXF**. |
| **Deterministic simulation** | Kinematic assembly motion (25-sample trace), mass properties (volume/mass/centroid), clearance/interference (AABB). No FEM/CFD — clearly labelled estimate. |
| **Dark Vector-style UI + live viewport** | Near-black premium theme (mirrors Vector's design language, improved), 4 workspaces (Repair · Assembly · Build · Simulate), and a hand-rolled canvas 3D viewport that auto-fits meshes and draws solids **and holes**. |

## Why it exists

Second iteration on **Vector** (`https://heyvector.co/`). Vector is a cloud,
account-gated AI copilot for Fusion/SOLIDWORKS. Chase complements it by being
**local, deterministic, auditable, review-gated** — and now **universal** (any 3D
software) with **local generation + simulation**.

> **Honest constraint:** no CAD host / SDK / licence runs here, so host adapters
> ship as import-safe templates (`connectors/adapters/`) with a deterministic
> simulation core; the connectors are unverified against a real host.

## Verification

- Engine: **121** self-tests (build/export/simulate/adapters). `verify_bridge`: all pass. `verify_static`: 37 checks.
- **Independent engine↔bridge parity**: adapter registry, `buildMesh`, and `simulate` match semantically.
- Gate: `build_site` ✓ · `check_site` **PASSED** (34 HTML, 0 errors) · `run_all_tests` **21/21**.
- Visual: headless-browser screenshot confirms a fitted isometric plate with 5 holes, dark grid, crop marks, "80.0 mm" dimension.

## Sync

- GitHub monorepo: https://github.com/juwpegatron/projects @ `main` (commit `52acc15`; prior `e764324`, `2ea46ac`).
- Portfolio: https://juwpegatron.github.io/portfolio/
- Vault note path: `Projects/chase.md`
- Sync channel: filesystem fallback (Obsidian REST down / no `OBSIDIAN_API_KEY`).

## Open questions / next steps

- Verify the adapters against a **real** host (needs a licensed seat + vendor API) — the only unverified surface.
- Add a real boolean (CSG) kernel so holes are cut out of exported STL/3MF manifolds.
- DOF/interference solver beyond AABB; optional FEM/CFD estimates.
