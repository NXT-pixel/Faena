---
name: export-tenants
description: Exporta la configuración, contexto, reglas y preferencias de todos los tenants a tenants.local.json (ignorado por Git) para transferirlos a otra máquina.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 📤 Comando: export-tenants (Exportar Configuración de Tenants)

Exporta todos los espacios de trabajo, preferencias corporativas, memoria técnica y repositorios registrados a un archivo JSON portable (`tenants.local.json`).

> [!IMPORTANT]
> El archivo `tenants.local.json` está estrictamente ignorado por `.gitignore`. Nunca se versiona en Git, protegiendo credenciales y datos confidenciales. Puedes transferirlo de forma manual y segura a otra computadora.

---

## 🎯 Instrucciones para el Asistente

Cuando el usuario invoque `@commands/export-tenants.md`:

1. **Ejecución del Script:**
   - En Windows (PowerShell / CMD):
     ```powershell
     powershell -NoProfile -ExecutionPolicy Bypass -File scripts/export-tenants.ps1
     ```
     o con doble clic en `scripts/export-tenants.cmd`.
   - En Linux / macOS:
     ```bash
     ./scripts/export-tenants.sh
     ```
   - O desde el Companion Dashboard: Clic en **📤 Exportar**.

2. **Resultado Esperado:**
   - Se genera `tenants.local.json` en la raíz de Faena.
   - Informa al usuario cuántos tenants fueron guardados y que el archivo está listo para ser transferido a otra PC.
