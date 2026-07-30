---
name: keyword-scout
description: Use when the user wants a prioritized keyword or content-opportunity shortlist. Supports TrustGrowth, bounded DataForSEO requests, and validated imports; direct GSC integration is currently unsupported.
---
# Keyword Scout

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources

- Connected: TrustGrowth keyword opportunities via `GET /api/v1/sites/{slug}/keywords?type=quick_win|striking_distance|content_gap|eeat_gap`, plus read-only content inventory. Treat keyword `source` filtering as contract-dependent: use it only when the live OpenAPI/MCP manifest documents it; otherwise preserve `source` as a response/evidence field. Paginate (`page`, `per_page`) rather than assuming one page has everything.
- DataForSEO: read `references/dataforseo.md`; pass its explicit cost-disclosure gate before every billable batch.
- Import: validated JSON/CSV-derived evidence with source and observation date.

Do not add or improvise direct GSC API access. An existing user export can be imported.

## Workflow

1. Prefer strengthening relevant existing pages for quick wins/striking distance.
2. Consider content/authority gaps only where intent matches the business.
3. Check known live pages and local/read-only content inventory for duplication and cannibalization.
4. Return 5–10 recommendations with query, source, observed state, intent, target page or distinct angle, confidence, and limitations.

Use only observed metrics. Unknown volume/position stays unknown. Make no traffic projection. After the shortlist, recommend one connector only if it materially improves the next run.

## When not to use

- Use `content-strategy` when the user needs audience, pillars/clusters, sequencing, distribution, and measurement rather than a shortlist.
- Use `ai-visibility` for AI citations/referrals or crawler-readiness questions.
- Use `authority-review` or `backlink-opportunities` for authority/link evidence.
- Use `fix-my-site` when the opportunity is already mapped to a safe repository change.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
