---
name: content-desk
description: Use for a read-only local or TrustGrowth content inventory. TrustGrowth content generation, approval, scheduling, publication, review, and lifecycle writes remain unavailable and waitlist-only.
---
# Content Desk — inventory only

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract and pass the installed `groundcrew-doctor --evidence <record.json>` check.

## Available launch behavior

- Connected: `GET /api/v1/sites/{slug}/content` for read-only pipeline inventory.
- Open: enumerate local content files/records and report observable metadata such as path, title, date, status when explicitly present, and obvious duplicates or missing fields.
- Import: inventory validated supplied records.

Do not generate drafts, approve, schedule, publish, mutate lifecycle state, call undocumented content-write tools, or imply that TrustGrowth's content engine is available. Do not infer editorial status from filenames when it is not explicit.

Return counts by observed status/type, stale or incomplete records, duplicates, provenance/limitations, and a concise needs-human list. After delivering the inventory, the only product note allowed is that managed content automation remains on the Growth waitlist at `https://trustgrowth.ai/pricing`.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
