#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 -m py_compile "$ROOT/scripts/groundcrew-doctor.py" "$ROOT/tests/test_timestamp.py"
python3 "$ROOT/tests/test_timestamp.py"
"$ROOT/scripts/groundcrew-doctor.py" --evidence "$ROOT/examples/evidence/valid-keyword.json"
"$ROOT/scripts/groundcrew-doctor.py" --evidence "$ROOT/examples/evidence/valid-ai-visibility.json"
if "$ROOT/scripts/groundcrew-doctor.py" --evidence "$ROOT/tests/fixtures/invalid-evidence.json" >/dev/null 2>&1; then echo "invalid evidence unexpectedly passed" >&2; exit 1; fi
if "$ROOT/scripts/groundcrew-doctor.py" --evidence "$ROOT/tests/fixtures/invalid-date-only.json" >/dev/null 2>&1; then echo "date-only timestamp unexpectedly passed" >&2; exit 1; fi
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/skills/fix-my-site"; echo custom > "$tmp/skills/fix-my-site/custom.txt"
if SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" >/dev/null 2>&1; then echo "collision unexpectedly overwritten" >&2; exit 1; fi
test -f "$tmp/skills/fix-my-site/custom.txt"
SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" --force >/dev/null
test -x "$tmp/skills/.groundcrew/groundcrew-doctor.py"
test -f "$tmp/skills/fix-my-site/references/provider-selection.md"
# Unmanaged third-party skills must not be subjected to Groundcrew's shared-reference contract.
mkdir -p "$tmp/skills/third-party"
printf '%s\n' '---' 'name: third-party' 'description: unrelated' '---' '# Third party' > "$tmp/skills/third-party/SKILL.md"
"$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null
SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" --update >/dev/null
SKILLS_DIR="$tmp/dry" "$ROOT/install.sh" --dry-run >/dev/null
test ! -e "$tmp/dry"
# DataForSEO cost-guard drift must fail.
printf '\ndrift\n' >> "$tmp/skills/keyword-scout/references/dataforseo.md"
if "$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null 2>&1; then echo "DataForSEO guard drift unexpectedly passed" >&2; exit 1; fi
SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" --update >/dev/null
# Provider-selection drift must fail.
printf '\ndrift\n' >> "$tmp/skills/fix-my-site/references/provider-selection.md"
if "$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null 2>&1; then echo "drift unexpectedly passed" >&2; exit 1; fi
echo "groundcrew tests passed"
