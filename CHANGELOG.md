# Changelog

All notable changes to the Groundcrew skill pack. Versions are pack-level
(semver); individual skills carry no separate versions. "Verified against"
names the live-contract snapshot the pack's connected-mode text was checked
against.

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
