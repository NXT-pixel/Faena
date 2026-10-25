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

## 3. Protocolo TDD al recibir un Ticket
1. **Comprensión**: Identifica al Tech Lead, QA y DevOps mencionados en `team-context.md`.
2. **Arquitectura (TRD)**: Diseña la solución y crea `tasks/task-<nombre>/trd-<nombre>.md` y `test-spec-<nombre>.md`. Incluye la sección de handoff para QA y DevOps.
3. **Tareas TDD**: Desglosa en tareas atómicas `task01-setup`, `task02-red`, `task03-green` con `README.md` de seguimiento.
4. **Ejecución**: Escribe tests primero (RED) -> Ejecuta y confirma que fallen -> Implementa código (GREEN) -> Ejecuta hasta pasar -> Corre quality gates (VERIFY).
5. **Auditoría de Seguridad (ECC Gate)**: Revisa el `git diff` con el criterio de `security-reviewer.md` para evitar secretos o vulnerabilidades.
6. **Memoria**: Guarda las lecciones aprendidas en `tasks/context/learnings.md`.
