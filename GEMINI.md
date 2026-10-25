# GEMINI.md - Directivas de Contexto para Gemini en Faena

Eres el asistente de IA operando dentro de la factoría de desarrollo Faena. Tu misión es transformar tickets de requerimientos en código probado, seguro y listo para producción, operando directamente dentro de este chat.

## Protocolo Obligatorio:
1. **Revisa el contexto organizacional primero**: Lee `tasks/context/team-context.md` para entender quién es el Tech Lead, el Product Owner, el QA y el DevOps del equipo.
2. **Localiza el código objetivo**: Todo el código de la empresa está en `Proyecto/`. Realiza todas las lecturas, escrituras y ejecuciones de terminal dentro del repositorio correspondiente en `Proyecto/`.
3. **Consulta las habilidades y reglas del proyecto**:
   - `rules/project/`: Reglas obligatorias de la empresa.
   - `skills/`: Referencias técnicas (.NET, Angular, Azure, ABP Framework).
   - `agents/`: Adopta las personas especializadas de `agents/coding/` y `agents/design/`.
4. **Flujo de 5 Pasos**:
   - Paso 1: Lee el ticket e interpreta las responsabilidades (Desarrollo vs. Handoff QA/DevOps).
   - Paso 2: Genera el TRD y la Especificación de Pruebas en `tasks/task-<nombre>/`.
   - Paso 3: Genera las tareas TDD (`task01-setup`, `task02-red`, `task03-green`) con casillas de progreso.
   - Paso 4: Ejecuta los cambios con TDD estricto (RED falla -> GREEN pasa -> VERIFY aprueba).
   - Paso 5: Audita el `git diff` con `security-reviewer.md`, registra las lecciones en `tasks/context/learnings.md` y prepara la entrega para QA.
