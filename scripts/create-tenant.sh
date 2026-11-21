#!/usr/bin/env bash
set -euo pipefail

TENANT="${1:-}"
if [ -z "$TENANT" ]; then
    echo "Uso: $0 <nombre-del-tenant>" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TENANT_DIR="$REPO_ROOT/tenants/$TENANT"

if [ -d "$TENANT_DIR" ]; then
    echo "Aviso: El tenant '$TENANT' ya existe en $TENANT_DIR"
    exit 0
fi

echo "Inicializando tenant '$TENANT'..."
mkdir -p "$TENANT_DIR/context" "$TENANT_DIR/rules" "$TENANT_DIR/tasks" "$TENANT_DIR/Proyecto"
touch "$TENANT_DIR/tasks/.gitkeep" "$TENANT_DIR/Proyecto/.gitkeep"

cat <<EOF > "$TENANT_DIR/context/team-context.md"
# Team Context — $TENANT

**Tenant:** \`$TENANT\`

## 1. Identidad Git Corporativa
- **Email Corporativo:** \`developer@$TENANT.local\`
- **Nombre:** Desarrollador Faena

## 2. Organigrama y Roles
- **Tech Lead:** [Nombre]
- **QA:** [Nombre]
- **DevOps:** [Nombre]
EOF

cat <<EOF > "$TENANT_DIR/context/tech-context.md"
# Tech Context — $TENANT
**Tenant:** \`$TENANT\`
EOF

cat <<EOF > "$TENANT_DIR/context/learnings.md"
# Continuous Memory & Learnings — $TENANT
**Tenant:** \`$TENANT\`
EOF

cat <<EOF > "$TENANT_DIR/rules/company-standards.md"
# Company Standards — $TENANT
EOF

echo "[OK] Tenant '$TENANT' creado exitosamente."
EOF
