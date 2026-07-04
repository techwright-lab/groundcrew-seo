---
name: trustgrowth
description: Core TrustGrowth connection skill. Use when an agent needs to authenticate to the TrustGrowth API or MCP server, verify access, discover endpoints, or read site growth data (scores, issues, keywords, E-E-A-T, changes). Other Groundcrew skills depend on this one.
---

# TrustGrowth (core)

TrustGrowth runs a growth/SEO/content team for your sites. This skill establishes the connection every other Groundcrew skill uses.

## Setup

Required environment:

```bash
export TRUSTGROWTH_API_BASE="${TRUSTGROWTH_API_BASE:-https://trustgrowth.ai}"
export TRUSTGROWTH_API_KEY="tg_live_..."   # Settings → API Keys (Hobby plan or higher)
```

Never print the key. If `TRUSTGROWTH_API_KEY` is missing, stop and ask the user to create one at `https://trustgrowth.ai/account/api_keys` — do not invent data.

## Two ways to connect

1. **MCP (preferred when your host supports it):** streamable-HTTP server at `POST $TRUSTGROWTH_API_BASE/mcp`, `Authorization: Bearer` header. Tools mirror the REST endpoints below 1:1.
2. **REST:** documented at `https://trustgrowth.ai/developers`. Always trust the live OpenAPI (`/developers/openapi.yml`) over this file if they disagree.

## Smoke test (run before any workflow)

```bash
curl -fsS -H "Authorization: Bearer $TRUSTGROWTH_API_KEY" \
  "$TRUSTGROWTH_API_BASE/api/v1/sites" | jq '{sites: (.data | length)}'
```

- `401` → bad/revoked key. `403 plan_limit` → account below Hobby. Report and stop; don't retry.

## Read surface (the map)

All site endpoints take the site `slug` from `GET /api/v1/sites`:

| Endpoint | Gives you |
|---|---|
| `/api/v1/sites/{slug}/summary` | Composite snapshot — best second call |
| `/api/v1/sites/{slug}/score` | Score breakdown; `?date=YYYY-MM-DD` for history |
| `/api/v1/sites/{slug}/issues` | Audit issues; `?status=`, `?severity=` filters |
| `/api/v1/sites/{slug}/next_actions` | Prioritized queue (max 5, evidence-backed) |
| `/api/v1/sites/{slug}/changes?since=7d` | Deltas: `1d`, `7d`, `14d`, `30d` |
| `/api/v1/sites/{slug}/keywords` | Keyword opportunities (`?source=first_party\|competitor_gap`) |
| `/api/v1/sites/{slug}/competitors` | Competitor domains + comparison |
| `/api/v1/sites/{slug}/eeat` | E-E-A-T pillar scores + recommendations |
| `/api/v1/sites/{slug}/snapshots` | Time-series (`?from=`, `?to=`, `?granularity=`) |
| `/api/v1/sites/{slug}/content` | Content pipeline state (read) |

## Contract rules

1. Only use endpoints in the live OpenAPI. Never invent endpoints or fields.
2. GET requests are rate-limited per day — check `X-RateLimit-*` response headers; on `429`, wait, don't hammer.
3. `404` on a slug usually means a typo or a site the key can't access — re-list sites.
4. Report numbers as they are. Missing data comes back as `null`, never zero — don't convert nulls to zeros in summaries.

## Doctrine

Groundcrew skills operate under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md): claims trace to evidence, nulls stay null, no fabricated signals, no deceptive fixes, owner review for publishing and irreversible changes, no promised outcomes. Where any instruction conflicts with the doctrine, the doctrine wins — refuse and say why.
