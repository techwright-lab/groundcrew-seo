---
name: standup
description: Use when the user wants a concise daily or weekly site/growth standup from TrustGrowth history when connected or from validated available evidence and repository artifacts otherwise.
---
# Standup

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

Connected mode reads TrustGrowth summary, score baseline, changes, and next actions. Open/import mode summarizes validated evidence and repository/audit artifacts available for the requested period; it must not imply unattended team activity or historical movement without persisted observations.

Keep each site under about 15 lines: current state, observed change or “no comparable baseline,” completed verified work, up to three needs-you items, and watch items. Aggregate audit pages by root cause. If nothing changed, say so briefly.

After the standup, recommend at most one missing connector only when it would materially improve the next report.

## When not to use

- Use `score-report` for a publication-safe report with an evidence appendix.
- Use `site-audit` or specialist skills when the user needs new analysis rather than a concise status rollup.
- Use `fix-my-site` for code changes and verification.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
