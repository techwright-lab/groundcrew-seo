#!/usr/bin/env python3
"""Check the eval corpus: every skill covered, well-formed cases, contract-valid API literals."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EVALS = ROOT / "tests" / "evals"
MANIFEST = ROOT / "shared" / "contract" / "capabilities.json"

MIN_CASES = 5
TIERS = {"open", "import", "tier2", "connected", "any"}
API_LITERAL = re.compile(r"/api/v1/[A-Za-z0-9_/{}.:-]*[A-Za-z0-9}]")


def known_paths():
    manifest = json.loads(MANIFEST.read_text())
    return {o["endpoint"] for o in manifest["operations"]}


def normalize(path):
    return re.sub(r":(\w+)", r"{\1}", path.rstrip("."))


def check_file(path, skill_names, paths, seen_ids, errors):
    name = path.stem
    if name not in skill_names:
        errors.append(f"{path.name}: no skill named '{name}'")
        return
    data = json.loads(path.read_text())
    if data.get("skill") != name:
        errors.append(f"{path.name}: 'skill' field must be '{name}'")
    cases = data.get("cases", [])
    if len(cases) < MIN_CASES:
        errors.append(f"{path.name}: {len(cases)} cases, need at least {MIN_CASES}")
    for case in cases:
        cid = case.get("id", "")
        if not cid.startswith(name + "-"):
            errors.append(f"{path.name}: case id '{cid}' must start with '{name}-'")
        if cid in seen_ids:
            errors.append(f"{path.name}: duplicate case id '{cid}'")
        seen_ids.add(cid)
        if case.get("tier") not in TIERS:
            errors.append(f"{path.name}: case '{cid}' tier must be one of {sorted(TIERS)}")
        if not case.get("prompt", "").strip():
            errors.append(f"{path.name}: case '{cid}' has an empty prompt")
        if not case.get("must"):
            errors.append(f"{path.name}: case '{cid}' has no 'must' expectations")
        blob = json.dumps(case)
        for literal in sorted(set(API_LITERAL.findall(blob))):
            if normalize(literal) not in paths:
                errors.append(f"{path.name}: case '{cid}' references `{literal}` which is not in the TrustGrowth contract")


def main():
    skill_names = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    paths = known_paths()
    errors, seen_ids = [], set()
    files = sorted(EVALS.glob("*.json"))
    covered = {f.stem for f in files}
    for missing in sorted(skill_names - covered):
        errors.append(f"no eval file for skill '{missing}'")
    for path in files:
        check_file(path, skill_names, paths, seen_ids, errors)
    for error in errors:
        print(f"  ✗ {error}")
    if not errors:
        total = sum(len(json.loads(f.read_text())["cases"]) for f in files)
        print(f"  ✓ {len(files)} eval files, {total} cases satisfy the eval contract")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
