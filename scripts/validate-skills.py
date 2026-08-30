#!/usr/bin/env python3
"""Check every skill against the Groundcrew skill contract and the generated TrustGrowth contract."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MANIFEST = ROOT / "shared" / "contract" / "capabilities.json"

REQUIRED_SECTIONS = ("## When not to use", "## Doctrine")
API_LITERAL = re.compile(r"/api/v1/[A-Za-z0-9_/{}.:-]*[A-Za-z0-9}]")


def known_paths():
    manifest = json.loads(MANIFEST.read_text())
    return {o["endpoint"] for o in manifest["operations"]}


def normalize(path):
    return re.sub(r":(\w+)", r"{\1}", path.rstrip("."))


def check_skill(skill, paths, errors):
    name = skill.parent.name
    text = skill.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.+)", text, re.S)
    if not match:
        errors.append(f"{name}: missing frontmatter")
        return
    front, body = match.groups()
    declared = re.search(r"^name:\s*(\S+)", front, re.M)
    if not declared or declared.group(1) != name:
        errors.append(f"{name}: frontmatter name must equal the directory name")
    description = re.search(r"^description:\s*(.+)", front, re.M)
    if not description:
        errors.append(f"{name}: missing description")
    elif not description.group(1).startswith("Use when"):
        errors.append(f"{name}: description must start with 'Use when' so agents can route on the trigger")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(section)}\s*$", body, re.M):
            errors.append(f"{name}: missing section '{section}'")
    for literal in sorted(set(API_LITERAL.findall(body))):
        if normalize(literal) not in paths:
            errors.append(f"{name}: references `{literal}` which is not in the TrustGrowth contract — regenerate or fix the skill")


def main():
    paths = known_paths()
    errors = []
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    for skill in skills:
        check_skill(skill, paths, errors)
    for error in errors:
        print(f"  ✗ {error}")
    if not errors:
        print(f"  ✓ {len(skills)} skills satisfy the skill contract")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
