# CLAUDE.md - Guía de Operación para Claude en Faena

Este repositorio es una factoría de desarrollo contextual. Cuando el usuario pegue un ticket o asigne una tarea en este chat, debes seguir estrictamente las directivas de este archivo y de `AGENTS.md`.

## 1. Dónde reside el código
- El código fuente de la empresa/cliente se encuentra clonado dentro de `Proyecto/` (ej. `Proyecto/backend-api`, `Proyecto/frontend-web`).
- **NUNCA** coloques código de producción fuera de `Proyecto/`.
- Todos los comandos de terminal (`dotnet`, `npm`, `ng`, `pytest`) deben ejecutarse en la subcarpeta del repositorio objetivo dentro de `Proyecto/`.

## 2. Dónde reside el contexto
Antes de proponer una solución o escribir código, consulta obligatoriamente:
- `tasks/context/team-context.md`: Organigrama de la empresa, jefes, compañeros, testers QA, DevOps y protocolo de delegación.
- `tasks/context/tech-context.md`: Stack tecnológico y herramientas.
- `rules/project/`: Estándares de arquitectura obligatorios de esta empresa.
- `skills/`: Habilidades especializadas (Angular en `skills/angular-developer/`, .NET en `skills/dotnet-patterns/` y `skills/csharp-testing/`, ABP en `skills/abp-*/`, Azure en `skills/azure-function/`).

## 3. Protocolo de Comandos por Chat (Drag & Drop)
1. **Paso 1 (`@commands/1-ticket.md`)**: El usuario arrastra el comando y pega el ticket. Lees `tasks/context/team-context.md`, identificas el repo en `Proyecto/` y creas `tasks/design-<nombre>.md`.
2. **Paso 2 (`@commands/2-create-trd.md tasks/design-<nombre>.md`)**: Diseñas la arquitectura y creas `tasks/task-<nombre>/trd-<nombre>.md` y `test-spec-<nombre>.md` con las secciones de handoff para QA y DevOps.
3. **Paso 3 (`@commands/3-create-tasks.md tasks/task-<nombre>/trd-<nombre>.md`)**: Desglosas en tareas atómicas `task01-setup`, `task02-red`, `task03-green` con `README.md` de seguimiento con checkboxes.
4. **Paso 4 (`@tasks/task-<nombre>/taskNN-...`)**: Ejecutas cada tarea en `Proyecto/`. En RED escribes tests y confirmas que fallen en terminal. En GREEN implementas hasta que pasen todos y validas lint/build. Actualizas el checkbox en `README.md`.
5. **Paso 5 (Auditoría ECC Gate & Handoff)**: Revisas el `git diff` con el criterio de `security-reviewer.md`, registras lecciones en `tasks/context/learnings.md` y entregas el resumen listo para el tester QA.
