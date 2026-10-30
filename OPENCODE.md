# OPENCODE.md — Adaptador para OpenCode y modelos locales (Ollama / Qwen)

Fuente única de verdad: [`PROTOCOL.md`](PROTOCOL.md). **Léelo completo antes de actuar.**

## Notas de este host

- Los modelos locales tienen contexto corto: lee `PROTOCOL.md` **por secciones**, empezando por §2 (invariantes) y §3 (flujo). No cargues varias skills a la vez.
- Abre solo el `SKILL.md` del dominio que toca la tarea; los `references/` únicamente si `SKILL.md` los pide para esa tarea.
- Sé conciso en tus respuestas: menos tokens, más señal.
- Si no puedes leer un archivo o ejecutar un comando, dilo explícitamente en lugar de suponer su contenido.

## Atajos

| Necesitas | Lee |
| :--- | :--- |
| Invariantes y flujo | `PROTOCOL.md` §2 y §3 |
| Disciplina TDD | `rules/process-task-list.md` |
| Skills por dominio | `rules/skills-routing.md` + `skills/README.md` |
