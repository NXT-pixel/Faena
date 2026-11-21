---
name: switch-tenant
description: Consulta o cambia el tenant activo de trabajo en Faena para dirigir el contexto y la ejecución de tickets al cliente seleccionado.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 🔄 Comando: switch-tenant (Cambiar de Tenant Activo)

Usa este comando para alternar entre diferentes empresas o proyectos aislados dentro de Faena.

---

## 🎯 Instrucciones para el Asistente

Cuando el usuario invoque `@commands/switch-tenant.md [nombre-tenant]`:

1. **Si no se proporciona nombre:**
   - Lista los tenants existentes en `tenants/` y muestra cuál está activo según `.active-tenant`.
2. **Si se proporciona un nombre:**
   - Verifica que exista `tenants/<nombre-tenant>/`.
   - Actualiza el archivo `.active-tenant` en la raíz con el nombre del tenant seleccionado.
   - Confirma el cambio indicando que el orquestador y el dashboard ahora operan sobre:
     - `tenants/<nombre-tenant>/context/`
     - `tenants/<nombre-tenant>/Proyecto/`
     - `tenants/<nombre-tenant>/tasks/`
