#!/usr/bin/env python3
import contextlib, importlib.util, io, json, subprocess, sys, tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


doctor = load("groundcrew_doctor", root / "scripts/groundcrew-doctor.py")
gen = load("gen_contract", root / "scripts/gen-contract.py")

for live, pinned, expected in [
    ("1.0.0", "1.0.0", True), ("1.2.0", "1.0.0", True), ("1.0.1", "1.0.0", True),
    ("2.0.0", "1.0.0", False), ("1.0.0", "1.1.0", False), ("v1", "1.0.0", False), (None, "1.0.0", False),
]:
    assert doctor.version_satisfies(live, pinned) is expected, (live, pinned, expected)

for live, pinned, expected in [
    ("1.7.0", "1.7.0", "full"),
    ("1.8.0", "1.7.0", "full"),
    ("1.6.9", "1.7.0", "read_only_feature_detected"),
    ("1.0.0", "1.7.0", "read_only_feature_detected"),
    ("2.0.0", "1.7.0", None),
    ("v1", "1.7.0", None),
    (None, "1.7.0", None),
]:
    assert doctor.compatibility_mode(live, pinned) == expected, (live, pinned, expected)

compatibility_manifest = {
    "operations": [
        {
            "availability": "public",
            "method": "GET",
            "endpoint": "/api/v1/sites/{slug}/issues",
        },
        {
            "availability": "public",
            "method": "POST",
            "endpoint": "/api/v1/sites/{slug}/issues/{issue_id}/reviews",
        },
    ]
}
assert doctor.operation_allowed(
    compatibility_manifest,
    "GET",
    "/api/v1/sites/{slug}/issues",
    "read_only_feature_detected",
)
assert not doctor.operation_allowed(
    compatibility_manifest,
    "POST",
    "/api/v1/sites/{slug}/issues/{issue_id}/reviews",
    "read_only_feature_detected",
)
assert doctor.operation_allowed(
    compatibility_manifest,
    "POST",
    "/api/v1/sites/{slug}/issues/{issue_id}/reviews",
    "full",
)
assert not doctor.operation_allowed(
    compatibility_manifest,
    "GET",
    "/api/v1/sites/{slug}/missing",
    "read_only_feature_detected",
)

manifest = gen.normalize(json.loads((root / "shared/contract/capabilities.json").read_text()))
pin = json.loads((root / "shared/contract-pin.json").read_text())
assert pin["older_same_major"] == "read_only_feature_detected"
assert pin["incompatible_major"] == "blocked"
first, second = gen.render(manifest, pin), gen.render(manifest, pin)
assert first == second, "render must be deterministic"
assert "full-mode target `1.7.0`" in first
assert "Older same-major contracts run read-only" in first
assert "| `trigger_audit` |" in first and "`/api/v1/sites/{slug}/trigger_audit`" in first
assert "| `review_audit_issue` |" in first and "`/api/v1/sites/{slug}/issues/{issue_id}/reviews`" in first
assert all(f"`{d['name']}`" in first for d in manifest["dark_surfaces"]), "dark surfaces must be listed"
assert not any(f"| `{d['name']}` |" in first for d in manifest["dark_surfaces"]), "dark surfaces must not appear as tools"

original_api_get = doctor.api_get
try:
    for live, expected_error, expected_text in [
        ("1.8.0", False, "supports full mode"),
        ("1.6.0", False, "read-only feature-detected compatibility mode"),
        ("2.0.0", True, "is incompatible"),
        ("broken", True, "is incompatible"),
    ]:
        doctor.api_get = lambda *_args, live=live: (200, {"contract_version": live})
        errors = []
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            doctor.check_contract("https://example.test", "secret", errors)
        assert bool(errors) is expected_error, (live, errors)
        assert expected_text in output.getvalue(), (live, output.getvalue())
finally:
    doctor.api_get = original_api_get

with tempfile.TemporaryDirectory() as tmp:
    skill = Path(tmp) / "skills/invented"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: invented\ndescription: Use when testing\n---\n# x\n\n`/api/v1/sites/{slug}/does_not_exist`\n\n## When not to use\n\n## Doctrine\n")
    validator = load("validate_skills", root / "scripts/validate-skills.py")
    errors = []
    validator.check_skill(skill / "SKILL.md", validator.known_paths(), errors)
    assert errors and "does_not_exist" in errors[0], errors

print("contract tests passed")
