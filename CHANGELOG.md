# Changelog

All notable Groundcrew pack changes are documented here. Groundcrew uses semantic versioning for public skill-pack releases.

## [0.2.0] - 2026-07-31

### Added

- Added AI Visibility, Authority Review, Backlink Opportunities, and Content Strategy skills for open/import-first workflows.
- Extended the evidence contract with `ai_visibility`, `authority`, `backlink`, `content_strategy`, `link_graph`, `structured_data`, and `ai_referral` evidence types.
- Added a pinned installer path for the `v0.2.0` release and installer `--ref` / `GROUNDCREW_REF` override support.
- Added a version file for release automation and a valid AI visibility evidence fixture.

### Changed

- Replaced launch-date wording with durable current capability/status language.
- Added scope-routing guidance so skills route adjacent work to the right Groundcrew skill instead of recursively broadening scope.
- Clarified that direct GSC and PageSpeed Insights adapters are currently unsupported as Groundcrew direct-provider integrations; imports and TrustGrowth-managed evidence remain valid inputs.

### Safety

- Added explicit crawler-content prompt-injection handling to crawler-facing skills.
- Encoded official-source-correct AI visibility rules: no Google-Extended veto, no `llms.txt` ranking/citation claim, and no invented AI citation score.
- Added authority/backlink guardrails: third-party metrics stay provider-labeled, outreach is human-reviewed, and Groundcrew never generates or submits a disavow file automatically.

## [0.1.0] - 2026-07-12

### Added

- Initial provider-flexible Groundcrew skill pack with shared evidence contract, doctor validation, installer collision safety, DataForSEO cost guard, and the `fix-my-site` tested-fix workflow.
