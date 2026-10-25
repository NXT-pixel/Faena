# GEMINI.md - Directivas de Contexto para Gemini en Faena

Eres el asistente de IA operando dentro de la factoría de desarrollo Faena. Tu misión es transformar tickets de requerimientos en código probado, seguro y listo para producción, operando directamente dentro de este chat.

## Protocolo Obligatorio:
1. **Revisa el contexto organizacional primero**: Lee `tasks/context/team-context.md` para entender quién es el Tech Lead, el Product Owner, el QA y el DevOps del equipo.
2. **Localiza el código objetivo**: Todo el código de la empresa está en `Proyecto/`. `Proyecto/**` está en `.gitignore` para aislar repositorios; NUNCA uses `git status` para saber si `Proyecto/` está vacío, verifica carpetas en disco o en `project-structure.md`. Realiza todas las lecturas, escrituras y ejecuciones de terminal dentro del repositorio correspondiente en `Proyecto/`.
3. **Consulta las habilidades y reglas del proyecto**:
   - `rules/project/`: Reglas obligatorias de la empresa.
   - `skills/`: Referencias técnicas (.NET, Angular, Azure, ABP Framework).
   - `agents/`: Adopta las personas especializadas de `agents/coding/` y `agents/design/`.
4. **Flujo de Comandos Arrastrables en el Chat**:
   - **Paso 1**: El usuario arrastra `@commands/1-ticket.md` y pega el ticket -> Genera `tasks/design-<nombre>.md` con el alcance y contexto del equipo.
   - **Paso 2**: El usuario arrastra `@commands/2-create-trd.md tasks/design-<nombre>.md` -> Genera `trd-<nombre>.md` y `test-spec-<nombre>.md` en `tasks/task-<nombre>/`.
   - **Paso 3**: El usuario arrastra `@commands/3-create-tasks.md tasks/task-<nombre>/trd-<nombre>.md` -> Genera `task01-setup`, `task02-red`, `task03-green` y `README.md`.
   - **Paso 4**: El usuario arrastra cada tarea `@tasks/task-<nombre>/taskNN-...` -> Ejecuta el cambio TDD en `Proyecto/` (RED falla -> GREEN pasa -> VERIFY aprueba) y actualiza el checkbox.
   - **Paso 5**: Audita el `git diff` con `security-reviewer.md`, registra lecciones en `tasks/context/learnings.md` y entrega el handoff para QA.
