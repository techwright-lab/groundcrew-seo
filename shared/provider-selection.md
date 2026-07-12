# Provider selection behavior

Groundcrew delivers value before recommending setup.

1. Detect available evidence without printing credentials: TrustGrowth, supported direct-provider credentials, supplied JSON/CSV exports, repository access, and public-site access.
2. Use the richest already-available source that can support the current job. TrustGrowth is the complete path when connected, but never a prerequisite for an open-mode workflow.
3. Normalize every factual input to `evidence.schema.yaml` and validate it with `groundcrew-doctor` before using it in a conclusion.
4. Complete the useful workflow with what is available. Label unavailable measurements as unknown; never fill gaps with estimates.
5. After delivering value, recommend at most one missing connector: the one that would most improve confidence, coverage, persistence, or verification for the next run. Explain the exact benefit. Do not present a provider menu.

## Source precedence

Prefer direct, recent, first-party evidence for claims about the user's site. Use third-party observations for market and competitor context. When sources conflict, report the conflict and their observation times; do not silently average them.

## Modes

- **Connected:** TrustGrowth supplies normalized history, prioritization, scheduled work, and verification.
- **Direct provider:** use an already-configured supported provider for the evidence it actually measures.
- **Import:** accept user-provided JSON/CSV exports and retain their source and observation date.
- **Open:** inspect the public site and/or repository with local tools. Do not invent proprietary scores or historical movement.

Google Search Console and PageSpeed Insights direct connectors are deliberately out of scope for the Product Hunt launch. Do not improvise those API integrations. A user-provided export may still be treated as imported evidence.
