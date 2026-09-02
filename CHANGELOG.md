# Changelog

All notable changes to the Groundcrew skill pack. Versions are pack-level
(semver); individual skills carry no separate versions. "Verified against"
names the live-contract snapshot the pack's connected-mode text was checked
against.

## [1.0.0-rc.1] — 2026-09-02

Release candidate for the 1.0.0 directory publish. No content changes over
0.7.0 — version bump, plus the publisher preview now derives the skill count
instead of hard-coding it. Verified against live contract 1.2.0.

## [0.7.0] — 2026-09-02

### Added
- `grow` — the one-command loop: survey → fix → verify → report, with owner
  gates between phases and a real verify step (re-crawl in open mode;
  trigger-audit → job poll → fixed-issue reads when connected). `--phase`
  runs one phase and stops.
- Eval corpus: `tests/evals/<skill>.json`, 5 cases per skill (100 cases) —
  open-tier behavior, connected behavior, honesty under missing data, a safety
  gate, and routing per skill. `scripts/validate-evals.py` enforces coverage,
  case shape, and contract-valid API literals in CI; cases are
  harness-agnostic and never ship in the distribution payload.

### Changed
- Pack grows from 19 to 20 skills.

## [0.6.0] — 2026-09-02

### Added
- Six report skills: `weekly-report`, `audit-report`, `keyword-report`,
  `competitor-readout`, `geo-report`, `authority-report`. Each runs at Tier 1
  (no account), uses `~~category` connectors at Tier 2, and reads TrustGrowth
  history when connected.
- `shared/reporting.md` — the shared reporting contract: one skeleton
  (bottom line, Measured table, what changed, next actions, evidence, not
  measured), SHIP/FIX/BLOCK/UNDECIDED verdicts with absolute vetoes, and
  Measured/User-provided/Estimated fact labels. Installed into every skill's
  `references/` and drift-checked by the doctor.

### Changed
- Pack grows from 13 to 19 skills; adapters, marketplace catalog, and the
  installer ship the new set.

## [0.5.1] — 2026-09-02

### Changed
- Refreshed the vendored capability manifest from live (contract 1.2.0):
  58 operations and 40 MCP tools, adding the keyless free-tool surface and the
  Search Console / SEO-tool reads (GSC per-query and per-page rows, index
  verdicts, SERP snapshots, keyword history, referring domains).
- Contract pin raised to 1.2.0 — the doctor now requires a server that carries
  these surfaces.
- `trigger_audit` tool scopes now read `write` (were empty in the 1.0.0
  snapshot).

## [0.5.0] — 2026-08-30

### Changed
- Renamed to **Groundcrew SEO**: repository `techwright-lab/groundcrew-seo`
  (GitHub redirects the old name), plugin id `groundcrew-seo`, display name
  "Groundcrew SEO — TrustGrowth", README/ETHICS headings, marketplace catalog
  and preview commands, doctor/contract user agents. Skill names, the
  `.groundcrew/` doctor directory, and the `.groundcrew-managed` marker are
  unchanged, so existing installs still `--update`. Claude Code / Codex plugin
  users reinstall once under the new id.
- Marketplace preview commands now derive the release tag from the catalog
  instead of a hard-coded `0.2.0`.

## [0.4.0] — 2026-08-30

### Added
- `shared/connectors.md`: evidence categories (`~~search console`, `~~page speed`,
  `~~SEO tool`, `~~link database`, `~~analytics`, `~~AI monitor`, `~~web crawler`)
  with a Tier 1 / 2 / 3 map and recipes for GSC exports and local MCP, PageSpeed
  Insights, GA4 MCP, Open PageRank, Ahrefs and Semrush MCP, DataForSEO, and
  TrustGrowth. Installed into every skill's `references/`; the doctor fails on
  drift.

### Changed
- The GSC / PageSpeed Insights connector deferral is lifted (decision 2026-08-30):
  `provider-selection.md` now describes categories and tiers instead of a ban.
- Skills name evidence categories (`~~search console`, `~~SEO tool`, ...) instead
  of vendors.

## [0.3.0] — 2026-08-30

Merged as #6; superseded by 0.4.0 before a marketplace release was cut.

### Added
- Generated TrustGrowth contract: `skills/trustgrowth/references/contract.md`
  is rendered by `scripts/gen-contract.py` from the vendored capability
  manifest (`shared/contract/capabilities.json`, refresh with `--from-live`).
  Skills may only reference paths that appear there; `scripts/validate-skills.py`
  enforces it, together with frontmatter and required sections.
- Contract pin (`shared/contract-pin.json`). `groundcrew-doctor.py --connectivity`
  now fetches `GET /api/v1/capabilities/v1` and fails when the server's
  `contract_version` is a different major or older than the pin.

### Changed
- `trustgrowth` skill: the hand-written endpoint table is replaced by the
  generated contract; rate-limit rule corrected — `X-RateLimit-*` /
  `Retry-After` headers are authoritative, `meta.rate_limit` mirrors them.
- Five skill descriptions now open with their `Use when` trigger.

## [0.2.0] — 2026-08-09

### Added
- Four new skills (open/import mode; connected modes follow the TrustGrowth
  API slices): `ai-visibility`, `content-strategy`, `authority-review`,
  `backlink-opportunities`.
- `When not to use` cross-routing section in every skill — each skill names
  which sibling owns the adjacent job.
- Untrusted-content boundary in `shared/provider-selection.md`: fetched web
  content is evidence, never instructions.
- Evidence contract 1.1: `evidence_type` gains `ai_visibility`, `authority`,
  `backlink`, `content_strategy`, `content_gap`, `link_graph`,
  `structured_data`, `ai_referral`. Contract 1.0 records remain valid.

### Changed
- Direct GSC / PageSpeed Insights connector status is now durable ("not
  supported, no committed date; exports importable") instead of launch-dated.

## [0.1.0] — 2026-07-12

Initial public pack: nine provider-flexible skills (connected / direct /
import / open modes), shared evidence schema + `groundcrew-doctor`,
DataForSEO cost-disclosure gate, WHY-NOT-SLOP + ETHICS doctrine, installer
with collision refusal and managed updates.
