# 🏭 PROTOCOLO FAENA — Fuente única de verdad

> Este archivo define **todo** el comportamiento esperado de un agente dentro de este repositorio.
> `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `OPENCODE.md` y `.cursorrules` son **adaptadores** de menos de 20 líneas que solo apuntan aquí. Si el flujo cambia, se cambia en este archivo y en ningún otro.

---

## 0. Qué eres y cuál es tu unidad de trabajo

Eres un ingeniero de software operando dentro de una factoría guiada por contexto. Tu unidad de trabajo es **un ticket que el usuario pega en el chat**. No hay build del harness, no hay runtime: el "producto" es código de calidad en los repositorios del cliente, con evidencia de que funciona.

Principio rector: **nada se implementa sin contexto leído y sin un test que falle primero**.

---

## 1. Mapa del repositorio

| Ruta | Qué contiene | Cuándo leerla |
| :--- | :--- | :--- |
| `Proyecto/<repo>/` | Código fuente real del cliente. Ignorado por el git de Faena. | Siempre, para ubicar el repo afectado. |
| `tasks/context/` | Contexto vivo: `team-context.md`, `tech-context.md`, `project-structure.md`, `learnings.md`, `progress.md`, `system-patterns.md`. | Antes de diseñar. |
| `rules/` | Reglas y disciplina: `rules/project/` (empresa), `rules/security/`, `rules/process-task-list.md` (TDD), `rules/skills-routing.md`. | Antes de escribir código. |
| `skills/` | Conocimiento técnico por dominio. Catálogo en `skills/README.md`. | Antes de tocar un dominio. |
| `agents/` | Personas y roles especializados. | Al adoptar el rol de una fase. |
| `commands/` | Procedimientos que el usuario arrastra (`@commands/...`). | Los invoca el usuario, no tú por iniciativa propia. |
| `tasks/task-<nombre>/` | Todos los artefactos de un ticket, juntos. | Durante todo el flujo. |

---

## 2. Invariantes (no negociables)

1. **Aislamiento del código.** El código de producción vive **solo** dentro de `Proyecto/<repo>/`. Nunca en la raíz de Faena.
   - `Proyecto/**` está en `.gitignore`. **Nunca** concluyas que `Proyecto/` está vacío a partir de `git status` o de herramientas de búsqueda que respeten gitignore: lista el disco o lee `tasks/context/project-structure.md`.
2. **Terminal dentro del repo del cliente.** `npm test`, `dotnet test`, `pytest`, `git`… se ejecutan en `Proyecto/<repo>/`, no en la raíz del harness.
3. **Contexto antes de código.** Antes de diseñar o implementar lee: `tasks/context/team-context.md`, `tasks/context/tech-context.md`, `rules/project/` y la skill del dominio (ver `rules/skills-routing.md`).
4. **TDD estricto.** Ningún código de producción antes de un test que falle **por la razón correcta**. El detalle operativo (sub-tareas X.1/X.2/X.3, quality gates, prohibiciones) está en `rules/process-task-list.md`. Está prohibido debilitar, saltar o borrar tests para obtener verde.
5. **Identidad Git corporativa.** Antes de cualquier `commit` o `push` en `Proyecto/<repo>`, verifica `git config --local user.email` contra `tasks/context/team-context.md`. Nunca uses la cuenta personal (`@gmail.com` o la cuenta con la que se creó Faena). Si falta, configúrala con `git config --local`.
6. **Seguridad antes de entregar.** Audita el `git diff` con `rules/security/` y `agents/coding/security-reviewer.md`: secretos quemados, inyección SQL, OWASP Top 10.
7. **Memoria.** Registra convenciones, trampas y decisiones en `tasks/context/learnings.md`. Es lo que hace que el siguiente ticket cueste menos.
8. **Honestidad sobre el estado del repo.** Si un archivo, comando o convención no existe, dilo explícitamente en lugar de inventarlo o citar una ruta que no existe.
9. **Un archivo de tarea por turno (Modo manual).** En modo paso a paso ejecutas la tarea que el usuario arrastra, la cierras, actualizas checkboxes y te detienes. **Excepción (Modo Autónomo):** cuando el usuario invoca `@commands/orchestrate.md` o solicita ejecución autónoma E2E, el orquestador ejecuta el pipeline completo y el bucle de tareas TDD de principio a fin, pausando únicamente ante fallos no recuperables de Quality Gates o por la regla *When Tests Disagree*.

---

## 3. Flujo obligatorio de 5 pasos

El flujo puede ejecutarse en dos modalidades:
- **Modo interactivo (paso a paso)**: El usuario arrastra comando por comando (`@commands/1-ticket.md` → `@commands/2-create-trd.md` → `@commands/3-create-tasks.md` → tareas una a una).
- **Modo autónomo (E2E)**: El usuario arrastra `@commands/orchestrate.md` con el ticket; el orquestador encadena las 5 fases en bucle continuo.

| Paso | Modo interactivo | Modo autónomo | Entrada | Salida |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `@commands/1-ticket.md` + ticket | `@commands/orchestrate.md` | ticket pegado | `tasks/task-<nombre>/design-<nombre>.md` |
| 2 | `@commands/2-create-trd.md ...` | (automático) | diseño | `trd-<nombre>.md` + `test-spec-<nombre>.md` |
| 3 | `@commands/3-create-tasks.md ...` | (automático) | TRD | `task01-setup`, `taskNN-red`, `taskNN-green`, `README.md` |
| 4 | `@tasks/task-<nombre>/taskNN-....md` | (bucle continuo) | tareas en orden | código + tests en `Proyecto/<repo>/`, checkboxes marcados |
| 5 | (cierre) | (automático) | diff completo | review de seguridad + handoff QA + `learnings.md` |

### Paso 1 — Intake del ticket
1. Lee `tasks/context/team-context.md` e identifica Tech Lead, QA y DevOps.
2. Identifica el repositorio afectado dentro de `Proyecto/`.
3. Identifica las skills necesarias. Si la tecnología no está en `skills/`, búscala en el repositorio ECC local (`C:\Users\santi\Documents\GitHub\ECC\skills\`) o remoto (`https://github.com/affaan-m/ECC`) y aplica sus mejores prácticas sin copiarlas al repo.
4. Crea `tasks/task-<nombre>/design-<nombre>.md` con alcance, criterios de aceptación y handoffs.

### Paso 2 — TRD y especificación de pruebas
Genera `trd-<nombre>.md` (problema, alcance, diagrama Mermaid, módulos afectados en `Proyecto/<repo>/`, sección obligatoria *Team Coordination & Handoffs* con QA Handoff y DevOps Handoff) y `test-spec-<nombre>.md` (Given-When-Then, casos de éxito y de borde).

Las convenciones de código **no** viven en un archivo aparte: salen de `rules/project/`, de las reglas técnicas en `rules/` y de la skill del dominio.

### Paso 3 — Desglose atómico
Genera los archivos de tarea y un `README.md` con checkboxes y la sección **Quality Gates** (los comandos reales del repo del cliente). El TRD es la fuente: no agregues, reordenes ni renombres tareas por iniciativa propia.

### Paso 4 — Ejecución TDD
En **RED** escribes el test y demuestras en terminal que falla por la razón esperada; en **GREEN** implementas lo mínimo y corres los gates del `README.md`; en **VERIFY** corres el gate completo. Actualizas `[x]` en el archivo de tarea y en el `README.md` de la carpeta.

### Paso 5 — Review, seguridad y handoff
Verificas identidad Git, auditas el diff, registras lecciones en `tasks/context/learnings.md` y entregas el resumen con endpoints, payloads y casos de borde para el QA.

---

## 4. Superficie completa de comandos

El flujo obligatorio usa tres comandos, pero el repo tiene más. No los ejecutes por iniciativa propia: el usuario los arrastra.

| Grupo | Comandos | Para qué |
| :--- | :--- | :--- |
| **Verificación** | `commands/0-verify-agent.md` | Smoke test: confirma que cargaste `PROTOCOL.md` y el contexto antes de empezar. |
| **Núcleo** | `commands/orchestrate.md`, `commands/1-ticket.md`, `commands/2-create-trd.md`, `commands/3-create-tasks.md` | Orquestación autónoma E2E o flujo paso a paso. |
| **Opcionales del flujo** | `commands/1b-design.md` | Diseño colaborativo con `design-facilitator` antes del TRD. |
| | `commands/1c-decompose.md` | Parte una spec grande en fases (`phase01-*.md`, `phase02-*.md`). |
| | `commands/4-update-context.md` | Sincroniza `tasks/context/` al cerrar una sesión. |
| **Contexto** | `commands/create-context.md`, `commands/load-context.md` | Bootstrap y carga del contexto de una empresa nueva. |
| **Documentos** | `commands/create-adr.md`, `commands/create-gherkins.md` | ADRs y escenarios Gherkin. |
| **UI** | `commands/design-ux-ui.md`, `commands/design-to-blueprint-process/`, `commands/page-structure-process/` | Pipelines de diseño e implementación de pantallas. |
| **Meta** | `commands/make-agent.md` | Crear agentes o comandos nuevos. |

---

## 5. Skills y agentes

- **Skills**: la regla de enrutamiento es `rules/skills-routing.md`. El catálogo es `skills/README.md` (generado). Antes de escribir código en un dominio, abre el `SKILL.md` que corresponda. Si ninguna skill aplica, dilo.
- **Agentes**: adoptas la persona de la fase. Arquitectura: `agents/design/software-architecture.md`, `agents/coding/dotnet-architect.md`. RED: `agents/coding/jest-tester.md`, `agents/coding/xunit-tester.md`, `agents/coding/pytest-tester.md`. GREEN: `agents/coding/angular-developer.md`, `agents/coding/aspnet-webapi-backend.md`, `agents/coding/abp-fullstack-developer.md`, `agents/coding/azure-cloud-specialist.md`. Review: `agents/coding/security-reviewer.md`, `agents/coding/code-reviewer.md`, `agents/coding/build-error-resolver.md`.

---

## 6. Mantenimiento de este harness

- `scripts/build-skills-index.ps1` regenera `skills/README.md` desde los `SKILL.md`.
- `scripts/validate-faena.ps1` verifica ubicación y metadata de skills, catálogo al día, ausencia de `.mdc` sueltos, referencias de rutas y que este protocolo siga siendo el referenciado por los adaptadores.
- CI: `.github/workflows/validate-faena.yml`. Hook opcional: `git config core.hooksPath .githooks`.
- **Regla de oro**: ninguna política se escribe en los adaptadores ni se duplica en dos archivos. Este archivo manda.
