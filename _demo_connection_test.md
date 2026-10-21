---
created: 2026-10-21
updated: 2026-10-21
type: demo
tags: [demo, connection-test, opencode]
---

# Obsidian Connection Demo

Created by the OpenCode agent (Sisyphus). Vault: `C:\Users\juwen_lie\Documents\Obsidian Vault`.

## Current status (verified)

| Capability | Method | Status |
|---|---|---|
| Read/write vault files | filesystem | working |
| Local REST API | `https://127.0.0.1:27124` | working |
| API auth | 64-char key (plugin `data.json`) | working |
| Native create | `PUT /vault/{path}` | working (204) |
| Native read | `GET /vault/{path}` | working (200) |
| Native search | `POST /search/simple/` | working (200) |
| MCP endpoint | `/mcp/` initialize | working |
| OpenCode MCP client | `opencode.json` registration | pending user paste |

This note was last written **through the REST API**, not to the filesystem.

## Links

- Native-API proof: [[_api_native_demo]]
- Back to [[Welcome]]

#connection-test #opencode
