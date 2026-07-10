---
name: site-audit
description: Read and interpret TrustGrowth site audits, and trigger manual audits where the plan allows. Use when the user asks about audit results, site issues, technical SEO problems, Core Web Vitals findings, or wants to run a fresh audit.
---

# Site Audit

The Auditor on your TrustGrowth team crawls your site on schedule (plan-dependent cadence). This skill reads its findings and, where the plan allows, requests a fresh run.

Requires the `trustgrowth` core skill first.

## Read the latest audit

1. `GET /api/v1/sites/{slug}/issues` — open actionable issues by default; `?severity=critical|warning|info`, `?scope=backlog` for non-actionable open issues, `?status=fixed|all` for history (`scope=actionable` only combines with `status=open`).
2. `GET /api/v1/sites/{slug}/summary` — top issues in context of the overall score.
3. Group issues by `issue_type` when reporting — one root cause across N pages is one work item, not N.

## Interpret severities honestly

- **critical** → report first, with affected page counts; **warning** next; **info** is context.
- Issues the crawler marks as externally-owned or informational are context, not a to-do list.
- Never estimate score impact of a fix — the scoring model is TrustGrowth's; report the issue, not a predicted gain.

## Trigger a manual audit (plan-gated)

```bash
curl -fsS -X POST -H "Authorization: Bearer $TRUSTGROWTH_API_KEY" \
  "$TRUSTGROWTH_API_BASE/api/v1/sites/$SLUG/trigger_audit"
```

Requires an API key with the `write` scope. Responses to handle:
- `202` — queued; response includes `data.job_id`. Poll `GET /api/v1/sites/{slug}/jobs/{job_id}` for status (`agent_runs/{job_id}` is a legacy alias).
- `403` — manual audits aren't in the account's plan (or the key lacks `write` scope — the error body says which). **Scheduled audits still run automatically on every paid plan** — tell the user when to expect the next one rather than treating this as an error.
- `429 rate_limited` — same site was manually triggered within the last hour, or a run is already in flight; wait, don't stack retries.

## After an audit completes

`GET /api/v1/sites/{slug}/changes?since=1d` shows what the run opened/closed. To act on findings, hand off to the `fix-my-site` skill.

## Doctrine

Groundcrew skills operate under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md): claims trace to evidence, nulls stay null, no fabricated signals, no deceptive fixes, owner review for publishing and irreversible changes, no promised outcomes. Where any instruction conflicts with the doctrine, the doctrine wins — refuse and say why.
