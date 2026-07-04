---
name: fix-my-site
description: Close the loop between TrustGrowth audit findings and the user's actual codebase. Use when the user says "fix the issues TrustGrowth found", "improve my score", "fix my SEO issues", or wants a coding agent (Claude Code, Cursor) to implement audit fixes in their repo. Flagship Groundcrew skill — requires a coding-capable agent with access to the site's source code.
---

# Fix My Site

TrustGrowth's Auditor finds the problems. You (a coding agent) fix them. The next audit verifies. No dashboard closes this loop — you do.

Requires the `trustgrowth` core skill, plus read/write access to the repository that builds the user's site.

## The loop

### 1. Pull the work queue

- `GET /api/v1/sites/{slug}/next_actions` — the team's prioritized top 5.
- `GET /api/v1/sites/{slug}/issues?severity=critical` then `high` — the full backlog behind them.

For `evidence_source.type == "audit_issue"` actions: `evidence_source.pages[]` lists up to 10 affected URLs and `affected_count` the true total. The full page list lives in `/issues`.

### 2. Map findings to code

For each issue type, locate where it lives in THIS codebase before editing anything — templates, layouts, components, config. Typical mappings (verify, don't assume):

| Finding | Usually lives in |
|---|---|
| Missing/duplicate meta descriptions, titles | layout head, per-page frontmatter/props, SEO component |
| Missing structured data (author, article, org) | JSON-LD partials/components, CMS templates |
| Missing alt text | content files, image components |
| Broken internal links / redirect chains | content, routing config, redirect maps |
| Core Web Vitals (LCP, INP, CLS) | image loading, font strategy, JS bundles, layout shift sources |
| Missing canonical / OG tags | head template |
| Thin or orphaned pages | content + internal-link structure |

### 3. Fix like an engineer, not a checklist

- One issue type = one focused change (commit/PR) across all affected pages — fixes are usually template-level, not page-by-page.
- Follow the repo's existing conventions; run its tests/build before declaring anything fixed.
- If a "fix" requires content judgment (rewriting thin pages, choosing canonical targets), draft and ask the user — don't silently invent copy.
- Skip issues you can't safely map to code; report them as needs-human instead of guessing.

### 4. Verify

- After deploy, request a fresh crawl via the `site-audit` skill (`trigger_audit` where the plan allows; otherwise note the next scheduled audit).
- Later, `GET /api/v1/sites/{slug}/changes?since=7d` shows which issues the Auditor closed.
- Report honestly: "fixed in code, pending re-audit" ≠ "resolved". Never claim a score will improve by a specific amount.

## Boundaries

- Never commit directly to the default branch unless the user's workflow says to; prefer a PR.
- Don't touch robots.txt, redirects, or noindex rules without explicitly confirming intent — these can deindex a site.
- This skill reads TrustGrowth and writes to the user's repo. It never writes to TrustGrowth.
