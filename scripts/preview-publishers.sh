#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/generate-adapters.py" --check
"$ROOT/scripts/validate-distribution.py"

release="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["release"])' "$ROOT/marketplaces/catalog.json")"
mapfile -t skills < <(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
printf 'skills.sh / Smithery Skills / SkillsMP / AgentSkillsHub: repository import https://github.com/techwright-lab/groundcrew-seo (%s canonical skills)\n' "${#skills[@]}"
for skill in "${skills[@]}"; do
  printf 'ClawHub preview: clawhub skill publish skills/%s --version "$release" --dry-run --json\n' "$skill"
  printf 'SkillX scan: skillx scan https://github.com/techwright-lab/groundcrew-seo/tree/v$release/skills/%s\n' "$skill"
  printf 'Skilo pack: skilo pack skills/%s --dry-run\n' "$skill"
done
printf 'No publication performed. Run each printed publisher command only after human approval.\n'
