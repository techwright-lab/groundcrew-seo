#!/usr/bin/env bash
# Groundcrew installer — copies TrustGrowth skills into your agent's skills directory.
# Usage: curl -fsSL https://raw.githubusercontent.com/techwright-lab/groundcrew/main/install.sh | bash
#        SKILLS_DIR=~/.config/myagent/skills ./install.sh
set -euo pipefail

REPO_URL="https://github.com/techwright-lab/groundcrew"
SKILLS_DIR="${SKILLS_DIR:-}"

# Detect a skills directory if not given.
if [ -z "$SKILLS_DIR" ]; then
  for candidate in "$HOME/.claude/skills" "$HOME/.hermes/skills" "$HOME/.openclaw/skills"; do
    if [ -d "$(dirname "$candidate")" ]; then
      SKILLS_DIR="$candidate"
      break
    fi
  done
fi

if [ -z "$SKILLS_DIR" ]; then
  echo "Could not detect a skills directory. Re-run with SKILLS_DIR=/path/to/skills" >&2
  exit 1
fi

echo "Installing Groundcrew skills into $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

if [ -d "$(pwd)/skills" ] && [ -f "$(pwd)/README.md" ]; then
  src="$(pwd)/skills"
else
  git clone --depth 1 --quiet "$REPO_URL" "$workdir/groundcrew"
  src="$workdir/groundcrew/skills"
fi

for skill in "$src"/*/; do
  name="$(basename "$skill")"
  rm -rf "${SKILLS_DIR:?}/$name"
  cp -r "$skill" "$SKILLS_DIR/$name"
  echo "  ✓ $name"
done

cat <<'EOF'

Groundcrew installed. Next steps:
  1. Get an API key: https://trustgrowth.ai/account/api_keys (Hobby plan or higher)
  2. export TRUSTGROWTH_API_KEY="tg_live_..."
  3. Ask your agent: "run my growth standup"

Docs: https://trustgrowth.ai/developers
EOF
