#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/generate-adapters.py" --check
"$ROOT/scripts/validate-distribution.py"

mapfile -t skills < <(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
printf 'skills.sh / Smithery Skills / SkillsMP / AgentSkillsHub: repository import https://github.com/techwright-lab/groundcrew (13 canonical skills)\n'
for skill in "${skills[@]}"; do
  printf 'ClawHub preview: clawhub skill publish skills/%s --version 0.2.0 --dry-run --json\n' "$skill"
  printf 'SkillX scan: skillx scan https://github.com/techwright-lab/groundcrew/tree/0.2.0/skills/%s\n' "$skill"
  printf 'Skilo pack: skilo pack skills/%s --dry-run\n' "$skill"
done
printf 'No publication performed. Run each printed publisher command only after human approval.\n'
