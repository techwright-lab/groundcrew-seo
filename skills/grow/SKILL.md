---
name: grow
description: Use when the user wants the full Groundcrew growth loop on a site — survey, fix, verify, report — as one command, or one named phase of it (`--phase survey|fix|verify|report`).
---
# Grow

Read `references/provider-selection.md` before choosing a source and `references/reporting.md` before classifying audit work. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Report output follows `references/reporting.md`.

Grow orchestrates other Groundcrew skills; it adds no data source of its own. Invoked without `--phase` it runs the loop in order and stops at every gate. `--phase` runs exactly one phase and stops.

## The loop

1. **survey** — establish current state: `site-audit` for defects, `ai-visibility` for answer-engine reach, `keyword-scout` for the keyword picture at the current tier. Output one prioritized finding list, each finding tagged with its owning skill and decision state: leave unchanged, investigate, propose for owner review, or eligible for an already authorized implementation. Preserve complete remediation metadata before batching; severity orders review but does not decide the action.
2. **fix** — hand only confirmed, authorized, code-fixable findings to `fix-my-site`, one branch per root cause. Keep optional advice and valid no-change decisions out of the repair queue. Missing guidance, unknown applicability, missing context, and anything irreversible or outward-facing are investigated or proposed, never applied — the loop stops and waits for the owner. Skipped findings are recorded as skipped with the reason.
3. **verify** — prove what changed. Open mode: re-crawl the touched pages and diff actual rendered responses against the survey observations and preservation constraints. Connected: `POST /api/v1/sites/{slug}/trigger_audit` (write scope, explicit user intent; on `403` say when the next scheduled audit runs, on `429` wait — never stack retries), poll `GET /api/v1/sites/{slug}/jobs/{job_id}`, then read `GET /api/v1/sites/{slug}/issues?status=fixed` for closures. A fix nothing re-observed stays "applied, unverified".
4. **report** — package the cycle with the owning report skill (`weekly-report` for the period, `audit-report` for findings depth). Verdict rules come from `references/reporting.md`; a cycle whose fixes are unverified cannot say SHIP.

## Audit remediation invariants

- **Intake:** Retain `detection_policy_version` and the complete `remediation` object before batching; split only between issues and keep every preservation, avoid, no-change, and verification constraint.
- **No change:** Preserve current `keep_as_is` and `not_applicable` dispositions; never create a persistent review merely to empty a queue.
- **Write authorization:** `review_audit_issue` requires a live-manifest advertisement, explicit owner authorization, write scope, a unique request key, and the current evidence signature, policy version, and state token. Read-only compatibility mode blocks it and every other write.
- **Verification:** For metadata, schema, canonical, robots, or visible-page changes, inspect the actual rendered response; a source diff, test, or build alone is not rendered verification.

On an older same-major TrustGrowth contract, run only advertised `GET` operations in read-only feature-detected mode. Missing remediation remains investigate/propose, and `trigger_audit`, `review_audit_issue`, and every other write are blocked; use open-mode rendered verification instead.

## Gates

Between phases the loop presents what it found, what it intends next, and stops when the next phase would write anywhere outside a local branch. One full pass is one cycle; the loop never self-restarts — the user starts the next cycle.

## When not to use

- One question about one surface → the owning skill directly (`site-audit`, `keyword-scout`, `ai-visibility`, `competitor-watch`).
- Only a document, no action → the report skills.
- Content production or publishing → `content-strategy` / `content-desk`; the loop does not write or publish content.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
