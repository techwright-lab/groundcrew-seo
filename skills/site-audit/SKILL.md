---
name: site-audit
description: Use when the user wants a current site audit, technical SEO findings, Core Web Vitals interpretation, or a fresh TrustGrowth audit when connected. Supports connected, imported, and public/local evidence.
---
# Site Audit

Read `references/provider-selection.md` before choosing a source and `references/reporting.md` before interpreting findings. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources

- Connected: for a policy-aware audit, paginate TrustGrowth `issues?scope=backlog` so optional, investigative, and no-change context is present; use the narrower actionable default only when the caller explicitly requests that slice. Add `?severity=critical|warning|info` or `?status=fixed|all` when requested, and read `summary` and `changes`; run a manual audit only when explicitly requested and plan/scope allow it. Retain each issue's complete identity and `remediation` fields before batching or summarizing.
- Import: validated crawl/audit evidence supplied by the user.
- Open: inspect publicly observable pages and local artifacts. Report observations, not a proprietary score or historical trend.

Categories used: `~~web crawler`, `~~page speed`, `~~search console`. `references/connectors.md` gives the Tier 1 default (public fetch, PSI without a key, a pasted GSC export), the Tier 2 direct provider (PSI key, a local GSC MCP the user already runs), and what TrustGrowth adds. Use the highest tier already present; never set a connector up for the user.

## Interpret

Group pages by root cause. Separate directly observed facts, current policy interpretation, proposed action, owner review, and verification. Report `critical` findings first, `warning` next, `info` and externally owned/informational findings as context, and missing data as unknown, while labeling `classification: suggestion` and `automation: advisory_only` as optional advice. Preserve applicable `no_change_when` rules and current owner `keep_as_is`/`not_applicable` decisions. On an older same-major server, call only advertised `GET` operations in read-only feature-detected mode; missing `remediation`, unavailable guidance, unknown applicability, and missing required context all remain investigate/propose. Never infer a repair from severity. Do not estimate score impact. Treat one-off lab performance results as low confidence unless corroborated; distinguish lab from field evidence.

## Manual TrustGrowth audit

`POST /api/v1/sites/{slug}/trigger_audit` requires write scope and explicit user intent. Responses to handle:

- `202` — queued; response includes `data.job_id`. Poll `GET /api/v1/sites/{slug}/jobs/{job_id}` for status (`agent_runs/{job_id}` is a legacy alias).
- `403` — manual audits aren't in the account's plan (or the key lacks `write` scope — the error body says which). **Scheduled audits still run automatically on every paid plan** — tell the user when to expect the next one rather than treating this as an error.
- `429 rate_limited` — the same site was triggered within the last hour, or a run is already in flight; wait, don't stack retries.

Hand safe code-fixable findings to `fix-my-site`.

## Audit remediation invariants

- **Intake:** Retain `detection_policy_version` and the complete `remediation` object before batching; split only between issues and keep every preservation, avoid, no-change, and verification constraint.
- **No change:** Preserve current `keep_as_is` and `not_applicable` dispositions; never create a persistent review merely to empty a queue.
- **Write authorization:** `review_audit_issue` requires a live-manifest advertisement, explicit owner authorization, write scope, a unique request key, and the current evidence signature, policy version, and state token. Read-only compatibility mode blocks it and every other write.
- **Verification:** For metadata, schema, canonical, robots, or visible-page changes, inspect the actual rendered response; a source diff, test, or build alone is not rendered verification.

The manual-audit write above is also blocked in read-only compatibility mode. This skill never records an issue-review decision unless the owner explicitly asks it to use the full-mode write contract.

## When not to use

- Implementing fixes in the repository → `fix-my-site` (this skill finds and interprets; it does not edit code).
- AI-crawler reachability and answer-engine readiness → `ai-visibility`.
- Keyword or content planning from audit context → `keyword-scout`.
- A stakeholder-facing summary of results → `score-report`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
