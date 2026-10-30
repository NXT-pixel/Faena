# 🎫 Tickets y tareas

Aquí vive el trabajo de la empresa/cliente, separado del código (que está en `Proyecto/`).

## Dos carpetas, dos propósitos

| Carpeta | Qué guarda | Quién escribe |
| :--- | :--- | :--- |
| `tickets/` | El texto original del ticket tal como llegó (Jira, Azure DevOps, correo). Histórico, no se edita | Cualquiera, a mano |
| `task-<nombre>/` | Todos los artefactos de un ticket en curso, desde el diseño hasta los tests | Los comandos del flujo |

## Anatomía de `task-<nombre>/`

| Archivo | Lo genera | Contenido |
| :--- | :--- | :--- |
| `design-<nombre>.md` | `commands/1-ticket.md` | Alcance, criterios de aceptación, personas, handoffs |
| `trd-<nombre>.md` | `commands/2-create-trd.md` | Arquitectura, módulos, *Team Coordination & Handoffs* |
| `test-spec-<nombre>.md` | `commands/2-create-trd.md` | Escenarios Given-When-Then |
| `taskNN-setup-*.md`, `taskNN-red-*.md`, `taskNN-green-*.md` | `commands/3-create-tasks.md` | Una tarea atómica por archivo |
| `README.md` | `commands/3-create-tasks.md` | Índice con checkboxes y la sección **Quality Gates** |

Un ticket completo tiene los cinco tipos. Si falta el TRD o el test spec, el ticket está a medias: el estado real se ve en el dashboard.

## Ver el estado

```powershell
.\scripts\index-tasks.cmd
```

Genera `tasks/INDEX.md` (local, no versionado) con una fila por ticket: artefactos que tiene, tareas hechas y fecha de última modificación.

> El índice **no se commitea** a propósito: es distinto en cada rama y en cada máquina, así que versionarlo solo produce conflictos. Se regenera cuando lo necesitas.
