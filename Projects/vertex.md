---
title: "vertex — one local 3D app (build · repair · simulate)"
date: 2026-10-24
tags:
  - rea
  - project/vertex
  - status/active
source: "https://heyvector.co/"
repo: "https://github.com/juwpegatron/projects"
---

# vertex (Vertex)

> One local, offline, zero-dependency **3D app**: build parts and export 3D files
> (STL/OBJ/glTF/3MF/DXF), repair broken models and plan whole assemblies in **any**
> 3D software, and run **deterministic simulations**.

## Why one app
`/rea` ran twice on the same target **Vector** (`https://heyvector.co/`): first as a
*complement* (**Part Lab** — a parametric part builder) and then as the *better
version* (**Chase** — a universal 3D copilot). They converged on the same idea, so
they are now **unified as Vertex** and the old names are retired.

## What it does
| Area | Capability |
| --- | --- |
| **Build** | Parametric geometry: numeric params + additive solids (box/cylinder/cone/sphere/prism) + subtractive holes. Pure, deterministic (`identical input ⇒ byte-identical output`). Presets: bracket, flange, spacer. |
| **Export** | Real 3D files: **STL (ascii + binary), OBJ, glTF 2.0, 3MF (store-only ZIP), DXF**. |
| **Repair** | Reads a host-agnostic ModelReport → typed **Diagnosis** (failed fillets, broken references, dangling/circular dependencies, failed mates) + ordered upstream-first **Repair plan**. |
| **Assemble** | **Assembly plan** (base part + insert/mate steps + structural checks), review-gated. |
| **Simulate** | Deterministic: kinematic assembly motion (25-sample trace), mass properties (volume/mass/centroid), clearance/interference (AABB). No FEM/CFD — labelled estimate. |
| **Universal** | **20 adapters**: Fusion, SOLIDWORKS, FreeCAD, Blender, Onshape, Rhino, SketchUp, Inventor, AutoCAD, CATIA, Solid Edge, Creo, Maya + open formats STEP/STL/OBJ/glTF/3MF/DXF + simulated. |

Dark, Vector-style UI (near-black, single periwinkle accent) with a live canvas 3D
viewport (auto-fit; draws solids **and holes**; blue dimension leaders; crop marks).

## Verification
- Engine **121** self-tests (build/export/simulate/adapters); `verify_bridge` all pass; `verify_static` 37.
- Independent engine↔bridge **parity**: adapter registry, `buildMesh`, `simulate` match.
- Gate: `build_site` ✓ · `check_site` **PASSED** (34 HTML, 0 errors) · `run_all_tests` **18/18**.
- Visual: headless-browser screenshot → fitted isometric plate, 5 holes, grid, "80.0 mm" dimension.

## Sync
- GitHub: https://github.com/juwpegatron/projects @ `main` (commit `0b7eea7`).
- Portfolio: https://juwpegatron.github.io/portfolio/
- Legacy notes redirected: [[Part Lab]] → Vertex, [[chase]] → Vertex, [[gantry]] → Vertex.

## Honest constraint
Host adapters (Fusion/SOLIDWORKS/etc.) are import-safe **templates, unverified
against a real CAD host** (no seat/SDK here); the tested path is the deterministic
simulation core. Follow-up: port Part Lab's saved-parts library (SQLite CRUD) into
Vertex, and add a real boolean/CSG kernel so holes are cut from exported manifolds.
