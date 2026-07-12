---
name: site-audit
description: Use when the user wants a current site audit, technical SEO findings, Core Web Vitals interpretation, or a fresh TrustGrowth audit when connected. Supports connected, imported, and public/local evidence.
---
# Site Audit

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources

- Connected: TrustGrowth `issues`, `summary`, and `changes`; manual audit only when explicitly requested and plan/scope allow it.
- Import: validated crawl/audit evidence supplied by the user.
- Open: inspect publicly observable pages and local artifacts. Report observations, not a proprietary score or historical trend.

Direct GSC and PageSpeed Insights API connectors are deferred for launch. Do not improvise them. User-provided exports may be imported.

## Interpret

Group pages by root cause. Separate directly observed facts from interpretation. Report critical findings first, externally owned/informational findings as context, and missing data as unknown. Do not estimate score impact. Treat one-off lab performance results as low confidence unless corroborated; distinguish lab from field evidence.

## Manual TrustGrowth audit

`POST /api/v1/sites/{slug}/trigger_audit` requires write scope and explicit user intent. Poll the returned job through the documented job endpoint. Respect `403` and `429`; do not retry blindly.

Hand safe code-fixable findings to `fix-my-site`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
