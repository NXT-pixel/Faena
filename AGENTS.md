# 🏭 Faena — Adaptador para agentes (`AGENTS.md`)

Este repositorio tiene **un solo protocolo**: [`PROTOCOL.md`](PROTOCOL.md), en la raíz.

**Antes de actuar, lee `PROTOCOL.md` completo.** Ahí están el mapa del repo, las invariantes no negociables (aislamiento de `Proyecto/`, TDD, identidad Git, skills), el flujo de 5 pasos y la superficie completa de comandos.

## Regla de este archivo

No copies reglas aquí. Este archivo es un **adaptador**: si el flujo cambia, se edita `PROTOCOL.md` y este archivo no se toca. `scripts/validate-faena.ps1` falla si este adaptador deja de apuntar a `PROTOCOL.md`.

## Notas de este host

- `AGENTS.md` lo leen automáticamente Cursor, Claude Code, Codex, Gemini CLI, OpenCode y DeepSeek Harness.
- Los subagentes y delegados **no** heredan este archivo: pásales la ruta (o el contenido) de `PROTOCOL.md`.
- Los comandos se arrastran al chat: `@commands/...`, `@tasks/task-.../...`.

## Atajos

| Necesitas | Lee |
| :--- | :--- |
| Flujo, fases e invariantes | `PROTOCOL.md` |
| Disciplina TDD (RED-GREEN-VERIFY) | `rules/process-task-list.md` |
| Qué skill usar antes de escribir código | `rules/skills-routing.md` + `skills/README.md` |
| Estándares de la empresa | `rules/project/` |
| Organigrama y handoffs | `tasks/context/team-context.md` |
