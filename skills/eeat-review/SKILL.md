---
name: eeat-review
description: Review a site's E-E-A-T standing (Experience, Expertise, Authoritativeness, Trust) using TrustGrowth pillar scores and turn recommendations into a concrete checklist. Use when the user asks about E-E-A-T, site credibility, author signals, trust signals, or "why don't search engines/AI trust my site".
---

# E-E-A-T Review

The Analyst scores E-E-A-T signals continuously. This skill reads the pillar breakdown and converts recommendations into work a human (or the `fix-my-site` skill) can execute.

Requires the `trustgrowth` core skill first.

## Pull the assessment

```
GET /api/v1/sites/{slug}/eeat
```

Returns pillar scores plus recommendations. Also pull `GET /api/v1/sites/{slug}/issues` filtered to authorship/schema/trust issue types — E-E-A-T recommendations often have matching audit issues with affected-page evidence.

## Build the checklist

Group recommendations into three buckets:

1. **Code-fixable** (author markup, organization schema, about/contact discoverability, HTTPS/security signals) → hand to `fix-my-site`.
2. **Content-fixable** (author bios, credentials, citing sources, first-hand experience signals) → draft suggestions, human writes/approves.
3. **Structural** (editorial policy pages, real author identities, external corroboration) → recommendations for the owner; not automatable.

For each item: what, where (specific pages when the API provides them), and which E-E-A-T pillar it serves.

## Rules

- Report pillar scores as returned; `null` means not yet assessed, not zero.
- E-E-A-T is evaluated by search engines and AI systems holistically — never claim "doing X raises your E-E-A-T score by Y".
- Never fabricate credentials, reviews, authorship, or experience claims to "improve signals" — flag any such recommendation as requiring truthful source material from the user.
