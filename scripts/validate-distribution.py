#!/usr/bin/env python3
"""Build and audit the exact public distribution payload without publishing it."""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROOT_FILES = {"CHANGELOG.md", "ETHICS.md", "LICENSE", "README.md", "WHY-NOT-SLOP.md"}
ALLOWED_DIRS = {"skills", "shared", ".claude-plugin", ".codex-plugin", "marketplaces"}
DENIED_PARTS = {".git", ".github", ".env", "private", "holdout", "_vault", "tests", "scripts", "examples"}


def main() -> int:
    catalog = json.loads((ROOT / "marketplaces/catalog.json").read_text())
    expected = sorted(item["slug"] for item in catalog["skills"])
    actual = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    if actual != expected or len(actual) != 13:
        raise SystemExit("catalog/canonical skill mismatch")
    with tempfile.TemporaryDirectory(prefix="groundcrew-public-") as temp:
        stage = Path(temp)
        for name in sorted(ALLOWED_ROOT_FILES):
            shutil.copy2(ROOT / name, stage / name)
        for name in sorted(ALLOWED_DIRS):
            shutil.copytree(ROOT / name, stage / name)
        leaked = [p for p in stage.rglob("*") if DENIED_PARTS.intersection(p.parts)]
        if leaked:
            raise SystemExit("private/unrelated file in payload")
        files = sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file())
        if any(p.endswith("SKILL.md") and not p.startswith("skills/") for p in files):
            raise SystemExit("duplicated skill body outside canonical skills/")
        if os.environ.get("GROUNDCREW_PRINT_PAYLOAD") == "1":
            print("\n".join(files))
    print(f"public payload verified: {len(actual)} canonical skills; no private/unrelated files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
