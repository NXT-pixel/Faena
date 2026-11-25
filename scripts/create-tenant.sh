#!/usr/bin/env bash
set -euo pipefail

RAW_TENANT="${1:-}"
TENANT="$(printf '%s' "$RAW_TENANT" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9_-]+/-/g; s/^-+//; s/-+$//')"
if [ -z "$TENANT" ] || [ "$TENANT" = "default" ]; then
    echo "Uso: $0 <nombre-del-tenant> (slug valido distinto de 'default')" >&2
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

NOW_ISO="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat <<EOF > "$TENANT_DIR/context/team-context.md"
# Team Context — $TENANT

**Tenant:** \`$TENANT\`
**Fecha de Creacion:** $NOW_ISO

---

## 1. Identidad Git Corporativa
- **Email Corporativo:** \`developer@$TENANT.local\` (configurar en Proyecto/<repo> con git config --local user.email)
- **Nombre:** Desarrollador Faena
- **Prefijo de rama:** \`feature/\`

## 2. Organigrama y Roles
- **Tech Lead:** [Nombre del Tech Lead] (alineacion tecnica y arquitectura)
- **QA:** [Nombre del QA] (criterios de aceptacion y testing)
- **DevOps:** [Nombre de DevOps] (secretos, pipelines y despliegue)

## 3. Protocolo de Handoff
Todo ticket debe culminar con un resumen de handoff claro para QA y DevOps.
EOF

cat <<EOF > "$TENANT_DIR/context/tech-context.md"
# Tech Context — $TENANT

**Tenant:** \`$TENANT\`

---

## 1. Stack Tecnologico Principal
- **Backend:** [Ej. .NET 8 / ASP.NET Core, Node.js, FastAPI]
- **Frontend:** [Ej. Angular 18, React, Vue]
- **Base de Datos:** [Ej. SQL Server, PostgreSQL, CosmosDB]
- **Gestores de Paquetes:** [dotnet, npm, pnpm]

## 2. Comandos de Calidad (Quality Gates de Referencia)
- **Build:** [Ej. dotnet build / npm run build]
- **Tests unitarios:** [Ej. dotnet test / npm test]
EOF

cat <<EOF > "$TENANT_DIR/context/project-structure.md"
# Project Structure — $TENANT

**Tenant:** \`$TENANT\`

---

## Repositorios Clonados en Proyecto/
Los repositorios del cliente viven dentro de \`tenants/$TENANT/Proyecto/<repo>/\`.

- *(Aun no hay repositorios clonados. Clona los repositorios del cliente aqui).*
EOF

cat <<EOF > "$TENANT_DIR/context/learnings.md"
# Continuous Memory & Learnings — $TENANT

**Tenant:** \`$TENANT\`
Registra aqui convenciones, trampas y decisiones de diseno especificas de este tenant para acelerar tickets futuros.

---

## Convenciones y Decisiones
- *(Pendiente de primeros tickets)*
EOF

cat <<EOF > "$TENANT_DIR/context/progress.md"
# Project Progress — $TENANT

**Tenant:** \`$TENANT\`
**Estado:** Inicializado y listo para recibir tickets.
EOF

cat <<EOF > "$TENANT_DIR/context/system-patterns.md"
# System Patterns — $TENANT

**Tenant:** \`$TENANT\`
Patrones arquitectonicos y de diseno aprobados para este tenant.
EOF

cat <<EOF > "$TENANT_DIR/rules/company-standards.md"
# Company Standards — $TENANT

Estandares de ingenieria obligatorios para el cliente \`$TENANT\`.
- Convencion de ramas: \`feature/TICKET-descripcion\`
- Cobertura de pruebas minima: Requerida en cada PR (disciplina TDD)
- Prohibido quemar secretos o cadenas de conexion
EOF

echo "[OK] Tenant '$TENANT' creado exitosamente."
