#!/usr/bin/env python3
"""Deterministic checks for remediation intake worked examples.

These checks validate concrete decision artifacts. They do not execute an agent or
pretend that the static eval corpus does.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "remediation"

ISSUE_FIELDS = {
    "id",
    "issue_type",
    "page_url",
    "status",
    "recorded_severity",
    "severity",
    "classification",
    "interpretation",
    "policy_version",
    "detection_policy_version",
}
GUIDANCE_FIELDS = {
    "guidance_available",
    "applicability",
    "automation",
    "ownership",
    "material_policy_version",
    "observation",
    "recommended_action",
    "proposed_change",
    "preserve",
    "avoid",
    "no_change_when",
    "verification",
    "required_context",
    "scoring_policy",
    "review",
    "context",
    "evidence",
}


def load(name):
    return json.loads((EXAMPLES / name).read_text())


def assert_common(artifact):
    assert artifact["artifact_kind"] == "deterministic_worked_example"
    assert artifact["agent_executed"] is False
    assert artifact["contract_version"] == "1.7.0"
    batches = artifact["batches"]
    assert [batch["number"] for batch in batches] == list(range(1, len(batches) + 1))
    assert all(batch["context_limit"] == 1 for batch in batches)

    seen = []
    for batch in batches:
        issue = batch["input_issue"]
        assert ISSUE_FIELDS <= issue.keys()
        assert GUIDANCE_FIELDS <= issue["remediation"].keys()
        assert batch["retained_issue_identity"] == {
            key: value for key, value in issue.items() if key != "remediation"
        }
        assert batch["retained_remediation"] == issue["remediation"]
        seen.append(issue["id"])
    assert seen == artifact["source_issue_order"]


artifact = load("metadata-decisions.json")
assert_common(artifact)
long_title, missing_title = artifact["batches"]

expected_title = "Proof Pages — your score, in public, with the flaws left in — TrustGrowth"
assert long_title["input_issue"]["issue_type"] == "meta_title_too_long"
assert long_title["input_issue"]["classification"] == "suggestion"
assert long_title["input_issue"]["remediation"]["automation"] == "advisory_only"
assert long_title["decision"]["action"] == "leave_unchanged"
assert long_title["decision"]["rendered_title_before"] == expected_title
assert long_title["decision"]["rendered_title_after"] == expected_title
assert long_title["decision"]["verification"]["status"] == "rendered_verified"
assert long_title["decision"]["verification"]["method"] == "rendered_response_assertion"

assert missing_title["input_issue"]["issue_type"] == "meta_title_missing"
assert missing_title["input_issue"]["remediation"]["automation"] == "propose_change"
assert missing_title["decision"]["action"] == "propose_for_owner_review"
assert missing_title["decision"]["applied"] is False
context = missing_title["input_issue"]["remediation"]["context"]
proposal = missing_title["decision"]["proposed_title"]
assert context["visible_h1"] in proposal
assert proposal.count(context["brand"]) == 1
assert missing_title["decision"]["verification"]["status"] == "pending_owner_and_rendered_verification"

guidance = (ROOT / "shared" / "reporting.md").read_text()
for phrase in [
    "shared title truncator",
    "character padding",
    "bulk rewriting",
    "invented authors or dates",
    "unnecessary schema",
    "reversing deliberate crawler choices",
]:
    assert phrase in guidance, phrase

print("remediation guidance tests passed (2 deterministic worked examples; 0 agent runs)")
