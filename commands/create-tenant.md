---
name: create-tenant
description: Inicializa un nuevo tenant (empresa, cliente o proyecto aislado) dentro de tenants/<nombre>/ con su propio contexto, reglas, tareas y repositorio Proyecto/ aislado.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 🏢 Comando: create-tenant (Inicializar Nuevo Tenant)

Usa este comando para crear un espacio de trabajo completamente aislado para un nuevo cliente o proyecto, sin tener que clonar otro repositorio de Faena.

---

## 🎯 Instrucciones para el Asistente

Cuando el usuario invoque `@commands/create-tenant.md <nombre-tenant>`:

1. **Validación del Nombre:**
   - Convierte el nombre a minúsculas en formato slug (ej. `fintech-corp`, `ecommerce-v2`).
2. **Ejecución o Creación:**
   - Ejecuta el script de inicialización:
     ```powershell
     powershell -NoProfile -ExecutionPolicy Bypass -File scripts/create-tenant.ps1 -TenantName "<nombre-tenant>"
     ```
   - O crea directamente la estructura en `tenants/<nombre-tenant>/`:
     - `context/` (`team-context.md`, `tech-context.md`, `project-structure.md`, `learnings.md`, `progress.md`, `system-patterns.md`)
     - `rules/` (`company-standards.md`)
     - `tasks/`
     - `Proyecto/`
3. **Respuesta al Usuario:**
   - Informa las rutas creadas en `tenants/<nombre-tenant>/`.
   - Recuerda clonar los repositorios del cliente en `tenants/<nombre-tenant>/Proyecto/<repo>/`.
   - Indica el comando para activarlo: `@commands/switch-tenant.md <nombre-tenant>`.
