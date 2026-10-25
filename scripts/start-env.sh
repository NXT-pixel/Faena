#!/usr/bin/env bash
# start-env.sh — Entry point for new developers (invokes the full Docker stack).
# Delegates to scripts/start-dev-environment.sh at the repository root. Requires Docker; no
# local .NET/Node/ABP is required for the default flow (builds use containers).
#
# Usage (from anywhere):
#   bash scripts/start-env.sh
#   bash scripts/start-env.sh --no-cache --local-setup
#   bash scripts/start-env.sh --skip-infra --skip-publish
#
# See: scripts/README.md, docker/README.md

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET="$REPO_ROOT/scripts/start-dev-environment.sh"
if [[ ! -f "$TARGET" ]]; then
  echo "Missing $TARGET" >&2
  exit 1
fi
exec bash "$TARGET" "$@"

