#!/usr/bin/env python3
"""Generate thin marketplace metadata from canonical skills/*/SKILL.md files."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.5.1"


def skill_metadata(path: Path) -> dict[str, str]:
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    slug = path.parent.name
    if fields.get("name") != slug or not fields.get("description"):
        raise ValueError(f"name/description mismatch: {path.relative_to(ROOT)}")
    return {"slug": slug, "description": fields["description"], "path": f"skills/{slug}"}


def outputs() -> dict[Path, object]:
    skills = [skill_metadata(p) for p in sorted((ROOT / "skills").glob("*/SKILL.md"))]
    if len(skills) != 13:
        raise ValueError(f"release {VERSION} requires exactly 13 skills, found {len(skills)}")
    common = {
        "name": "groundcrew-seo",
        "version": VERSION,
        "description": "Thirteen open SEO and growth skills for AI agents — audit, fix, keywords, competitors, E-E-A-T, AI visibility, reports — from TrustGrowth.",
        "author": {"name": "TechWright", "url": "https://trustgrowth.ai"},
        "homepage": "https://github.com/techwright-lab/groundcrew-seo",
        "repository": "https://github.com/techwright-lab/groundcrew-seo",
        "license": "MIT",
    }
    claude = {**common, "displayName": "Groundcrew SEO — TrustGrowth", "keywords": ["seo", "seo agent skills", "technical seo", "search console", "e-e-a-t", "geo", "ai visibility", "growth", "trustgrowth", "skills"]}
    codex = {**common, "skills": "./skills/"}
    catalog = {
        "schemaVersion": 1,
        "release": VERSION,
        "canonicalRoot": "skills",
        "repository": "https://github.com/techwright-lab/groundcrew-seo",
        "skills": skills,
        "surfaces": {
            "repositoryDiscovery": ["skills.sh", "Smithery Skills", "SkillsMP", "AgentSkillsHub"],
            "multiSkillPreview": ["ClawHub", "SkillX", "Skilo"],
            "plugins": ["Claude Code", "OpenAI Codex"],
        },
    }
    return {
        ROOT / ".claude-plugin/plugin.json": claude,
        ROOT / ".codex-plugin/plugin.json": codex,
        ROOT / "marketplaces/catalog.json": catalog,
    }


def rendered(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    drift = []
    for path, value in outputs().items():
        content = rendered(value)
        if check:
            if not path.exists() or path.read_text() != content:
                drift.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if drift:
        print("generated adapter drift: " + ", ".join(drift), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
