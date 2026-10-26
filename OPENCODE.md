# OPENCODE.md - Directivas para OpenCode y Modelos Locales (Ollama)

Eres el asistente de desarrollo dentro de la factoría de software **Faena**, ejecutándote a través de **OpenCode** (con modelos locales como Ollama / Qwen o modelos cloud).

---

## 🧭 Reglas Fundamentales de Operación

1. **Ubicación del Código del Cliente**:
   - Todo el código fuente de los clientes vive exclusivamente dentro de la carpeta `Proyecto/` (ej. `Proyecto/growthhacking.PrototypeZero/`, `Proyecto/backend-api/`).
   - `Proyecto/**` está ignorado en `.gitignore` para aislar repositorios; **NUNCA** asumas que está vacío por comandos de Git. Inspecciona las carpetas en disco o lee `tasks/context/project-structure.md`.
   - **NUNCA** generes código de producción en la raíz de Faena ni fuera de `Proyecto/`.
   - Todos los comandos de terminal (`dotnet`, `npm`, `pytest`, `git`) deben ejecutarse dentro de la subcarpeta correspondiente en `Proyecto/`.

2. **Contexto Organizacional Obligatorio**:
   - Antes de implementar, consulta `tasks/context/team-context.md` para conocer los roles del equipo (Tech Lead, QA asignado, DevOps).
   - Consulta `rules/project/` para aplicar los estándares de ingeniería de la empresa.

3. **Flujo de Comandos (Drag & Drop o Mencionar en Chat)**:
   - **Paso 1 (`@commands/1-ticket.md`)**: Recibe el ticket y genera `tasks/design-<nombre>.md`.
   - **Paso 2 (`@commands/2-create-trd.md tasks/design-...`)**: Genera la arquitectura técnica `trd-<nombre>.md`, la especificación de pruebas y los handoffs para QA/DevOps.
   - **Paso 3 (`@commands/3-create-tasks.md tasks/task-.../trd-...`)**: Desglosa el trabajo en tareas atómicas (`task01-setup`, `task02-red`, `task03-green`) y crea `README.md`.
   - **Paso 4 (`@tasks/task-.../taskNN-...`)**: Ejecuta cada tarea con disciplina TDD estricta.

4. **Disciplina TDD para Modelos Locales (Ollama / Qwen)**:
   - **En tareas RED**: Solo escribe los archivos de prueba. Ejecuta el comando en terminal (`dotnet test`, `npm test`) y confirma que la prueba falle por la razón esperada. NO implementes la solución aún.
   - **En tareas GREEN**: Implementa la lógica mínima necesaria en `Proyecto/` hasta que todos los tests pasen en verde al 100%. Valida linter y compilación. Marca `[x]` en el `README.md`.

5. **Directivas de Estilo para Modelos Locales**:
   - Sé conciso y directo al grano en tus respuestas para ahorrar tiempo de inferencia y memoria VRAM.
   - No inventes dependencias ni patrones nuevos; sigue estrictamente lo especificado en el TRD.
