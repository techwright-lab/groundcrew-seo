#!/usr/bin/env python3
"""Static instruction guard for the five policy-aware remediation consumers.

This test reads canonical skill instructions. It does not execute an agent or validate
the separate eval corpus.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONSUMERS = (
    "fix-my-site",
    "grow",
    "site-audit",
    "audit-report",
    "trustgrowth",
)
REQUIRED_CLAUSES = {
    "mandatory intake": (
        "Retain `detection_policy_version` and the complete `remediation` object before batching",
        "split only between issues",
        "preservation, avoid, no-change, and verification constraint",
    ),
    "valid no-change decisions": (
        "Preserve current `keep_as_is` and `not_applicable` dispositions",
        "never create a persistent review merely to empty a queue",
    ),
    "write authorization": (
        "`review_audit_issue` requires a live-manifest advertisement",
        "explicit owner authorization",
        "write scope",
        "unique request key",
        "current evidence signature, policy version, and state token",
        "Read-only compatibility mode blocks it and every other write",
    ),
    "rendered verification": (
        "inspect the actual rendered response",
        "a source diff, test, or build alone is not rendered verification",
    ),
}


for consumer in CONSUMERS:
    path = ROOT / "skills" / consumer / "SKILL.md"
    text = path.read_text()
    for clause, needles in REQUIRED_CLAUSES.items():
        missing = [needle for needle in needles if needle not in text]
        assert not missing, f"{consumer}: missing {clause}: {missing}"

print(
    "remediation consumer contract tests passed "
    "(5 canonical skills; static instruction guard; 0 agent runs)"
)
