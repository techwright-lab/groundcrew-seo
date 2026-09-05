#!/usr/bin/env python3
import importlib.util, json, subprocess, sys, tempfile
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

manifest = gen.normalize(json.loads((root / "shared/contract/capabilities.json").read_text()))
pin = json.loads((root / "shared/contract-pin.json").read_text())
first, second = gen.render(manifest, pin), gen.render(manifest, pin)
assert first == second, "render must be deterministic"
assert "| `trigger_audit` |" in first and "`/api/v1/sites/{slug}/trigger_audit`" in first
assert "| `review_audit_issue` |" in first and "`/api/v1/sites/{slug}/issues/{issue_id}/reviews`" in first
assert all(f"`{d['name']}`" in first for d in manifest["dark_surfaces"]), "dark surfaces must be listed"
assert not any(f"| `{d['name']}` |" in first for d in manifest["dark_surfaces"]), "dark surfaces must not appear as tools"

with tempfile.TemporaryDirectory() as tmp:
    skill = Path(tmp) / "skills/invented"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: invented\ndescription: Use when testing\n---\n# x\n\n`/api/v1/sites/{slug}/does_not_exist`\n\n## When not to use\n\n## Doctrine\n")
    validator = load("validate_skills", root / "scripts/validate-skills.py")
    errors = []
    validator.check_skill(skill / "SKILL.md", validator.known_paths(), errors)
    assert errors and "does_not_exist" in errors[0], errors

print("contract tests passed")
