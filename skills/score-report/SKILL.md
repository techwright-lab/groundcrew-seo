---
name: score-report
description: Assemble a shareable, claim-safe growth report from TrustGrowth score history, snapshots, and evidence. Use when the user wants a weekly/monthly report, a stakeholder update, a client report, or asks "how is my site doing" in a form meant to be shared.
---

# Score Report

Turn your growth team's evidence into a report you can send to a stakeholder or client without a lawyer reading it first.

Requires the `trustgrowth` core skill first.

## Gather evidence

1. `GET /api/v1/sites/{slug}/score` and historical points (`?date=`) for the reporting window
2. `GET /api/v1/sites/{slug}/snapshots?from=...&to=...&granularity=weekly` — trend series
3. `GET /api/v1/sites/{slug}/changes?since=30d` — what the team did
4. `GET /api/v1/sites/{slug}/publication_evidence_packet` — the operator-safe score snapshot and publication-safety flags. **When this packet and raw score data disagree, the packet wins for anything shared externally.**

## Report structure

```
# {Site} growth report — {period}

TrustGrowth Score: {current} ({delta} over period)
Pillar movement: <pillars that changed, from score breakdown>
Work completed: <audits, issues closed, content shipped — from changes>
Trend: <2-3 sentences from snapshots — direction, not prediction>
Open items: <top next_actions, framed as team queue>
Data notes: <any nulls/gaps, stated plainly>
```

## Claim-safety rules (non-negotiable)

- **Current-state framing only.** "Score moved from 58 to 62" ✅. "On track to reach 70" ❌. No projections, no guarantees, no attributing business outcomes (revenue, leads) to the score.
- Missing data is reported as missing — never smoothed, interpolated, or zero-filled.
- Respect the evidence packet's publication-safety flags; if it marks something as not operator-safe to share, leave it out.
- Every number in the report must trace to an API response from this run. If you didn't fetch it, don't state it.
