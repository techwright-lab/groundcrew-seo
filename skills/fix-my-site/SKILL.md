---
name: fix-my-site
description: Use when a coding-capable agent should find and fix real site defects in the user's repository, from TrustGrowth evidence when connected or from public/local inspection otherwise. Groundcrew's flagship open workflow.
---
# Fix My Site

The wedge: find a real defect, map it to code, implement a focused fix, verify it, and prepare a PR. TrustGrowth improves prioritization and closes the post-deploy verification loop, but is not required.

Read `references/provider-selection.md` before choosing a source and `references/reporting.md` before interpreting or acting on an audit issue. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## 1. Build the queue

Categories: `~~web crawler` and `~~page speed` for open-mode evidence (`references/connectors.md`); connected mode uses TrustGrowth `next_actions` and `issues`.

- Connected: read TrustGrowth `next_actions`, then paginate `issues?scope=backlog` for the queue behind them. Consume each issue's complete `remediation`; filter or order by current severity only after retaining its policy metadata. An item in `next_actions`, an open issue, or a legacy `critical` value does not authorize a repair.
- Import: validate supplied audit/crawl evidence.
- Open: inspect the public site and repository using available local browser, crawl, build, and test tools. Record directly observed defects; do not assign a TrustGrowth score.

Group affected pages by root cause. Verify every finding against the current site or code before editing.

Classify each finding as leave unchanged, investigate, propose for owner review, or eligible for an already authorized implementation. Preserve current `keep_as_is` and `not_applicable` review dispositions. Advice marked `advisory_only`, length-only suggestions, unknown applicability, missing context, and unavailable or absent guidance do not enter the implementation queue. On an older server without `remediation`, investigate with explicit local evidence and prepare a bounded proposal; do not infer a generic fix from issue type or severity.

## 2. Map findings to this codebase

Discover repository guidance and conventions first. Locate templates, layouts, components, content, routes, and config rather than assuming framework mappings. Carry every issue's `preserve`, `avoid`, `no_change_when`, and `verification` constraints into the implementation plan, including when the queue is split into batches. Content judgment, canonical targets, robots/noindex, redirect behavior, authorship, dates, and schema applicability require explicit owner confirmation and truthful evidence.

## 3. Fix and verify

One root cause should produce one focused change across affected pages. Do not add shared title truncators, character padding, bulk metadata rewrites, invented authors or dates, unnecessary schema, or reverse deliberate crawler choices. Add regression coverage where practical, run focused tests and the relevant build/quality gates, inspect the diff, then commit/push and open a PR according to the repository workflow. Never push directly to the default branch unless explicitly allowed.

Verification follows the issue's current `remediation.verification`. For metadata, schema, canonical, robots, and visible-page changes, inspect the actual rendered response in a browser or fetched HTML after the change. A source diff, test, or build does not by itself prove the rendered outcome. Preserve a complete clear authored title exactly; for a missing title, derive a contextual proposal from the page's visible purpose and existing brand composition, then wait for owner authorization before applying it.

Report three distinct states:

- **locally verified** — tests/build pass;
- **deployed** — change is live;
- **audit-verified** — a post-deploy observation shows the defect closed.

Do not collapse these into “resolved.” Connected mode may trigger or await a TrustGrowth re-audit. Open mode explains the remaining verification gap.

## Completion

Return findings with evidence, changed files, exact verification output, PR/patch location, unresolved needs-human items, and—after the result—at most one connector recommendation.

## When not to use

- No repository access → stay in `site-audit` and report findings instead of guessing at code.
- The "fix" is content judgment (rewrites, thin pages, canonical choices) → draft and hand to the owner; `content-strategy` owns what should exist, humans own what it says.
- Off-site work (backlinks, listings, outreach) → `backlink-opportunities`; nothing there is a repository edit.
- Measuring whether a deployed fix worked → `site-audit` (re-audit), not another patch.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
