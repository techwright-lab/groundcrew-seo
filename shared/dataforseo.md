# DataForSEO provider guard

DataForSEO is an optional, paid, usage-based source for keyword and competitor evidence. It is never required to use Groundcrew.

Official references (check at execution time because prices and endpoint terms change):

- Pricing overview: https://dataforseo.com/pricing
- SERP Google Organic Live Advanced: https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/
- Google Ads Search Volume Live: https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/
- API documentation root: https://docs.dataforseo.com/v3/

## Cost-disclosure gate

Before any billable request:

1. Identify the exact endpoint, task count, location/language, depth, and live-vs-standard mode.
2. Read the current official endpoint pricing; never rely on a price copied into this repository.
3. Show the user a preflight containing the endpoint, number of tasks/keywords, current documented unit price or pricing rule, estimated maximum charge, and official pricing URL.
4. Obtain explicit approval for that bounded spend. Approval for one batch does not authorize later or larger batches.
5. Execute no more than the approved scope. Do not retry billable failures automatically unless the provider states the failed request was not charged.
6. Report actual task counts and provider-reported cost when available. Never print credentials.

Prefer the smallest probe that can change the recommendation. Cache/reuse results from the current run, deduplicate keywords and domains, and do not request broad country/device/depth combinations by default.

Normalize returned observations to the Groundcrew evidence contract and preserve DataForSEO task IDs in `provenance.reference` or `raw_reference`.
