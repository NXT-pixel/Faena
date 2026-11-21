#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "===================================================================="
echo "          Iniciando Faena Live Companion Dashboard (Linux)..."
echo "===================================================================="

if command -v python3 >/dev/null 2>&1; then
    python3 scripts/dashboard/server.py
elif command -v python >/dev/null 2>&1; then
    python scripts/dashboard/server.py
else
    echo "[ERROR] No se encontró Python 3 instalado en el sistema." >&2
    echo "Instálalo con: sudo apt install python3 (o el gestor de tu distro)." >&2
    exit 1
fi
