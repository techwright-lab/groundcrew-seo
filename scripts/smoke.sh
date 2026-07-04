#!/usr/bin/env bash
# Groundcrew smoke test — verifies every read surface the skills document.
# Safe: read-only, never prints the API key.
# Usage: TRUSTGROWTH_API_KEY=tg_live_... ./scripts/smoke.sh [site-slug]
set -euo pipefail

BASE="${TRUSTGROWTH_API_BASE:-https://trustgrowth.ai}"
: "${TRUSTGROWTH_API_KEY:?Set TRUSTGROWTH_API_KEY (never commit it)}"

auth=(-H "Authorization: Bearer $TRUSTGROWTH_API_KEY")
pass=0; fail=0

check() {
  local name="$1" url="$2"
  if curl -fsS "${auth[@]}" "$url" >/dev/null 2>&1; then
    echo "  ✓ $name"; pass=$((pass+1))
  else
    echo "  ✗ $name ($url)"; fail=$((fail+1))
  fi
}

echo "Groundcrew smoke test against $BASE"

echo "→ openapi (unauthenticated)"
curl -fsS "$BASE/developers/openapi.yml" >/dev/null && echo "  ✓ openapi" || { echo "  ✗ openapi"; fail=$((fail+1)); }

echo "→ core"
check "list sites" "$BASE/api/v1/sites"

SLUG="${1:-$(curl -fsS "${auth[@]}" "$BASE/api/v1/sites" | jq -r '.data[0].slug // empty')}"
if [ -z "$SLUG" ]; then
  echo "No accessible site found; add a site at trustgrowth.ai first."
  exit 1
fi
echo "→ site surfaces ($SLUG)"
for ep in summary score issues next_actions keywords competitors eeat snapshots content "changes?since=7d"; do
  check "$ep" "$BASE/api/v1/sites/$SLUG/$ep"
done

echo
echo "passed=$pass failed=$fail"
[ "$fail" -eq 0 ]
