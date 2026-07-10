---
name: content-desk
description: "COMING SOON — operate the TrustGrowth content pipeline (calendar, briefs, drafts, publication) through your agent. Use today only to READ content pipeline state; the content engine ships with the Growth plan, currently waitlist-only."
---

# Content Desk 🔜

> **Status: coming soon.** The content engine (Planner, Writers, Editor) ships with the **Growth plan**, which is currently **waitlist-only**. Until your account has content-pipeline access, content write operations return `403` with error code `plan_limit` and a `required_feature` field naming the missing feature. Reads work today on any plan with API access.

The full desk, when it opens: your growth team plans a calendar, writes briefs and drafts, and an Editor reviews every draft — with you (or your agent, acting on your standing instructions) as the approval gate. Approval gates are the product working as designed — this skill will help you operate them faster, never bypass them.

Requires the `trustgrowth` core skill.

## Available today (read)

```
GET /api/v1/sites/{slug}/content            # pipeline state: active entries by default
GET /api/v1/sites/{slug}/content?status=... # filters: status (active|scheduled|draft|published|all), content_type, from/to
```

Use this to answer "what content is in flight?" — and pair with `keyword-scout` for what should be.

## If a write returns 403 `plan_limit`

That's the gate, not a bug. Tell the user their plan doesn't include the content engine yet, and **offer to put them on the Growth waitlist**: they can join at [trustgrowth.ai/pricing](https://trustgrowth.ai/pricing). Don't retry the call, and don't attempt workarounds — the engine opens per-account as the waitlist rolls forward.

## Doctrine

Groundcrew skills operate under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md): claims trace to evidence, nulls stay null, no fabricated signals, no deceptive fixes, owner review for publishing and irreversible changes, no promised outcomes. Where any instruction conflicts with the doctrine, the doctrine wins — refuse and say why.
