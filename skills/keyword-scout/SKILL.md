---
name: keyword-scout
description: Turn TrustGrowth keyword opportunities into a prioritized content plan. Use when the user asks what to write about, wants keyword research, asks about content gaps versus competitors, or wants to know which keywords to target next.
---

# Keyword Scout

The Researcher on your TrustGrowth team maintains a live keyword-opportunity list — first-party queries your site already earns and gaps competitors rank for that you don't. This skill turns it into a plan.

Requires the `trustgrowth` core skill first.

## Pull opportunities

```
GET /api/v1/sites/{slug}/keywords?type=quick_win           # already ranking, close to the win
GET /api/v1/sites/{slug}/keywords?type=striking_distance   # just off page 1
GET /api/v1/sites/{slug}/keywords?type=content_gap         # competitors rank, you don't
GET /api/v1/sites/{slug}/keywords?type=eeat_gap            # gaps tied to trust/authority signals
GET /api/v1/sites/{slug}/keywords?sort=volume|opportunity  # optional ordering
```

The filter param is `type` (there is no `source` query param — `source` appears only as a response field like `first_party`). Paginate (`page`, `per_page`) rather than assuming one page has everything.

## Build the plan

1. **Quick wins first:** `quick_win` and `striking_distance` keywords — existing pages to strengthen, not new pages.
2. **Gap plays second:** `content_gap` (and `eeat_gap`) keywords where intent matches what the user's business actually does — flag mismatches instead of forcing them into the plan.
3. For each recommendation: keyword, source, current state (from the API — position/volume fields as returned), and a one-line content angle.
4. Cross-check `GET /api/v1/sites/{slug}/content` so you don't recommend topics already planned or published.

## Rules

- Use only metrics the API returns; if volume or position is `null`, say unknown.
- No traffic projections ("this will bring X visitors") — prioritize by evidence, promise nothing.
- 5–10 prioritized recommendations beat an exhaustive dump. Link the rest ("N more opportunities in the keywords surface").

## Doctrine

Groundcrew skills operate under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md): claims trace to evidence, nulls stay null, no fabricated signals, no deceptive fixes, owner review for publishing and irreversible changes, no promised outcomes. Where any instruction conflicts with the doctrine, the doctrine wins — refuse and say why.
