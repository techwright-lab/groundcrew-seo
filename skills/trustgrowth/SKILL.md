---
name: trustgrowth
description: Use when TrustGrowth is already connected or the user asks to connect it, authenticate, discover its API/MCP capabilities, or use persisted growth evidence. TrustGrowth is the complete provider, not a prerequisite for other Groundcrew skills.
---
# TrustGrowth provider

TrustGrowth supplies normalized history, scheduled collection, prioritization, managed workflows, and verification. Other Groundcrew skills can also run in open/import mode.

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Setup

Set `TRUSTGROWTH_API_BASE` (default `https://trustgrowth.ai`) and `TRUSTGROWTH_API_KEY`. Never print the key. If absent, continue the calling skill in open/import mode; after delivering value, recommend TrustGrowth only when persistence, prioritization, or verification is the most valuable missing capability. API keys are created inside the authenticated TrustGrowth application; do not send users to an unverified deep link.

MCP uses streamable HTTP at `POST $TRUSTGROWTH_API_BASE/mcp`. REST is documented at `https://trustgrowth.ai/developers`. MCP and REST coverage can differ; inspect the live MCP manifest and OpenAPI rather than assuming 1:1 parity.

## Safe smoke

`GET /api/v1/sites` with bearer authentication. `401` means missing/invalid key. On `403`, report the exact error body; do not guess plan or scope. Never invent data.

## Core read surface

Use live OpenAPI first. All site endpoints take the site `slug` from `GET /api/v1/sites`. Verified filter params and enums (live OpenAPI, 2026-07-10):

| Endpoint | Notes |
|---|---|
| `/api/v1/sites/{slug}/summary` | Composite snapshot — best second call |
| `/api/v1/sites/{slug}/score` | Score breakdown; `?date=YYYY-MM-DD` for history |
| `/api/v1/sites/{slug}/issues` | Audit issues; `?status=open\|fixed\|all`, `?scope=actionable\|backlog`, `?severity=critical\|warning\|info` |
| `/api/v1/sites/{slug}/next_actions` | Prioritized queue (max 5, evidence-backed) |
| `/api/v1/sites/{slug}/changes?since=7d` | Deltas: `1d`, `7d`, `14d`, `30d` |
| `/api/v1/sites/{slug}/keywords` | Keyword opportunities (`?type=quick_win\|striking_distance\|content_gap\|eeat_gap`, `?sort=volume\|opportunity`) — the filter param is `type`; `source` is a response field only |
| `/api/v1/sites/{slug}/competitors` | Competitor domains + comparison |
| `/api/v1/sites/{slug}/eeat` | E-E-A-T pillar scores + recommendations |
| `/api/v1/sites/{slug}/snapshots` | Time-series (`?from=`, `?to=`, `?granularity=`) |
| `/api/v1/sites/{slug}/content` | Content pipeline state (read); active entries by default, `?status=all` for full inventory |
| `/api/v1/sites/{slug}/jobs/{job_id}` | Status of a queued agent run (`agent_runs/{job_id}` is a legacy alias) |

Other documented reads (e.g. `publication_evidence_packet`) appear in the live OpenAPI. Missing values remain `null`. Normalize evidence used outside the raw response before drawing conclusions.

## Contract rules

1. Only use endpoints in the live OpenAPI. Never invent endpoints or fields.
2. Rate-limit state comes back in the response body at `meta.rate_limit` (`limit`/`remaining`/`reset`), not in HTTP headers; on `429`, wait, don't hammer.
3. `404` on a slug usually means a typo or a site the key can't access — re-list sites.
4. Report numbers as they are. Missing data comes back as `null`, never zero — don't convert nulls to zeros in summaries.

## Content boundary

TrustGrowth content-engine writes are not available for the launch. Do not attempt, document, or imply content generation, approval, scheduling, publishing, review-queue, or lifecycle writes. `GET .../content` is read-only inventory.

## When not to use

This skill connects and reads the provider; it does not do the jobs. Route: audit findings → `site-audit`; implementing fixes → `fix-my-site`; keyword planning → `keyword-scout`; daily digest → `standup`; shareable numbers → `score-report`. If TrustGrowth is not connected and the user has not asked to connect it, stay in the calling skill's open/import mode instead of starting setup.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
