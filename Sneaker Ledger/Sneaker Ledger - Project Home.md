---
tags: [project, sneakers, data-integrity, provenance, rea]
app: sneaker-ledger
repo: https://github.com/juwpegatron/projects
path: apps/sneaker-ledger
status: shipped
created: 2026-10-22
target: apps/house-of-articles
---

# Sneaker Ledger — Project Home

A data-integrity and price-provenance console that **complements** [[House of Articles]]
by making its catalog verifiable. Built with the `/rea` pipeline
(REA → improve → project → sync) as the first full end-to-end validation run.

## What it is
Offline-first, static, zero-dependency (Python stdlib) web app. Per SKU it shows a
price waterfall (cost → retail → market), fee-aware resale economics, a provenance/
confidence badge, and a data-integrity panel. No login, no network.

## Why — risks it mitigates (from the REA analysis)
| House of Articles risk | Sneaker Ledger answer |
| --- | --- |
| R1 Catalog duplicated across builds → drift | Single source of truth `catalog.json` + automated integrity checks |
| R2 Synthetic/verified-less prices | `provenance {source, confidence, observed_at}` per colorway |
| R3 (legal) working-name risk | original name, no borrowed branding |
| R4 No fee-aware resale math | editable marketplace-fee net-profit / ROI calculator |
| R5 (ops, accepted) static-only | offline-first, still static |

## Contents
- 4 brands · 8 colorways (Basketball / Running / HYROX / Lifestyle)
- Price waterfall, fee-aware net profit, confidence badges
- Integrity panel: duplicate SKUs, cross-field mismatches, missing parts/provenance
- Optional stdlib API: `/api/health`, `/api/catalog`, `/api/sku/{id}`, `/api/integrity`

## Run / test
```powershell
python apps/sneaker-ledger/server/server.py
python apps/sneaker-ledger/tests/test_data_schema.py
python apps/sneaker-ledger/tests/test_static_integrity.py
python apps/sneaker-ledger/tests/verify_api.py
```

## Links
- Repo: https://github.com/juwpegatron/projects (`apps/sneaker-ledger`)
- Commit: `4decc6b`
- Analysis: `~/.config/opencode/skills/rea` (Phase-1 artifact: `%TEMP%\rea\hoa-manual.json`)
