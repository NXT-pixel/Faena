---
name: ticket
description: Inicia el flujo de trabajo procesando un ticket o requerimiento pegado por el usuario en el chat. Carga el contexto del equipo, identifica los repositorios en Proyecto/ y genera el documento de diseño y requerimientos en tasks/design-<nombre>.md.
agent: /agents/design/design-facilitator.md
tools: Read, Write, Bash, LS
---

# 🎫 Comando: ticket (Intake de Requerimientos)

Usa este comando cuando quieras arrastrar un comando al chat y pegar el texto de un ticket (Jira, Azure DevOps, correo o mensaje del Tech Lead).

---

## 🎯 Instrucciones para el Asistente de IA

Cuando el usuario invoque o arrastre `@commands/ticket.md` y pegue la descripción de un ticket:

### 1. Lectura Obligatoria de Contexto
Antes de responder:
1. **Contexto de Equipo**: Lee `tasks/context/team-context.md` para identificar:
   - Quién es el **Tech Lead** (para consultar o alinear decisiones).
   - Quién es el **QA** asignado (para saber qué pruebas delegar o preparar).
   - Quién es el **DevOps** (para configuración de variables o infraestructura).
2. **Contexto de Código**: Inspecciona la carpeta `Proyecto/` para determinar qué repositorio o proyecto existente será afectado (ej. `Proyecto/backend-api`, `Proyecto/frontend-web`).
3. **Reglas de la Empresa**: Revisa `rules/project/` para aplicar estándares corporativos obligatorios.

### 2. Análisis del Ticket
Extrae del texto pegado:
- **Objetivo de Negocio**: ¿Qué problema resuelve y para quién?
- **Alcance (In Scope / Out of Scope)**: Qué se debe programar en `Proyecto/` y qué queda fuera.
- **Historias de Usuario y Criterios de Aceptación (AC)**.
- **Delegación de Responsabilidades**:
  - ¿Hay tareas que corresponden a QA (ej. pruebas de regresión manuales, carga)?
  - ¿Hay tareas de DevOps (ej. secretos en KeyVault, variables en CI/CD)?
  - ¿Hay dependencias con otros desarrolladores?

### 3. Generar el Documento de Requerimientos
Crea el archivo en:
`tasks/design-<nombre-del-ticket>.md` (usa un slug descriptivo en minúsculas, ej. `tasks/design-auth-login-flow.md`).

#### Estructura del Documento `tasks/design-<nombre>.md`:
```markdown
# Requerimientos y Diseño: [Nombre del Requerimiento]

**Fecha:** [Fecha actual]
**Ticket Origen:** [Identificador o resumen del ticket]
**Repositorio Afectado:** `Proyecto/[repo]/`

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
`@commands/create-trd.md tasks/design-[nombre].md`
```

### 4. Respuesta al Usuario
1. Confirma la creación de `tasks/design-<nombre>.md`.
2. Presenta un breve resumen de lo comprendido (máximo 5-8 viñetas).
3. Indica el siguiente comando a arrastrar:
   > 👉 **Siguiente paso:** Arrastra al chat `@commands/create-trd.md tasks/design-<nombre>.md`
