#!/usr/bin/env python3
"""Validate Groundcrew installation, shared contracts, evidence, and optional connectivity."""
import argparse, datetime as dt, json, os, pathlib, re, subprocess, sys, urllib.error, urllib.request

SCRIPT = pathlib.Path(__file__).resolve()
if SCRIPT.parent.name == ".groundcrew":
    ROOT = SCRIPT.parent
    SKILLS = SCRIPT.parent.parent
    SHARED = SCRIPT.parent / "shared"
else:
    ROOT = SCRIPT.parents[1]
    SKILLS = ROOT / "skills"
    SHARED = ROOT / "shared"


def fail(message, errors):
    print(f"  ✗ {message}")
    errors.append(message)


def ok(message):
    print(f"  ✓ {message}")


def load_schema(errors):
    path = SHARED / "evidence.schema.yaml"
    try:
        schema = json.loads(path.read_text())  # JSON is valid YAML 1.2; stdlib keeps doctor dependency-free.
    except Exception as exc:
        fail(f"evidence schema is not valid JSON-compatible YAML: {exc}", errors)
        return None
    required = {"$schema", "type", "required", "properties"}
    if not required.issubset(schema):
        fail("evidence schema is missing structural keys", errors)
        return None
    ok("evidence schema parses")
    return schema


def validate_value(value, rule, path, errors):
    expected = rule.get("type")
    types = expected if isinstance(expected, list) else [expected] if expected else []
    checks = {"object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
              "string": lambda v: isinstance(v, str), "null": lambda v: v is None,
              "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
              "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
              "boolean": lambda v: isinstance(v, bool)}
    if types and not any(checks[t](value) for t in types):
        errors.append(f"{path}: expected {expected}")
        return
    if "const" in rule and value != rule["const"]: errors.append(f"{path}: must equal {rule['const']!r}")
    if "enum" in rule and value not in rule["enum"]: errors.append(f"{path}: unsupported value {value!r}")
    if isinstance(value, str) and len(value) < rule.get("minLength", 0): errors.append(f"{path}: must not be empty")
    if rule.get("format") == "date-time" and isinstance(value, str):
        rfc3339 = re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d"
            r"(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)",
            value,
        )
        try:
            if not rfc3339:
                raise ValueError
            normalized = value.replace("Z", "+00:00")
            # fromisoformat on Python < 3.11 accepts only 0/3/6 fractional digits; pad/truncate to 6 so any RFC 3339 fraction parses on every supported Python.
            normalized = re.sub(r"\.(\d+)", lambda m: "." + m.group(1)[:6].ljust(6, "0"), normalized)
            parsed = dt.datetime.fromisoformat(normalized)
            if parsed.utcoffset() is None:
                raise ValueError
        except ValueError:
            errors.append(f"{path}: invalid RFC 3339 date-time")
    if isinstance(value, dict):
        for key in rule.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        props = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            for key in value.keys() - props.keys(): errors.append(f"{path}: unknown property {key}")
        for key, child in value.items():
            if key in props: validate_value(child, props[key], f"{path}.{key}", errors)
    if isinstance(value, list) and "items" in rule:
        for i, child in enumerate(value): validate_value(child, rule["items"], f"{path}[{i}]", errors)


def validate_evidence(path, schema, errors):
    try: value = json.loads(pathlib.Path(path).read_text())
    except Exception as exc:
        fail(f"{path}: evidence must be JSON (also valid YAML): {exc}", errors); return
    local = []
    validate_value(value, schema, "$", local)
    if local:
        for message in local: fail(f"{path}: {message}", errors)
    else: ok(f"evidence valid: {path}")


