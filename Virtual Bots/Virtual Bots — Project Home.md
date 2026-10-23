---
id: virtual-bots-000
app: virtual-bots
type: spec
status: building
date: 2026-10-23
tags: [project, ai, agents, bots, dashboard, app]
links: ["[[Update Log]]"]
---

# Virtual Bots — Project Home

> **Command and watch your AI bots working in a live office — an installable App, a Web dashboard and a Mobile view, offline-first.**

`Virtual Bots` is the **bots office**: a dashboard where your virtual bots (AI agents) sit at their desks, report status, stream their tool activity, and take new goals. A small bridge backend connects to a live agent server; when no backend is reachable the UI runs a clearly-labelled **simulation**, so the whole thing is demoable offline. The static builds ship as **App + Web + Mobile**.

## At a glance

| | |
|---|---|
| Web (live) | https://juwpegatron.github.io/projects/virtual-bots/ |
| App (installable PWA) | https://juwpegatron.github.io/projects/virtual-bots/app.html |
| Mobile | https://juwpegatron.github.io/projects/virtual-bots/mobile.html |
| Portfolio card | https://juwpegatron.github.io/portfolio/ (Projects -> Virtual Bots) |
| Catalog (all apps) | https://juwpegatron.github.io/projects/ |
| Source (static builds) | `apps/virtual-bots/web/` (index.html web + app.html install + mobile.html) |
| Origin project | `agents-dashboard/` (bridge `server.py` + dashboard `index.html`, contract `CONTRACT.md`) |

## What it does

- **Bots roster** — the office of virtual bots: name, role, live status dot (idle / working / done) and progress.
- **Live activity** — a normalized event feed (`phase: start | tool | progress | text | end | error`).
- **Command** — send a goal to a bot; the bridge forwards it to the live agent server and relays the transcript and todo-derived progress.
- **Live / Sim modes** — attaches to an already-running agent server when present; otherwise a scripted simulation. The UI always shows which mode it is (no AI theatre).

## The three versions

| Version | File | Notes |
|---|---|---|
| App | `web/app.html` | Install landing + PWA (`manifest.webmanifest`, `sw.js`) — installs to home screen / desktop. |
| Web | `web/index.html` | The full bots-office dashboard (3D office), runs in sim mode when offline. |
| Mobile | `web/mobile.html` | Phone-first roster + activity + command view. |

## How it is hosted

Static front-ends live in `apps/virtual-bots/web/` and are deployed to GitHub Pages by `scripts/build_site.py` (registered in the app catalog). The web build is `index.html` (the office dashboard); when it cannot reach a backend it falls back to **sim** mode, so a purely static host still works.

## Bridge contract (origin)

The bridge is Python-standard-library-only and proxies the local agent server (`CONTRACT.md` is the fixed interface):

- `GET /api/health` — bridge + upstream status (`{ ok, mode: "live"|"sim", opencode: {...} }`).
- `GET /api/agents`, `GET /api/sessions` — roster + recent sessions.
- `GET /api/events` — SSE normalized event stream.
- `POST /api/command` — `{ goal, agent, session_id? }` -> dispatch a goal.
- `POST /api/permission` — reply to a permission request.

## Source of truth

- Static app: `apps/virtual-bots/web/` (this note is a mirror of the repo).
- Origin dashboard + bridge: `agents-dashboard/` (bridge `server.py`, dashboard `index.html`).
