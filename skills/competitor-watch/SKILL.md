---
name: competitor-watch
description: Track and interpret competitor movement using TrustGrowth's competitor intelligence. Use when the user asks how they compare to competitors, whether a competitor changed something, or wants a periodic competitive readout.
---

# Competitor Watch

The Researcher tracks the competitor set for each site. This skill reads that intelligence and reports movement without hype.

Requires the `trustgrowth` core skill first.

## Read the competitive picture

1. `GET /api/v1/sites/{slug}/competitors` — the tracked set + comparison data.
2. `GET /api/v1/sites/{slug}/keywords?source=competitor_gap` — where they rank and you don't.
3. `GET /api/v1/sites/{slug}/changes?since=7d` — includes shifts the team observed.

## Report format

```
## Competitive readout — {site} vs tracked set

Position: <where the site stands on the comparison metrics the API returns>
Moved this period: <competitor>: <observed change> (evidence: <field/endpoint>)
Exposed gaps: <top 2-3 competitor_gap keywords with intent fit>
No change: <competitors with nothing notable — one line total>
```

## Rules

- The tracked set is curated by TrustGrowth (platform giants are filtered out) — if the user asks about a domain not in the set, say it isn't tracked rather than improvising from general knowledge.
- Distinguish *observed data* (from the API) from *interpretation* (your read of it) — label each.
- Competitor pages/content are facts to report; never generate attack copy or claims about a competitor's business. Comparisons stay metric-level.

## Doctrine

Groundcrew skills operate under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md): claims trace to evidence, nulls stay null, no fabricated signals, no deceptive fixes, owner review for publishing and irreversible changes, no promised outcomes. Where any instruction conflicts with the doctrine, the doctrine wins — refuse and say why.
