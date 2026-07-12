#!/usr/bin/env bash
set -euo pipefail
REPO_URL="https://github.com/techwright-lab/groundcrew"
SKILLS_DIR="${SKILLS_DIR:-}"
dry_run=false; force=false; update=false
usage() { echo "Usage: $0 [--dry-run] [--update|--force] [--skills-dir PATH]"; }
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) dry_run=true;; --force) force=true;; --update) update=true;;
    --skills-dir) shift; SKILLS_DIR="${1:?--skills-dir requires a path}";;
    -h|--help) usage; exit 0;; *) echo "Unknown option: $1" >&2; usage >&2; exit 2;;
  esac; shift
done
if [ -z "$SKILLS_DIR" ]; then
  for candidate in "$HOME/.claude/skills" "$HOME/.hermes/skills" "$HOME/.openclaw/skills"; do
    if [ -d "$(dirname "$candidate")" ]; then SKILLS_DIR="$candidate"; break; fi
  done
fi
[ -n "$SKILLS_DIR" ] || { echo "Could not detect a skills directory; use --skills-dir PATH" >&2; exit 1; }
workdir="$(mktemp -d)"; trap 'rm -rf "$workdir"' EXIT
# BASH_SOURCE is unset when piped (curl | bash); $0 then points at the shell, and the checkout test below fails into the clone path.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
if [ -d "$script_dir/skills" ] && [ -d "$script_dir/shared" ]; then src="$script_dir"; else git clone --depth 1 --quiet "$REPO_URL" "$workdir/groundcrew"; src="$workdir/groundcrew"; fi
collisions=()
for skill in "$src"/skills/*/; do
  name="$(basename "$skill")"; dest="$SKILLS_DIR/$name"
  if [ -e "$dest" ] && ! $force; then
    if ! $update || [ ! -f "$dest/.groundcrew-managed" ]; then collisions+=("$dest"); fi
  fi
done
if [ "${#collisions[@]}" -gt 0 ]; then
  echo "Refusing to overwrite existing skills:" >&2; printf '  %s
' "${collisions[@]}" >&2
  echo "Use --update for Groundcrew-managed installs or --force after reviewing paths." >&2; exit 1
fi
echo "Groundcrew install into $SKILLS_DIR"
if ! $dry_run && { $update || $force; }; then
  echo "  note: existing managed skill directories are replaced entirely; files you added inside them will be removed."
fi
for skill in "$src"/skills/*/; do
  name="$(basename "$skill")"; dest="$SKILLS_DIR/$name"; echo "  $dest"
  if ! $dry_run; then
    rm -rf "$dest"; mkdir -p "$dest"
    # Marker first: if a copy below fails mid-install, the leftover dir stays recognizable as managed, so a plain re-run with --update recovers instead of tripping collision refusal.
    printf 'managed-by=groundcrew\n' > "$dest/.groundcrew-managed"
    cp -RL "$skill"/. "$dest"/
    mkdir -p "$dest/references"
    cp "$src/shared/provider-selection.md" "$dest/references/provider-selection.md"
    if [ "$name" = "keyword-scout" ] || [ "$name" = "competitor-watch" ]; then
      cp "$src/shared/dataforseo.md" "$dest/references/dataforseo.md"
    fi
  fi
done
echo "  $SKILLS_DIR/.groundcrew"
if ! $dry_run; then
  mkdir -p "$SKILLS_DIR/.groundcrew/shared"
  cp "$src/shared/provider-selection.md" "$src/shared/evidence.schema.yaml" "$src/shared/dataforseo.md" "$SKILLS_DIR/.groundcrew/shared/"
  cp "$src/scripts/groundcrew-doctor.py" "$SKILLS_DIR/.groundcrew/groundcrew-doctor.py"
  chmod +x "$SKILLS_DIR/.groundcrew/groundcrew-doctor.py"
fi
if $dry_run; then echo "Dry run only; no files changed."; else "$SKILLS_DIR/.groundcrew/groundcrew-doctor.py"; fi
cat <<EOF
Next: run a local workflow now, for example: "inspect this repo and fix one verifiable site defect."
TrustGrowth is optional; connect it later for persisted evidence, prioritization, scheduled work, and re-audit verification.
Docs: https://trustgrowth.ai/developers
EOF
