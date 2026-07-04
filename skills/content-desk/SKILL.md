---
name: content-desk
description: "COMING SOON — operate the TrustGrowth content pipeline: review the calendar, approve briefs and drafts, and record publications through your agent. Use today only to READ content pipeline state; write operations are rolling out."
---

# Content Desk 🔜

> **Status: coming soon.** The content pipeline (Planner, Writers, Editor) is rolling out to customer plans. Write operations below return `403` with a `coming_soon` hint until your account has content-pipeline access. Reads work today.

The full desk, when it opens: your growth team plans a calendar, writes briefs and drafts, and an Editor reviews every draft — with you (or your agent, acting on your standing instructions) as the approval gate.

Requires the `trustgrowth` core skill and an API key with the `write` scope.

## Available today (read)

```
GET /api/v1/sites/{slug}/content            # pipeline state: planned, drafted, reviewed, published
GET /api/v1/sites/{slug}/content?status=... # filters: status, content_type, from/to
```

Use this to answer "what content is in flight?" — and pair with `keyword-scout` for what should be.

## The desk workflow (rolling out)

1. `POST .../approve_strategy` — approve the pending strategy; calendar generation starts
2. `POST .../content/{entry_uid}/approve_brief` / `reject_brief` — gate briefs
3. `POST .../content/{entry_uid}/approve_draft` — approve an Editor-reviewed draft
4. `POST .../content/{entry_uid}/publish_draft` — prepare the publication package (**this packages, it does not publish**)
5. Review-queue approval, then `POST .../content/{entry_uid}/record_publication` — the actual publish + record step

Approval gates are the product working as designed — this skill will help you operate them faster, never bypass them. Claim-risk governance on packages stays mandatory.

## Want in?

Content pipeline access ships with the Growth plan rollout — waitlist at [trustgrowth.ai/pricing](https://trustgrowth.ai/pricing).
