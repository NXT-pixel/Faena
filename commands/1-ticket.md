---
name: ticket
description: Inicia el flujo de trabajo procesando un ticket o requerimiento pegado por el usuario en el chat. Carga el contexto del equipo, identifica los repositorios en Proyecto/ y genera la carpeta del ticket con el documento de diseño y requerimientos en tasks/task-<nombre>/design-<nombre>.md.
agent: agents/design/design-facilitator.md
tools: Read, Write, Bash, LS
---

# 🎫 Comando: 1-ticket (Intake de Requerimientos)

Usa este comando cuando quieras arrastrar un comando al chat y pegar el texto de un ticket (Jira, Azure DevOps, correo o mensaje del Tech Lead).

---

## 🎯 Instrucciones para el Asistente de IA

Cuando el usuario invoque o arrastre `@commands/1-ticket.md` y pegue la descripción de un ticket:

### 1. Lectura Obligatoria de Contexto
Antes de responder, resuelve las rutas según `.active-tenant` (`PROTOCOL.md` §1; raíz si no existe o vale `default`, o `tenants/<tenant>/` si hay un tenant activo):
1. **Contexto de Equipo**: Lee `tasks/context/team-context.md` (o `tenants/<tenant>/context/team-context.md`) para identificar:
   - Quién es el **Tech Lead** (para consultar o alinear decisiones).
   - Quién es el **QA** asignado (para saber qué pruebas delegar o preparar).
   - Quién es el **DevOps** (para configuración de variables o infraestructura).
2. **Contexto de Código**: Inspecciona la carpeta `Proyecto/` (o `tenants/<tenant>/Proyecto/`) para determinar qué repositorio existente será afectado.
3. **Reglas de la Empresa**: Revisa `rules/project/` (o `tenants/<tenant>/rules/`) para aplicar estándares corporativos obligatorios.

### 2. Análisis del Ticket
Extrae del texto pegado:
- **Objetivo de Negocio**: ¿Qué problema resuelve y para quién?
- **Alcance (In Scope / Out of Scope)**: Qué se debe programar en `Proyecto/` y qué queda fuera.
- **Historias de Usuario y Criterios de Aceptación (AC)**.
- **Delegación de Responsabilidades**:
  - ¿Hay tareas que corresponden a QA (ej. pruebas de regresión manuales, carga)?
  - ¿Hay tareas de DevOps (ej. secretos en KeyVault, variables en CI/CD)?
  - ¿Hay dependencias con otros desarrolladores?

### 3. Generar el Documento de Requerimientos en su Carpeta Dedicada
Crea la carpeta del ticket y el archivo de diseño dentro de ella:
`tasks/task-<nombre-del-ticket>/design-<nombre-del-ticket>.md` (usa un slug descriptivo en minúsculas, ej. `tasks/task-auth-login-flow/design-auth-login-flow.md`).
*(De esta forma, todos los artefactos del requerimiento —diseño, TRD, especificación de pruebas y tareas TDD— residirán juntos dentro de `tasks/task-<nombre>/`).*

#### Estructura del Documento `tasks/task-<nombre>/design-<nombre>.md`:
```markdown
# Requerimientos y Diseño: [Nombre del Requerimiento]

**Fecha:** [Fecha actual]
**Ticket Origen:** [Identificador o resumen del ticket]
**Repositorio Afectado:** `Proyecto/[repo]/` (o `tenants/[tenant]/Proyecto/[repo]/`)
**Branch:** `[rama Git del ticket, si aplica]`

---

## 1. Resumen Ejecutivo y Objetivos
[Explicación clara del propósito y valor del requerimiento]

## 2. Personas y Actores
- **Usuario Final / Rol**: [Quién interactúa]
- **Equipo Interno**:
  - Tech Lead: [Nombre desde team-context.md]
  - QA Asignado: [Nombre desde team-context.md]
  - DevOps: [Nombre desde team-context.md]

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)
- **Escenario 1**: [Título]
  - **Dado** [contexto inicial]
  - **Cuando** [acción]
  - **Entonces** [resultado esperado]
- **Escenario 2**: ...

## 4. Alcance Técnico
- **En Alcance (In Scope)**:
  - [Componentes, endpoints o módulos a modificar en Proyecto/]
- **Fuera de Alcance (Out of Scope)**:
  - [Cosas que no se tocarán en este ticket]

## 5. Coordinación de Equipo y Delegaciones
- **Handoff a QA ([Nombre QA])**: Criterios de validación y escenarios clave a certificar.
- **Handoff a DevOps ([Nombre DevOps])**: Variables de entorno o infraestructura necesaria.

## 6. Próximo Paso
Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:
Arrastra al chat:
`@commands/2-create-trd.md <tasks_dir>/task-[nombre]/design-[nombre].md`
```

### 4. Respuesta al Usuario
1. Confirma la creación de `<tasks_dir>/task-<nombre>/design-<nombre>.md` (en `tasks/` para `default`, o `tenants/<tenant>/tasks/` según `.active-tenant`).
2. Presenta un breve resumen de lo comprendido (máximo 5-8 viñetas).
3. Indica el siguiente comando a arrastrar:
   > 👉 **Siguiente paso:** Arrastra al chat `@commands/2-create-trd.md <tasks_dir>/task-<nombre>/design-<nombre>.md`
