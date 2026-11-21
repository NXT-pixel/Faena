#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Run python script or pwsh if available
if command -v python3 >/dev/null 2>&1; then
    python3 -c "
import os, sys, json
repo_root = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else os.path.join(repo_root, 'tenants.local.json')
tenants_dir = os.path.join(repo_root, 'tenants')
active_file = os.path.join(repo_root, '.active-tenant')

active_tenant = ''
if os.path.isfile(active_file):
    with open(active_file, 'r', encoding='utf-8') as f:
        active_tenant = f.read().strip()

tenants = []
if os.path.isdir(tenants_dir):
    for d in sorted(os.listdir(tenants_dir)):
        p = os.path.join(tenants_dir, d)
        if os.path.isdir(p) and not d.startswith('.'):
            ctx = os.path.join(p, 'context')
            rules = os.path.join(p, 'rules')
            proy = os.path.join(p, 'Proyecto')
            def rf(fpath):
                if os.path.isfile(fpath):
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        return f.read()
                return ''
            repos = []
            if os.path.isdir(proy):
                for r in sorted(os.listdir(proy)):
                    rp = os.path.join(proy, r)
                    if os.path.isdir(rp) and not r.startswith('.'):
                        repos.append({'name': r, 'remote_url': ''})
            tenants.append({
                'slug': d,
                'name': d.replace('-', ' '),
                'team_context': rf(os.path.join(ctx, 'team-context.md')),
                'tech_context': rf(os.path.join(ctx, 'tech-context.md')),
                'company_standards': rf(os.path.join(rules, 'company-standards.md')),
                'learnings': rf(os.path.join(ctx, 'learnings.md')),
                'project_structure': rf(os.path.join(ctx, 'project-structure.md')),
                'progress': rf(os.path.join(ctx, 'progress.md')),
                'system_patterns': rf(os.path.join(ctx, 'system-patterns.md')),
                'repos': repos
            })

payload = {
    'version': '1.0',
    'active_tenant': active_tenant,
    'tenants': tenants
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f'\033[0;32m[OK] Tenants exportados exitosamente a {output_file}\033[0m')
print(f'     Tenants guardados: {len(tenants)}')
" "$REPO_ROOT" "${1:-}"
elif command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT_DIR/export-tenants.ps1" "$@"
else
    echo "Error: Se requiere python3 o pwsh para exportar tenants." >&2
    exit 1
fi