def validate_skills(errors):
    canonical = (SHARED / "provider-selection.md").read_bytes()
    canonical_connectors = (SHARED / "connectors.md").read_bytes()
    found = 0
    candidates = sorted(SKILLS.glob("*/SKILL.md"))
    if SCRIPT.parent.name == ".groundcrew":
        candidates = [skill for skill in candidates if (skill.parent / ".groundcrew-managed").is_file()]
    for skill in candidates:
        found += 1
        text = skill.read_text()
        match = re.match(r"^---\n(.*?)\n---\n(.+)", text, re.S)
        if not match or not re.search(r"^name:\s*\S+", match.group(1), re.M) or not re.search(r"^description:\s*.+", match.group(1), re.M):
            fail(f"invalid skill frontmatter: {skill}", errors)
        ref = skill.parent / "references" / "provider-selection.md"
        if not ref.exists() or ref.read_bytes() != canonical:
            fail(f"missing or drifted provider-selection reference: {skill.parent.name}", errors)
        connectors = skill.parent / "references" / "connectors.md"
        if not connectors.exists() or connectors.read_bytes() != canonical_connectors:
            fail(f"missing or drifted connectors reference: {skill.parent.name}", errors)
        if skill.parent.name in {"keyword-scout", "competitor-watch"}:
            dataforseo = skill.parent / "references" / "dataforseo.md"
            canonical_dataforseo = (SHARED / "dataforseo.md").read_bytes()
            if not dataforseo.exists() or dataforseo.read_bytes() != canonical_dataforseo:
                fail(f"missing or drifted DataForSEO cost guard: {skill.parent.name}", errors)
    if found: ok(f"checked {found} skill frontmatters and shared references")
    else: fail("no skills found", errors)


def parse_version(value):
    parts = str(value).split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def version_satisfies(live, pinned):
    """Same major, and at least the pinned minor.patch — the contract is additive within a major."""
    live_v, pin_v = parse_version(live), parse_version(pinned)
    return bool(live_v and pin_v and live_v[0] == pin_v[0] and live_v >= pin_v)


def api_get(base, key, path):
    req = urllib.request.Request(base + path, headers={
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "User-Agent": "Groundcrew-Doctor/0.3 (+https://github.com/techwright-lab/groundcrew)",
    })
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.status, json.load(response)


def check_contract(base, key, errors):
    pin_path = SHARED / "contract-pin.json"
    if not pin_path.exists():
        fail("contract pin missing (shared/contract-pin.json)", errors); return
    pin = json.loads(pin_path.read_text())
    try:
        _, manifest = api_get(base, key, "/api/v1/capabilities/v1")
    except Exception as exc:
        fail(f"capability manifest fetch failed: {exc}", errors); return
    live = manifest.get("contract_version")
    if live is None:
        fail(f"server manifest has no contract_version; Groundcrew pins {pin['contract_version']} — upgrade the server or the pin", errors)
    elif version_satisfies(live, pin["contract_version"]):
        ok(f"TrustGrowth contract {live} satisfies pinned {pin['contract_version']}")
    else:
        fail(f"TrustGrowth contract {live} does not satisfy pinned {pin['contract_version']} (same major, >= minor.patch)", errors)


def connectivity(errors):
    key = os.getenv("TRUSTGROWTH_API_KEY")
    if not key:
        print("  - TrustGrowth connectivity skipped (TRUSTGROWTH_API_KEY not set)"); return
    base = os.getenv("TRUSTGROWTH_API_BASE", "https://trustgrowth.ai").rstrip("/")
    try:
        status, _ = api_get(base, key, "/api/v1/sites")
        if status == 200: ok("TrustGrowth API connection")
        else: fail(f"TrustGrowth API returned {status}", errors)
    except Exception as exc:
        fail(f"TrustGrowth API connection failed: {exc}", errors); return
    check_contract(base, key, errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", action="append", default=[], help="JSON evidence record to validate")
    parser.add_argument("--connectivity", action="store_true")
    args = parser.parse_args()
    errors = []
    print("Groundcrew doctor")
    schema = load_schema(errors)
    validate_skills(errors)
    if schema:
        for path in args.evidence: validate_evidence(path, schema, errors)
    if args.connectivity: connectivity(errors)
    print(f"\npassed={0 if errors else 1} errors={len(errors)}")
    return 1 if errors else 0

if __name__ == "__main__": raise SystemExit(main())
