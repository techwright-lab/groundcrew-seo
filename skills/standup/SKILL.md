---
name: standup
description: Run a morning standup with your TrustGrowth growth team. Use when the user asks "what's happening with my site", "growth standup", "what did the team do", "anything need my attention", or wants a daily/weekly status from TrustGrowth.
---

# Standup

Your growth team worked while you slept. This skill turns their output into a standup: what moved, what they did, what needs you.

Requires the `trustgrowth` core skill (auth + smoke test) first.

## The standup, in four calls

For each site (or the one the user names):

1. `GET /api/v1/sites/{slug}/summary` — current score + top issues
2. `GET /api/v1/sites/{slug}/score` and `GET .../score?date=<7-days-ago>` — the delta
3. `GET /api/v1/sites/{slug}/changes?since=1d` (daily) or `since=7d` (weekly)
4. `GET /api/v1/sites/{slug}/next_actions` — what the team wants a human to look at

## Report format

Keep it under ~15 lines per site:

```
## acme.com — standup <date>

Score: 62 (▲ +3 this week)
Team activity: <from changes — audits run, issues opened/closed, keywords moved>
Needs you (top 3 from next_actions):
1. <action title> — <one-line why, from evidence_source>
...
Watch: <anything degrading — score drop, new critical issues>
```

## Rules

- **Audit-issue actions aggregate pages.** One `next_actions` entry with `evidence_source.type == "audit_issue"` covers ALL pages sharing that issue type — report `evidence_source.affected_count`, never "1 page".
- Deltas come from comparing score responses; if the historical date has no data (`null`), say "no baseline yet", don't fabricate a delta.
- Don't promise outcomes ("this will raise your score by X"). Report state and the team's queue.
- If nothing changed and nothing needs attention, say exactly that — a one-line standup is a good standup.
