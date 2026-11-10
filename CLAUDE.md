# CLAUDE.md — Adaptador para Claude Code

Fuente única de verdad: [`PROTOCOL.md`](PROTOCOL.md). **Léelo completo antes de actuar**; este archivo no repite sus reglas.

## Notas de este host

- Claude Code carga `CLAUDE.md` automáticamente en cada sesión.
- `CLAUDE.md` **no** se hereda a los subagentes: al delegar, pásales la ruta o el contenido de `PROTOCOL.md`.
- Plan mode y `TodoWrite` son bienvenidos para organizar el trabajo, pero el plan debe respetar las invariantes de `PROTOCOL.md` §2.
- Si el proyecto define `AGENTS.md`, ambos apuntan al mismo protocolo: no hay dos versiones que reconciliar.

## Atajos

| Necesitas | Lee |
| :--- | :--- |
| Flujo de 5 pasos | `PROTOCOL.md` §3 |
| Disciplina TDD | `rules/process-task-list.md` |
| Skills por dominio | `rules/skills-routing.md` + `skills/README.md` |
| Estándares de la empresa | `rules/project/` |
