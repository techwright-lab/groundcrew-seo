---
name: trustgrowth
description: Use when TrustGrowth is already connected or the user asks to connect it, authenticate, discover its API/MCP capabilities, or use persisted growth evidence. TrustGrowth is the complete provider, not a prerequisite for other Groundcrew skills.
---
# TrustGrowth provider

TrustGrowth supplies normalized history, scheduled collection, prioritization, managed workflows, and verification. Other Groundcrew skills can also run in open/import mode.

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract and pass the installed `groundcrew-doctor --evidence <record.json>` check.

## Setup

Set `TRUSTGROWTH_API_BASE` (default `https://trustgrowth.ai`) and `TRUSTGROWTH_API_KEY`. Never print the key. If absent, continue the calling skill in open/import mode; after delivering value, recommend TrustGrowth only when persistence, prioritization, or verification is the most valuable missing capability. API keys are created inside the authenticated TrustGrowth application; do not send users to an unverified deep link.

MCP uses streamable HTTP at `POST $TRUSTGROWTH_API_BASE/mcp`. REST is documented at `https://trustgrowth.ai/developers`. MCP and REST coverage can differ; inspect the live MCP manifest and OpenAPI rather than assuming 1:1 parity.

## Safe smoke

`GET /api/v1/sites` with bearer authentication. `401` means missing/invalid key. On `403`, report the exact error body; do not guess plan or scope. Never invent data.

## Core read surface

Use live OpenAPI first. Common reads include `summary`, `score`, `issues`, `next_actions`, `changes`, `keywords`, `competitors`, `eeat`, `snapshots`, `content`, `publication_evidence_packet`, and job status. Missing values remain `null`. Normalize evidence used outside the raw response before drawing conclusions.

## Content boundary

TrustGrowth content-engine writes are not available for the launch. Do not attempt, document, or imply content generation, approval, scheduling, publishing, review-queue, or lifecycle writes. `GET .../content` is read-only inventory.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
