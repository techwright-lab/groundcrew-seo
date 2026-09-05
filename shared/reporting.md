# Reporting contract

Every Groundcrew report — any output the user may forward, file, or act on later —
follows one skeleton, one verdict scale, and one fact-labeling scheme. Report skills
(`weekly-report`, `audit-report`, `keyword-report`, `competitor-readout`, `geo-report`,
`authority-report`) must use all three; other skills use them whenever they emit a
report-shaped result.

## Skeleton

```markdown
# <Site> — <Report name> — <period or as-of date>

Bottom line: <one sentence>. Verdict: SHIP | FIX | BLOCK | UNDECIDED

## Measured
| metric | value | vs last | label | source | as of |

## What changed
<events in the period; each marked verified (how) or unverified>

## Next 3 actions
<action — owner — effort — expected effect (qualitative, no projections)>

## Evidence
<evidence record paths/ids, proof URLs, job ids>

## Not measured
<what could not be observed and why>
```

Sections stay in this order. Empty sections say why they are empty instead of
disappearing. `## Next 3 actions` may hold fewer than three when fewer are justified;
it never pads.

## Verdicts

- **SHIP** — the reported surface is in acceptable shape; nothing found blocks the next
  planned action. Open suggestions and explicit no-change decisions may coexist with
  SHIP when no applicable defect requires action.
- **FIX** — current evidence and applicable guidance establish specific named defects;
  the report lists them with an owner and a proposed repair. An open `critical` finding
  forces FIX only when its current remediation, or the equivalent standalone decision
  record, says the finding is applicable and supports a change. Severity orders
  attention; it never authorizes a write by itself.
- **BLOCK** — a veto tripped. Vetoes are absolute: one veto forces BLOCK regardless of
  every other number. Standing vetoes: a claim in the report cannot be traced to
  validated evidence; an evidence record failed doctor validation and was used anyway
  (never do this); the action the report recommends is irreversible or outward-facing
  and lacks owner review.
- **UNDECIDED** — required evidence, context, or applicable remediation guidance is
  missing. Name what is missing and the cheapest way to get it. Never guess a verdict
  or turn unavailable guidance into a repair to avoid UNDECIDED.

## Remediation decisions

Keep five states separate in every audit workflow: the original observation, its
current policy interpretation, a proposed action, the owner's review decision, and
post-change verification. A severity or accepted finding is not write authorization;
an accepted proposal or review decision is not proof that a repair happened.

### Connected issue intake

For every TrustGrowth issue, retain the stable `id`, `issue_type`, `page_url`, `status`,
`recorded_severity`, current `severity`, `classification`, `interpretation`,
`policy_version`, and `detection_policy_version`. Read the complete `remediation`
object before deciding what to do. In particular, retain:

- `guidance_available`, `applicability`, `automation`, `ownership`, and
  `material_policy_version`;
- `observation`, `recommended_action`, and `proposed_change`;
- `preserve`, `avoid`, `no_change_when`, `verification`, and `required_context`;
- `review`, `context`, `evidence`, and `scoring_policy`.

Paginate until the requested scope is complete. If context limits require batches,
split between issues, never inside one issue's identity and remediation fields. Carry
the full `preserve`, `avoid`, `no_change_when`, and `verification` arrays into the
working decision artifact for every batch. Do not let raw legacy severity, ordering in
`next_actions`, or a shortened summary replace those constraints.

Use the current metadata this way:

- `advisory_only` or `classification: suggestion` means advice, not a defect queue.
  Prefer no change when `no_change_when` applies.
- `investigate`, `applicability: unknown`, missing required context, or
  `guidance_available: false` means gather evidence and context before proposing a
  change.
- `propose_change` permits a contextual proposal only when applicability is confirmed.
  It does not permit applying the proposal.
- `applicability: not_applicable` and a current `review.disposition` of `keep_as_is` or
  `not_applicable` remain no-change decisions. Do not create a persistent review merely
  to remove an item from a queue. Preserve an existing valid owner decision until the
  server marks its evidence, occurrence, or material policy stale.

Older servers may omit `remediation`. Feature-detect it per response. Treat absent or
unusable guidance as `investigate`; with explicit local evidence, prepare a bounded
proposal for owner review. An explicit `applicability: not_applicable` stays a no-change
decision. Never turn missing guidance into a blanket repair.
Standalone and imported workflows apply the same principle: record the observation,
local evidence, required context, proposed action, preservation constraints, owner
decision, and rendered verification separately.

`review_audit_issue` may be used only when the generated contract advertises it and
the owner explicitly authorizes recording their decision. Use write scope, a unique
request key, and the current evidence signature, policy version, and state token from
`remediation.review`; handle stale conflicts by re-reading the issue. The call records
`keep_as_is`, `not_applicable`, or `reopen`. It does not approve an agent's own proposal,
verify a fix, alter scoring, or authorize content publication.

### Metadata and rendered verification

Preserve complete, accurate authored metadata. Character counts and preview pixel
widths are suggestions, not editing ceilings; real storage, payload, and platform
limits remain separate. Never introduce a shared title truncator, character padding,
bulk rewriting, invented authors or dates, unnecessary schema, or a change that amounts
to reversing deliberate crawler choices.

For a missing title, inspect the page's visible purpose and existing brand composition,
then propose one accurate, distinctive title. For an existing clear title, keep the
complete wording even when a length suggestion exists. After an approved code change,
verify the actual rendered response in a browser or fetched HTML, including the final
`<title>`, meta tags, structured data, canonical/robots behavior, and visible content
affected by the change. A source-template diff, unit test, or successful build alone is
local evidence, not rendered verification.

## Fact labels

Every value in `## Measured` carries exactly one label:

- **Measured** — read from a source that passed the Groundcrew evidence contract;
  the row names source and observation time.
- **User-provided** — pasted or imported by the user; reported verbatim with the
  import date. Groundcrew does not silently correct user numbers.
- **Estimated** — a third-party estimate or heuristic; the row names the estimator.
  Estimates never appear without the label and never upgrade to Measured by repetition.

`vs last` compares only values with the same label and the same source; otherwise the
cell stays empty with a note in `## Not measured`. Missing values remain missing —
never zero, never interpolated.
