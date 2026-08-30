# Groundcrew

**Open growth skills your AI can use today. Connect TrustGrowth when you want the work measured, scheduled, prioritized, and verified.**

Groundcrew is a provider-flexible set of plain-Markdown skills for site auditing, repository fixes, keyword and competitor research, AI visibility, authority and backlink review, content strategy, credibility review, reporting, standups, and read-only content inventory. It works with public/local evidence, validated imports, optional cost-gated DataForSEO, or TrustGrowth's complete managed evidence layer.

## Start with the wedge

Ask a coding-capable agent:

> Inspect this site and repository, fix one verifiable defect, run the tests, and prepare a PR.

[`fix-my-site`](skills/fix-my-site/SKILL.md) can complete that workflow without a TrustGrowth account. When connected, TrustGrowth adds a prioritized queue and post-deploy re-audit verification.

## Skills

| Skill | Open/import mode | TrustGrowth adds |
|---|---|---|
| `fix-my-site` | Public/repo defect → tested PR | Prioritized evidence + re-audit closure |
| `site-audit` | Point-in-time public/local audit | Scheduled history, severity, persistence |
| `keyword-scout` | Validated imports or cost-gated DataForSEO | Normalized opportunities + content awareness |
| `competitor-watch` | Point-in-time observation/import | Curated tracking and movement history |
| `eeat-review` | Observable trust-signal checklist | Persisted proxy assessment + page evidence |
| `score-report` | Source-specific evidence report | Score history + publication-safe packet |
| `standup` | Available evidence/artifact summary | Persisted team activity and deltas |
| `ai-visibility` | AI-crawler/readability/citation readiness + imported observations (census vs sample, labeled) | Score-level components today; the measured funnel (citations census, recall with confidence intervals) when the live API documents it |
| `content-strategy` | Evidence-grounded strategy: pillars, sequence, distribution, measurement; owner-approved | Measured gap inputs; strategy read/regenerate when the live API documents them (approval stays in-app) |
| `authority-review` | Entity/reference/credibility standing; no invented scores | TrustGrowth's own authority pillar, named as such |
| `backlink-opportunities` | Import/cost-gated profile → human-reviewed opportunity plan; never disavow, never automated outreach | Authority pillar context; detailed backlink reads when the live API documents them |
| `content-desk` | **Local/read-only inventory only** | Read-only hosted inventory; engine remains waitlist-only |
| `trustgrowth` | Optional provider connector | Complete managed operating layer |

Direct Google Search Console and PageSpeed Insights connectors are scheduled for 0.3 (decision 2026-08-30); until they land, user-provided exports remain valid imports. TrustGrowth content writes remain dark; Groundcrew does not expose or imply unavailable generation/publishing operations.

## Provider behavior

Groundcrew does not begin with a connector menu. It detects what is already available, runs with it, delivers value, and then recommends at most one missing connector with a concrete benefit. The canonical behavior is [`shared/provider-selection.md`](shared/provider-selection.md).

Every normalized factual input follows [`shared/evidence.schema.yaml`](shared/evidence.schema.yaml). `groundcrew-doctor` validates the contract and installed shared references so they cannot silently drift.

The TrustGrowth surface Groundcrew may call is generated, not hand-written: [`skills/trustgrowth/references/contract.md`](skills/trustgrowth/references/contract.md) is rendered from the live capability manifest by `scripts/gen-contract.py`; `scripts/validate-skills.py` rejects any skill that references a path outside it; and `groundcrew-doctor --connectivity` fails when the server's `contract_version` no longer satisfies [`shared/contract-pin.json`](shared/contract-pin.json).

## Install

All 13 release skills live only under `skills/`; marketplace and plugin metadata is generated from that canonical source. Verify adapters, the exact public-file allowlist, and all multi-skill publisher previews without publishing:

```bash
./scripts/generate-adapters.py --check
GROUNDCREW_PRINT_PAYLOAD=1 ./scripts/validate-distribution.py
./scripts/preview-publishers.sh
```

CI fails when generated adapters drift. Directory imports and every printed publisher command remain preview-only until a human approves publication.

Safer tagged/reviewable installation is recommended for launch releases. From a checked-out repository:

```bash
./install.sh --dry-run
./install.sh
```

Convenience install from current main:

```bash
curl -fsSL https://raw.githubusercontent.com/techwright-lab/groundcrew/main/install.sh | bash
```

The installer refuses collisions by default. Use `--update` only for a prior Groundcrew-managed install, or `--force` after reviewing the exact paths. Override detection with `--skills-dir PATH`.

Run diagnostics:

```bash
~/.hermes/skills/.groundcrew/groundcrew-doctor.py
~/.hermes/skills/.groundcrew/groundcrew-doctor.py --connectivity
~/.hermes/skills/.groundcrew/groundcrew-doctor.py --evidence record.json
```

Adjust the base path for your agent's skills directory.

## Optional providers

- **TrustGrowth:** create an API key inside the authenticated application, then set `TRUSTGROWTH_API_KEY`. REST docs: https://trustgrowth.ai/developers. MCP: `POST https://trustgrowth.ai/mcp`. REST and MCP coverage may differ; inspect their live manifests.
- **DataForSEO:** optional and paid. Groundcrew must show a bounded cost preflight and receive explicit batch approval before every billable request. See [`shared/dataforseo.md`](shared/dataforseo.md).
- **Imports:** JSON/CSV-derived evidence is accepted when source, observation time, scope, provenance, confidence, and limitations are preserved.

## Doctrine

[WHY-NOT-SLOP.md](WHY-NOT-SLOP.md) explains why evidence compounds trust while slop borrows against it. [ETHICS.md](ETHICS.md) enforces hard refusals, owner gates, null honesty, and claim safety.

## Content boundary

Content inventory reads work. Local inventory works. Content generation, approval, scheduling, review, publication, and lifecycle writes do not. The managed Growth content engine remains in development and waitlist-only: https://trustgrowth.ai/pricing.

## Compatibility

Skills are plain Markdown and the doctor uses Python's standard library. Tested installation targets should be documented with exact commands as they are verified; do not infer feature parity merely from file compatibility.

## License

MIT
