---
name: audit-report
description: Use when the user wants audit findings turned into a stakeholder-ready document — severities, page counts, first-seen/fixed history — as a Markdown or CSV deliverable rather than a working diagnosis.
---
# Audit Report

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Output follows `references/reporting.md`: shared skeleton, SHIP/FIX/BLOCK/UNDECIDED verdict, Measured/User-provided/Estimated labels.

## Sources

Categories: `~~web crawler`, `~~page speed` (`references/connectors.md`).

- Tier 1 (open): findings from public crawl of the site's pages; observations only, no proprietary score.
- Tier 2: add Core Web Vitals via `~~page speed`; keep lab and field results labeled apart.
- Connected (TrustGrowth): paginate `GET /api/v1/sites/{slug}/issues` (open actionable by default; `?scope=backlog` for full policy context, `?severity=`, `?status=fixed|all` for history) with first-seen and fixed timestamps, complete remediation metadata, plus `GET /api/v1/sites/{slug}/summary` for totals.

## Shape

Group findings by root cause, not by page; give each group a severity, classification, remediation decision state, affected-page count, and one example URL. Order: critical, warning, info, externally owned, while keeping suggestions visibly optional. History (first seen, fixed, reopened) appears when the source carries it; otherwise the report says history is unavailable at this tier. Apply the policy-aware verdict rules in `references/reporting.md`: an open critical finding forces FIX only when current evidence and applicable guidance support a repair; missing or unavailable guidance and unknown applicability produce UNDECIDED; optional advice and valid no-change decisions do not force FIX.

Deliverable: write the report as a `.md` file, and a `.csv` of the findings table when the user asks for one; hand back the paths.

## When not to use

- Finding and interpreting issues interactively → `site-audit`; this skill packages, it does not diagnose.
- Implementing the fixes → `fix-my-site`.
- A broader periodic status beyond audit findings → `weekly-report` or `score-report`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
