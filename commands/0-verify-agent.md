---
name: 0-verify-agent
description: Smoke test previo a cualquier ticket. Comprueba que el agente cargó el protocolo y el contexto antes de trabajar, para no descubrirlo a mitad del primer ticket.
---

# ✅ Comando: 0-verify-agent (smoke test)

Arrastra este comando **antes** del primer ticket de una sesión. Sirve para una sola cosa: saber si tu agente realmente leyó el protocolo y el contexto, o si está improvisando.

## Instrucciones para el asistente

Responde a las cinco preguntas leyendo los archivos indicados (resolviendo rutas según `.active-tenant` en `PROTOCOL.md` §1 si hay un tenant distinto de `default`). **No respondas de memoria ni supongas**: si no puedes leer un archivo, dilo.

1. **`PROTOCOL.md` §2** — nombra las invariantes de aislamiento de código y explica por qué no puedes concluir que `Proyecto/` (o `tenants/<tenant>/Proyecto/`) está vacío usando `git status`.
2. **`rules/skills-routing.md`** — ¿dónde viven las skills, dónde está el catálogo y qué debes hacer antes de escribir código en un dominio?
3. **`PROTOCOL.md` §3** — ¿qué comando genera el TRD y qué dos archivos produce, en qué carpeta?
4. **`PROTOCOL.md` §2** y `rules/project/` (o `tenants/<tenant>/rules/`) — ¿qué debes verificar antes de un `commit` o `push` en el repo del cliente y de dónde sale ese valor?
5. **`tasks/context/team-context.md`** (o `tenants/<tenant>/context/team-context.md`) — ¿quién es el Tech Lead y quién el QA? Si los campos siguen vacíos, di exactamente eso.

## Formato de respuesta

```markdown
| # | Comprobación | Resultado |
| :--- | :--- | :--- |
| 1 | Aislamiento de Proyecto/ | ✅ / ❌ |
| 2 | Skills y su enrutamiento | ✅ / ❌ |
| 3 | TRD: comando y salidas | ✅ / ❌ |
| 4 | Verificación previa a commit | ✅ / ❌ |
| 5 | Tech Lead y QA | ✅ / ⚠️ sin rellenar |

**PROTOCOLO CARGADO: SÍ / NO**
```

## Qué hacer con el resultado

- **SÍ, las cinco en ✅** → sigue con `@commands/1-ticket.md` (o `@commands/orchestrate.md` para modo autónomo).
- **Alguna ❌** → tu host no está cargando el adaptador. Pega el contenido de `PROTOCOL.md` al inicio del chat y repite este comando. No empieces un ticket en ese estado.
- **⚠️ en la 5** → el protocolo está cargado pero el contexto del equipo no: rellena `team-context.md` en la carpeta de contexto del tenant activo antes de continuar.
