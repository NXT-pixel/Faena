#!/usr/bin/env bash

# analyze-imports.sh — Onboarding & import analysis for the Orchestration Framework
#
# Run this when you start the project to see:
#   - Where Angular, C#, and Python apps live and how to run them
#   - Import/dependency patterns across the monorepo
#
# Usage: from repo root (orchestration_framework):
#   bash AngularWithMCPServers/scripts/analyze-imports.sh [--full|--check]
#
# On Windows: use Git Bash or WSL, or run from repo root:
#   bash .\AngularWithMCPServers\.cursor\scripts\analyze-imports.sh

set -e

# --- Repo root discovery ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
# From scripts/ go up to AngularWithMCPServers, then parent = repo root
ANGULAR_MCP="$(cd "$SCRIPT_DIR/../.." && pwd)"
if [ -d "$ANGULAR_MCP/../PythonMAFWithAzureFunctions" ]; then
  REPO_ROOT="$(cd "$ANGULAR_MCP/.." && pwd)"
else
  REPO_ROOT="$ANGULAR_MCP"
fi

# Configuration
EXCLUDE_DIRS=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=build --exclude-dir=coverage \
  --exclude-dir=.angular --exclude-dir=.vite --exclude-dir=.cache --exclude-dir=bin --exclude-dir=obj \
  --exclude-dir=__pycache__ --exclude-dir=.venv --exclude-dir=venv)
TS_FILES=(--include='*.ts' --include='*.tsx')
CS_FILES=(--include='*.cs')
PY_FILES=(--include='*.py')

# Parse command line
MODE="full"
while [[ $# -gt 0 ]]; do
  case $1 in
    --full)  MODE="full" ; shift ;;
    --check) MODE="check" ; shift ;;
    *)
      echo "Usage: $0 [--full|--check]" >&2
      exit 2
      ;;
  esac
done

