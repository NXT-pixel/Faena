# 📏 Reglas del harness

Las reglas son **instrucciones operativas**, no conocimiento de dominio: eso vive en [`skills/`](../skills/). `PROTOCOL.md` §2 las invoca como fuente de las invariantes; este índice dice cuál aplica y cuándo leerla.

## Núcleo (las usa el flujo de un ticket)

| Regla | Qué impone | Cuándo se lee |
| :--- | :--- | :--- |
| [`process-task-list.md`](process-task-list.md) | RED → GREEN → VERIFY, gates definidos por el repo y prohibiciones (no debilitar tests) | Al ejecutar cada `taskNN-*.md` |
| [`skills-routing.md`](skills-routing.md) | Abrir el `SKILL.md` del dominio antes de escribir código | Antes de implementar |
| [`project/`](project/) | Estándares de la empresa. Es la máxima prioridad; `company-standards.md` es el punto de partida | Antes de diseñar el TRD |
| [`security/`](security/) | OWASP, secretos y checklist previo al commit (`security.md`, `angular-security.md`, `csharp-security.md`) | Antes de commit o de un review |
| [`code-review/code-review.md`](code-review/code-review.md) | Criterio de revisión de código | En el paso 5 |

## Por stack (aplican según el repo del cliente)

| Regla | Cuándo se lee |
| :--- | :--- |
| [`angular.md`](angular.md) | Repos Angular |
| [`dotnet.md`](dotnet.md) | Repos .NET / C# |
| [`abp.md`](abp.md) | Proyectos sobre ABP Framework |
| [`python-maf-azurefunctions.md`](python-maf-azurefunctions.md) | Python MAF sobre Azure Functions |
| [`local-dev-docker.md`](local-dev-docker.md) | Levantar contenedores del repo del cliente en `Proyecto/` |

## Transversales

| Regla | Cuándo se lee |
| :--- | :--- |
| [`no-meta-commentary.md`](no-meta-commentary.md) | Al escribir documentación o comentarios: valor de uso, no historia de creación |

## Cómo se agrega una regla

1. Un `.md` en `rules/` — o en `rules/project/` si es específica de la empresa.
2. Si aplica solo a ciertas rutas, anota el glob en el front matter (`globs:`). Documenta la intención aunque ningún host lo use todavía.
3. Añádela a la tabla de arriba. Si no está en este índice, nadie la va a leer.

> Las reglas de estilo de vida breve, sin referencia desde ningún comando, son deuda: o se indexan aquí o se borran.
