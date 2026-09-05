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

## Surface

The callable surface is `references/contract.md`, generated from the live capability manifest (`GET /api/v1/capabilities/v1`) by `scripts/gen-contract.py`. It lists every read and write path, its query params, the MCP tool with the same name, scopes, and error codes. Never hand-write an endpoint; if it is not in that file, do not call it. Site paths take the `slug` from `GET /api/v1/sites`.

Prefer the MCP tool name (for example `get_site_score`, `list_site_issues`, `trigger_audit`) when an MCP client is available; use the REST path in the same row otherwise. Both run the same code.

## Contract rules

1. Only use endpoints in the live OpenAPI. Never invent endpoints or fields.
2. `X-RateLimit-*` and `Retry-After` headers are authoritative; `meta.rate_limit` in the body mirrors them for convenience. On `429`, wait for `Retry-After`, then retry once.
3. `404` on a slug usually means a typo or a site the key can't access — re-list sites.
4. Report numbers as they are. Missing data comes back as `null`, never zero — don't convert nulls to zeros in summaries.
5. Every response carries `meta.contract_version`. `groundcrew-doctor.py --connectivity` fails when the server's version does not satisfy `shared/contract-pin.json` (same major, at least the pinned minor.patch). Do not work around a failed pin check.

## Audit remediation compatibility

Issue consumers read the complete `remediation` object and follow the decision contract in `references/reporting.md`. Feature-detect that field on each response: older servers may omit it even when an issues endpoint exists. Missing guidance, `guidance_available: false`, unknown applicability, and absent required context mean investigate with explicit local evidence and, when justified, prepare a proposal for owner review. They never authorize a blanket repair or allow legacy severity to replace current policy.

If the generated contract advertises `review_audit_issue`, call it only with explicit authorization to record the authenticated owner's decision. Copy the current evidence signature, policy version, and state token from `remediation.review`, supply a unique request key and reason, and re-read on a stale conflict. Preserve existing valid `keep_as_is` and `not_applicable` decisions; do not create acceptance decisions merely to empty a queue. Audit review remains separate from repair verification, scoring, and content-engine publication approval.

## Content boundary

TrustGrowth content-engine writes are not available for the launch. Do not attempt, document, or imply content generation, approval, scheduling, publishing, review-queue, or lifecycle writes. `GET .../content` is read-only inventory.

## When not to use

This skill connects and reads the provider; it does not do the jobs. Route: audit findings → `site-audit`; implementing fixes → `fix-my-site`; keyword planning → `keyword-scout`; daily digest → `standup`; shareable numbers → `score-report`. If TrustGrowth is not connected and the user has not asked to connect it, stay in the calling skill's open/import mode instead of starting setup.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
