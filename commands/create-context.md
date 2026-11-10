---
name: create-context
description: Genera o actualiza el contexto de la empresa en tasks/context/ analizando los repositorios clonados en Proyecto/. Nunca sobrescribe team-context.md ni learnings.md.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 🧭 Comando: create-context (Bootstrap del contexto)

Crea los archivos de contexto que **el resto del harness realmente consume**. No inventa archivos nuevos ni rutas: si algo no se puede detectar, lo deja marcado como pendiente en lugar de rellenarlo con supuestos.

## 1. Archivos que gestiona

| Archivo | Quién lo llena | ¿Se sobrescribe? |
| :--- | :--- | :--- |
| `tasks/context/team-context.md` | Una persona del equipo | **NUNCA** |
| `tasks/context/learnings.md` | La memoria de los tickets | **NUNCA** |
| `tasks/context/tech-context.md` | Este comando (detección) | Sí, con confirmación |
| `tasks/context/project-structure.md` | Este comando (detección) | Sí, con confirmación |
| `tasks/context/progress.md` | Este comando (detección) | Sí, con confirmación |
| `tasks/context/system-patterns.md` | Este comando (detección) | Sí, con confirmación |

`team-context.md` guarda el organigrama y la identidad Git corporativa; `learnings.md` guarda la memoria acumulada. Si cualquiera de los dos existe, **no lo toques** ni siquiera con confirmación: avisa al usuario de que se mantienen intactos.

Las convenciones de código **no** viven aquí. Viven en `rules/project/` y en las skills de cada dominio.

## 2. Preflight

1. Comprueba que `Proyecto/` tenga repositorios. Lista el **disco**, nunca `git status` (está en `.gitignore`):

   ```powershell
   Get-ChildItem Proyecto -Directory | Select-Object -ExpandProperty Name
   ```

   Si no hay ningún repositorio clonado, detente y pide al usuario que clone los repos en `Proyecto/`.

2. Si ya existen `tech-context.md`, `project-structure.md`, `progress.md` o `system-patterns.md`, pregunta: *"Encontré N archivos de contexto. ¿Sobrescribo los detectables? (sí/no)"*. Sin un "sí" explícito, actualiza solo los que falten.

3. Obtén el timestamp real (`date -u +"%Y-%m-%dT%H:%M:%SZ"` o `Get-Date -Format o`). Nunca uses placeholders tipo `[DATE]`.

## 3. Detección por repositorio

Para cada carpeta en `Proyecto/<repo>/`, recoge evidencia real:

- **Manifiestos**: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `*.sln`, `*.csproj`, `Directory.Build.props`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `angular.json`, `Dockerfile`, `docker-compose.yml`.
- **Stack y versiones**: léelas del manifiesto, no las adivines. Anota también el gestor (npm/pnpm/yarn, dotnet, pip/poetry).
- **Comandos de test / build / lint**: tómalos de `scripts` en `package.json`, del nombre de los proyectos de test (`*.Tests.csproj`) o de la configuración de pytest. **Si un comando no lo puedes verificar en el repo, no lo escribas.**
- **Git**: `git -C Proyecto/<repo> remote -v`, `branch --show-current`, `log --oneline -10`.
- **Estructura**: carpetas de primer y segundo nivel, y dónde vive el código de producción frente a los tests.

## 4. Generación de archivos

Frontmatter común para los cuatro archivos detectables:

```yaml
---
created: <timestamp real>
last_updated: <timestamp real>
version: 1.0
author: Faena create-context
---
```

### `tech-context.md`

Una tabla por repositorio: stack principal, versiones, gestor de paquetes y los comandos verificados de test, build y lint. Si no hay repositorios, dilo explícitamente en lugar de dejar el archivo vacío.

### `project-structure.md`

Por repositorio: carpetas clave, dónde está el código de producción, dónde los tests y qué se genera (no se edita a mano). Incluye la lista de repos clonados.

### `progress.md`

Estado actual, rama, últimos commits y siguiente paso. Se regenera con frecuencia; que sea corto.

### `system-patterns.md`

Estilo arquitectónico observado (capas, módulos, monorepo o no), patrones de test y cualquier convención estructural que se pueda **probar leyendo el código**. No inventes patrones.

## 5. Validación

Para cada archivo generado:

- Tiene frontmatter válido y al menos 10 líneas de contenido específico.
- Todo comando mencionado existe en el repositorio del cliente.
- No hay rutas absolutas de la máquina del desarrollador (`C:\Users\...`): siempre `Proyecto/<repo>/...`.
- No se ha tocado `team-context.md` ni `learnings.md`.

Verifica y no dupliques información entre archivos: stack en `tech-context.md`, disposición en `project-structure.md`, patrones en `system-patterns.md`.

## 6. Resumen al usuario

````markdown
📋 Contexto generado en tasks/context/

| Archivo | Estado |
| :--- | :--- |
| tech-context.md | ✅ creado / ♻️ actualizado / ⏭️ omitido |
| project-structure.md | … |
| progress.md | … |
| system-patterns.md | … |
| team-context.md | 🔒 intacto |
| learnings.md | 🔒 intacto |

⏰ <timestamp>
👉 Siguiente paso: arrastra @commands/1-ticket.md y pega el ticket.
````

## 7. Errores frecuentes

- **No hay repos en `Proyecto/`** → detente y pide clonarlos; no generes contexto de un proyecto vacío.
- **No hay permisos de escritura** → informa y no dejes archivos a medias.
- **No puedes detectar el stack** → escribe "pendiente de confirmar" en el archivo y pídelo al usuario. Nunca supongas Angular o .NET por defecto.
