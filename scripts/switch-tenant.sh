#!/usr/bin/env bash
set -euo pipefail

RAW_TENANT="${1:-}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ACTIVE_FILE="$REPO_ROOT/.active-tenant"
TENANTS_DIR="$REPO_ROOT/tenants"

if [ -z "$RAW_TENANT" ]; then
    echo "============================================================"
    echo "              Tenants Disponibles en Faena"
    echo "============================================================"
    CURRENT=""
    if [ -f "$ACTIVE_FILE" ]; then
        CURRENT="$(tr -d '[:space:]' < "$ACTIVE_FILE")"
    fi

    if [ ! -d "$TENANTS_DIR" ]; then
        echo "No hay tenants creados todavia en tenants/."
    else
        for dir in "$TENANTS_DIR"/*; do
            if [ -d "$dir" ]; then
                tname="$(basename "$dir")"
                if [ "$tname" = "$CURRENT" ]; then
                    echo "  [ACTIVO] * $tname ($dir)"
                else
                    echo "           $tname ($dir)"
                fi
            fi
        done
    fi
    echo "------------------------------------------------------------"
    echo "Uso: $0 <nombre-del-tenant> para activar uno (o 'default')."
    exit 0
fi

TENANT="$(printf '%s' "$RAW_TENANT" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9_-]+/-/g; s/^-+//; s/-+$//')"
if [ -z "$TENANT" ]; then
    echo "Error: Nombre de tenant invalido." >&2
    exit 1
fi

if [ "$TENANT" = "default" ]; then
    printf 'default' > "$ACTIVE_FILE"
    echo "[OK] Tenant activo cambiado a: default (raiz)"
    exit 0
fi

TARGET_DIR="$TENANTS_DIR/$TENANT"
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: El tenant '$TENANT' no existe en tenants/$TENANT." >&2
    echo "Crea el tenant con: ./scripts/create-tenant.sh $TENANT" >&2
    exit 1
fi

printf '%s' "$TENANT" > "$ACTIVE_FILE"
echo "[OK] Tenant activo cambiado a: $TENANT"
echo "  Ubicacion: tenants/$TENANT/"
