---
name: import-tenants
description: Restaura la configuración, contexto corporativo, reglas y preferencias de tenants desde tenants.local.json tras clonar Faena en una nueva máquina.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 📥 Comando: import-tenants (Restaurar Configuración de Tenants)

Restaura todos tus tenants, contextos, estándares corporativos y espacios de trabajo a partir de un archivo `tenants.local.json` previamente exportado.

Permite clonar Faena en una máquina nueva y reanudar el trabajo de inmediato sin reconfigurar nada y sin subir información confidencial al repositorio Git.

---

## 🎯 Instrucciones para el Asistente

Cuando el usuario invoque `@commands/import-tenants.md`:

1. **Ejecución del Script:**
   - En Windows (PowerShell / CMD):
     ```powershell
     powershell -NoProfile -ExecutionPolicy Bypass -File scripts/import-tenants.ps1
     ```
     o con doble clic en `scripts/import-tenants.cmd`.
   - En Linux / macOS:
     ```bash
     ./scripts/import-tenants.sh
     ```
   - O desde el Companion Dashboard: Clic en **📥 Importar** (puedes arrastrar el archivo o restaurar desde la raíz).

2. **Parámetro Opcional (-CloneRepos):**
   - Si se añade `-CloneRepos`, el script intentará clonar automáticamente aquellos repositorios que cuenten con `remote_url`.

3. **Resultado:**
   - Restaura carpetas `tenants/<slug>/context/`, `rules/`, `tasks/`, `Proyecto/`.
   - Activa el último tenant seleccionado en `.active-tenant`.
   - Informa al usuario que todos los tenants están listos.
