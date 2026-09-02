#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 -m py_compile "$ROOT/scripts/groundcrew-doctor.py" "$ROOT/scripts/gen-contract.py" "$ROOT/scripts/validate-skills.py" "$ROOT/scripts/validate-evals.py" "$ROOT/tests/test_timestamp.py" "$ROOT/tests/test_contract.py"
python3 "$ROOT/tests/test_timestamp.py"
python3 "$ROOT/tests/test_contract.py"
"$ROOT/scripts/gen-contract.py" --check
"$ROOT/scripts/validate-skills.py"
"$ROOT/scripts/validate-evals.py"
"$ROOT/scripts/generate-adapters.py" --check
"$ROOT/scripts/validate-distribution.py"
preview="$($ROOT/scripts/preview-publishers.sh)"
test "$(printf '%s\n' "$preview" | grep -c '^ClawHub preview:')" -eq 20
test "$(printf '%s\n' "$preview" | grep -c '^SkillX scan:')" -eq 20
test "$(printf '%s\n' "$preview" | grep -c '^Skilo pack:')" -eq 20
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$ROOT/.claude-plugin/plugin.json")" = 0.7.0
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["skills"])' "$ROOT/.codex-plugin/plugin.json")" = ./skills/
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
test -f "$tmp/skills/fix-my-site/references/connectors.md"
test -f "$tmp/skills/fix-my-site/references/reporting.md"
test -f "$tmp/skills/.groundcrew/shared/connectors.md"
test -f "$tmp/skills/.groundcrew/shared/contract-pin.json"
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
# Connectors drift must fail.
printf '\ndrift\n' >> "$tmp/skills/site-audit/references/connectors.md"
if "$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null 2>&1; then echo "connectors drift unexpectedly passed" >&2; exit 1; fi
SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" --update >/dev/null
# Reporting drift must fail.
printf '\ndrift\n' >> "$tmp/skills/weekly-report/references/reporting.md"
if "$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null 2>&1; then echo "reporting drift unexpectedly passed" >&2; exit 1; fi
SKILLS_DIR="$tmp/skills" "$ROOT/install.sh" --update >/dev/null
# Provider-selection drift must fail.
printf '\ndrift\n' >> "$tmp/skills/fix-my-site/references/provider-selection.md"
if "$tmp/skills/.groundcrew/groundcrew-doctor.py" >/dev/null 2>&1; then echo "drift unexpectedly passed" >&2; exit 1; fi
echo "groundcrew tests passed"
