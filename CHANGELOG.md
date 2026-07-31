# Changelog

All notable changes to the Groundcrew skill pack. Versions are pack-level
(semver); individual skills carry no separate versions. "Verified against"
names the live-contract snapshot the pack's connected-mode text was checked
against.

## [Unreleased] — 0.2.0-dev

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