check_tools() {
  local missing=()
  for tool in grep sed sort uniq awk; do
    if ! command -v "$tool" &>/dev/null; then
      missing+=("$tool")
    fi
  done
  if [ ${#missing[@]} -gt 0 ]; then
    echo "ERROR: Missing required tools: ${missing[*]}" >&2
    exit 2
  fi
}

# ---------- 1. ONBOARDING: Project map & how to run ----------
print_onboarding() {
  echo "=== ORCHESTRATION FRAMEWORK — PROJECT MAP ==="
  echo "Run this script from repo root when you start the project (Angular + C# + Python)."
  echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "Repo root: $REPO_ROOT"
  echo ""

  # Angular
  echo "--- Angular ---"
  if [ -d "$REPO_ROOT/AngularWithMCPServers/src/ControlPanel" ]; then
    echo "  App: AngularWithMCPServers/src/ControlPanel (Control Panel UI)"
    echo "    Run: cd $REPO_ROOT/AngularWithMCPServers/src/ControlPanel && npm install && npm start"
    echo ""
  fi

  # C# (.NET)
  echo "--- C# / .NET ---"
  while IFS= read -r -d '' csproj; do
    dir="$(dirname "$csproj")"
    name="$(basename "$csproj" .csproj)"
    echo "  Project: $name"
    echo "    Path: $dir"
    echo "    Run: cd $dir && dotnet run"
    echo ""
  done < <(find "$REPO_ROOT" -name "*.csproj" -not -path "*/node_modules/*" -not -path "*/.angular/*" -print0 2>/dev/null)

  # Python
  echo "--- Python ---"
  for req in "$REPO_ROOT/AngularWithMCPServers/src/Orchestration/requirements.txt" "$REPO_ROOT/PythonMAFWithAzureFunctions/Orchestration/requirements.txt"; do
    if [ -f "$req" ]; then
      dir="$(dirname "$req")"
      echo "  App: $dir"
      echo "    Run: cd $dir && pip install -r requirements.txt && func start (Azure Functions)"
      echo ""
    fi
  done
  echo ""
}

# ---------- 2. Angular: import analysis ----------
analyze_angular() {
  local root="$REPO_ROOT/AngularWithMCPServers/src/ControlPanel"
  [ ! -d "$root" ] && return

  echo "=== ANGULAR (Control Panel) IMPORTS ==="
  echo ""

  # External packages (e.g. @angular/*)
  echo "--- External packages (top 25) ---"
  grep -rh "from ['\"]" "$root/src" "${EXCLUDE_DIRS[@]}" "${TS_FILES[@]}" 2>/dev/null \
    | sed -n "s/.*from ['\"]\\([^'\"]*\\)['\"].*/\1/p" \
    | sed 's|/.*||' \
    | sort | uniq -c | sort -rn | head -25

  echo ""
  echo "--- Internal (relative) imports ---"
  grep -rh "from ['\"]\\.\\.*" "$root/src" "${EXCLUDE_DIRS[@]}" "${TS_FILES[@]}" 2>/dev/null \
    | sed -n "s/.*from ['\"]\\([^'\"]*\\)['\"].*/\1/p" \
    | sort | uniq -c | sort -rn | head -20

  echo ""
}

# ---------- 3. C#: projects and usings ----------
analyze_csharp() {
  echo "=== C# / .NET PROJECTS & NAMESPACES ==="
  echo ""

  while IFS= read -r -d '' csproj; do
    dir="$(dirname "$csproj")"
    name="$(basename "$csproj" .csproj)"
    echo "--- Project: $name ($dir) ---"

    # Project references
    refs=$(grep -o '<ProjectReference[^>]*Include="[^"]*"' "$csproj" 2>/dev/null | sed 's/.*Include="\([^"]*\)".*/\1/' || true)
    if [ -n "$refs" ]; then
      echo "  References:"
      echo "$refs" | while read -r r; do echo "    - $r"; done
    fi

    # Top-level using (namespace) counts
    echo "  Top namespaces (using):"
    find "$dir" -name "*.cs" -not -path "*/bin/*" -not -path "*/obj/*" 2>/dev/null | while read -r f; do grep -h "^using " "$f" 2>/dev/null; done \
      | sed 's/using \s*\([^;]*\);/\1/' | sort | uniq -c | sort -rn | head -15 | while read -r count ns; do echo "    $count $ns"; done

    echo ""
  done < <(find "$REPO_ROOT" -name "*.csproj" -not -path "*/node_modules/*" -print0 2>/dev/null)
}

# ---------- 4. Python: imports ----------
analyze_python() {
  echo "=== PYTHON IMPORTS ==="
  echo ""

  for pyroot in "$REPO_ROOT/AngularWithMCPServers/src/Orchestration" "$REPO_ROOT/PythonMAFWithAzureFunctions/Orchestration"; do
    [ ! -d "$pyroot" ] && continue
    echo "--- $pyroot ---"
    grep -rh "^import \|^from " "$pyroot" "${EXCLUDE_DIRS[@]}" "${PY_FILES[@]}" 2>/dev/null \
      | sed 's/^import \s*\([a-zA-Z0-9_]*\).*/\1/' \
      | sed 's/^from \s*\([a-zA-Z0-9_.]*\).*/\1/' \
      | sed 's/\.[^.]*$//' \
      | sort | uniq -c | sort -rn | head -20
    echo ""
  done

  echo "--- requirements.txt (declared deps) ---"
  for req in "$REPO_ROOT/AngularWithMCPServers/src/Orchestration/requirements.txt" "$REPO_ROOT/PythonMAFWithAzureFunctions/Orchestration/requirements.txt"; do
    if [ -f "$req" ]; then
      echo "  $req:"
      grep -v "^#" "$req" | grep -v "^$" | sed 's/^/    /'
      echo ""
    fi
  done
}

# ---------- Main ----------
main() {
  check_tools

  echo ""
  print_onboarding

  if [ "$MODE" = "check" ]; then
    echo "=== MODE: check (run with --full for full import analysis) ==="
    exit 0
  fi

  analyze_angular
  analyze_csharp
  analyze_python

  echo "=== END OF REPORT ==="
}

main

