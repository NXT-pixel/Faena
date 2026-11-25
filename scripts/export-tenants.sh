#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
    python3 - "$REPO_ROOT" "${1:-}" <<'PY'
import json
import os
import subprocess
import sys
import time

repo_root = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else os.path.join(repo_root, "tenants.local.json")
tenants_dir = os.path.join(repo_root, "tenants")
active_file = os.path.join(repo_root, ".active-tenant")

active_tenant = ""
if os.path.isfile(active_file):
    with open(active_file, "r", encoding="utf-8") as f:
        active_tenant = f.read().strip()


def rf(fpath):
    if os.path.isfile(fpath):
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    return ""


tenants = []
if os.path.isdir(tenants_dir):
    for d in sorted(os.listdir(tenants_dir)):
        p = os.path.join(tenants_dir, d)
        if os.path.isdir(p) and not d.startswith("."):
            ctx = os.path.join(p, "context")
            rules = os.path.join(p, "rules")
            proy = os.path.join(p, "Proyecto")
            repos = []
            if os.path.isdir(proy):
                for r in sorted(os.listdir(proy)):
                    rp = os.path.join(proy, r)
                    if os.path.isdir(rp) and not r.startswith("."):
                        remote_url = ""
                        if os.path.exists(os.path.join(rp, ".git")):
                            try:
                                res = subprocess.run(
                                    ["git", "-C", rp, "remote", "get-url", "origin"],
                                    capture_output=True, text=True, timeout=3
                                )
                                if res.returncode == 0:
                                    remote_url = res.stdout.strip()
                            except Exception:
                                pass
                        repos.append({"name": r, "remote_url": remote_url})
            adrs = []
            adrs_dir = os.path.join(ctx, "adrs")
            if os.path.isdir(adrs_dir):
                for af in sorted(os.listdir(adrs_dir)):
                    if af.endswith(".md"):
                        adrs.append({"filename": af, "content": rf(os.path.join(adrs_dir, af))})
            tenants.append({
                "slug": d,
                "name": d.replace("-", " "),
                "team_context": rf(os.path.join(ctx, "team-context.md")),
                "tech_context": rf(os.path.join(ctx, "tech-context.md")),
                "company_standards": rf(os.path.join(rules, "company-standards.md")),
                "learnings": rf(os.path.join(ctx, "learnings.md")),
                "project_structure": rf(os.path.join(ctx, "project-structure.md")),
                "progress": rf(os.path.join(ctx, "progress.md")),
                "system_patterns": rf(os.path.join(ctx, "system-patterns.md")),
                "adrs": adrs,
                "repos": repos,
            })

payload = {
    "version": "1.0",
    "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "active_tenant": active_tenant,
    "tenants": tenants,
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f"\033[0;32m[OK] Tenants exportados exitosamente a {output_file}\033[0m")
print(f"     Tenants guardados: {len(tenants)}")
PY
elif command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT_DIR/export-tenants.ps1" "$@"
else
    echo "Error: Se requiere python3 o pwsh para exportar tenants." >&2
    exit 1
fi
