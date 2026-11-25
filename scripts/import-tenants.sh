#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
    python3 - "$REPO_ROOT" "${1:-}" <<'PY'
import json
import os
import re
import sys

repo_root = sys.argv[1]
input_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else os.path.join(repo_root, "tenants.local.json")
tenants_dir = os.path.join(repo_root, "tenants")
active_file = os.path.join(repo_root, ".active-tenant")

if not os.path.isfile(input_file):
    print(f"\033[0;31m[ERROR] No se encontro el archivo: {input_file}\033[0m", file=sys.stderr)
    sys.exit(1)

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

tenants = data.get("tenants", [])
os.makedirs(tenants_dir, exist_ok=True)


def sanitize_slug(raw):
    clean = re.sub(r"[^a-z0-9_-]", "-", str(raw or "").strip().lower())
    clean = re.sub(r"-+", "-", clean).strip("-")
    if not clean or clean == "default" or ".." in clean:
        return ""
    return clean


def safe_name(raw):
    s = str(raw or "").strip()
    if not s or "/" in s or "\\" in s or ".." in s or s in (".", ".."):
        return ""
    return re.sub(r"[^a-zA-Z0-9_.-]", "-", s).strip(".")


def wf(fpath, content):
    if content:
        with open(fpath, "w", encoding="utf-8") as out:
            out.write(content)


restored = []
for t in tenants:
    slug = sanitize_slug(t.get("slug"))
    if not slug:
        continue
    tdir = os.path.join(tenants_dir, slug)
    ctx = os.path.join(tdir, "context")
    rules = os.path.join(tdir, "rules")
    tasks = os.path.join(tdir, "tasks")
    proy = os.path.join(tdir, "Proyecto")

    os.makedirs(ctx, exist_ok=True)
    os.makedirs(rules, exist_ok=True)
    os.makedirs(tasks, exist_ok=True)
    os.makedirs(proy, exist_ok=True)

    wf(os.path.join(ctx, "team-context.md"), t.get("team_context"))
    wf(os.path.join(ctx, "tech-context.md"), t.get("tech_context"))
    wf(os.path.join(rules, "company-standards.md"), t.get("company_standards"))
    wf(os.path.join(ctx, "learnings.md"), t.get("learnings"))
    wf(os.path.join(ctx, "project-structure.md"), t.get("project_structure"))
    wf(os.path.join(ctx, "progress.md"), t.get("progress"))
    wf(os.path.join(ctx, "system-patterns.md"), t.get("system_patterns"))

    adrs = t.get("adrs", [])
    if isinstance(adrs, list) and adrs:
        adrs_dir = os.path.join(ctx, "adrs")
        os.makedirs(adrs_dir, exist_ok=True)
        for adr in adrs:
            if not isinstance(adr, dict):
                continue
            afname = safe_name(adr.get("filename"))
            if afname and afname.endswith(".md"):
                wf(os.path.join(adrs_dir, afname), adr.get("content"))

    for r in t.get("repos", []):
        rname = safe_name(r.get("name") if isinstance(r, dict) else r)
        if rname:
            os.makedirs(os.path.join(proy, rname), exist_ok=True)

    restored.append(slug)

act = data.get("active_tenant") or (restored[0] if restored else "")
if act:
    with open(active_file, "w", encoding="utf-8") as f:
        f.write(act)

joined = ", ".join(restored)
print(f"\033[0;32m[OK] Tenants importados exitosamente desde {input_file}\033[0m")
print(f"     Tenants restaurados: {len(restored)} ({joined})")
print(f"     Tenant activo:      {act}")
PY
elif command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT_DIR/import-tenants.ps1" "$@"
else
    echo "Error: Se requiere python3 o pwsh para importar tenants." >&2
    exit 1
fi
