---
name: update-context
description: Actualiza la documentación de contexto en tasks/context/ para reflejar el estado actual de los repositorios en Proyecto/ y del equipo.
agent: agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

# 🔄 Comando: update-context (Actualización de Contexto)

Actualiza los archivos de contexto en `tasks/context/` para mantener sincronizada la memoria del asistente de IA con los cambios de código en `Proyecto/`, la evolución de dependencias y los nuevos aprendizajes del equipo.

---

## 🎯 Instrucciones para el Asistente de IA

### 1. Ubicación del Contexto
Resuelve las rutas según `.active-tenant` (`PROTOCOL.md` §1): por defecto en `tasks/context/` (y `Proyecto/`), o en `tenants/<tenant>/context/` (y `tenants/<tenant>/Proyecto/`) si existe un tenant activo distinto de `default`:
- `tasks/context/team-context.md` (Organigrama del equipo, roles y delegación)
- `tasks/context/tech-context.md` (Stack tecnológico real detectado en `Proyecto/`)
- `tasks/context/project-structure.md` (Estructura de carpetas y repositorios en `Proyecto/`)
- `tasks/context/learnings.md` (Memoria acumulada, convenciones y trucos aprendidos)
- `tasks/context/progress.md` (Progreso de tareas y tickets completados)
- `tasks/context/system-patterns.md` (Patrones de arquitectura aplicados)

---

## 🔍 Paso 1: Análisis Sistemático de `Proyecto/`

En Faena, el código fuente del cliente se encuentra **exclusivamente dentro de la carpeta `Proyecto/`**.

### 1.1 Detección de Repositorios en `Proyecto/`
- Inspecciona las subcarpetas dentro de `Proyecto/`:
  - ¿Qué repositorios o proyectos están clonados? (ej. `Proyecto/backend-api`, `Proyecto/frontend-web`, etc.)
- Para cada repositorio en `<proyecto_dir>/` (`Proyecto/` o `tenants/<tenant>/Proyecto/` según `.active-tenant`):
  - Si tiene su propio `.git`, consulta sus cambios recientes:
    ```bash
    git -C <proyecto_dir>/<repo> status --short
    git -C <proyecto_dir>/<repo> log --oneline -5
    ```

### 1.2 Detección de Cambios en Dependencias en `Proyecto/`
Revisa si se han agregado o actualizado paquetes en las subcarpetas de `Proyecto/`:
- **Node.js / Angular / React / Vue**: Busca archivos `package.json` dentro de `Proyecto/`
- **.NET / C#**: Busca archivos `*.csproj` o `*.sln` dentro de `Proyecto/`
- **Python**: Busca `requirements.txt` o `pyproject.toml` dentro de `Proyecto/`
- **Otros** (Go `go.mod`, Rust `Cargo.toml`, Java `pom.xml` / `build.gradle`)

---

## 📝 Paso 2: Actualización Inteligente de Archivos de Contexto

Obtén la fecha/hora UTC actual (formato ISO 8601, ej. `2026-10-24T23:30:00Z`). **Nunca uses placeholders como `[DATE]`.**

Actualiza únicamente los archivos que presenten cambios reales:

### 1. `tasks/context/tech-context.md` (Si cambiaron dependencias o versiones)
- Registra nuevas librerías instaladas en los repositorios de `Proyecto/`.
- Actualiza versiones de frameworks, SDKs y herramientas activas.

### 2. `tasks/context/project-structure.md` (Si se crearon o movieron carpetas/repos)
- Actualiza el mapa de carpetas con los repositorios actuales dentro de `Proyecto/`.
- Añade nuevos módulos o subdirectorios significativos creados durante las tareas.

### 3. `tasks/context/progress.md` (Siempre se actualiza)
- Registra los tickets y tareas recientemente completados en `tasks/task-*/`.
- Detalla el estado actual del proyecto y los siguientes pasos pendientes.

### 4. `tasks/context/learnings.md` (Si se descubrieron patrones o convenciones)
- Consolida lecciones técnicas aprendidas (ej. configuración de puertos, trucos de Docker, errores comunes de compilación resueltos).

### 5. `tasks/context/system-patterns.md` (Si cambió la arquitectura)
- Documenta nuevos patrones arquitectónicos incorporados (ej. nuevos interceptores, middleware, DTOs, CQRS).

### 6. `tasks/context/team-context.md` (Revisión de roles)
- Verifica que los roles de Tech Lead, QA y DevOps sigan claros y reflejados.

---

## 📊 Paso 3: Resumen de Actualización

Presenta al usuario un resumen conciso:

```
🔄 Actualización de Contexto de Faena Completada

📊 Estadísticas:
  - Repositorios en Proyecto/ analizados: [Lista de repositorios]
  - Archivos de contexto actualizados: [Conteo]
  - Archivos sin cambios (omitidos): [Conteo]

📝 Archivos Actualizados:
  ✅ tech-context.md - [Breve detalle de lo actualizado]
  ✅ progress.md - [Últimos tickets/tareas registrados]
  ...

⏰ Fecha de actualización: [Timestamp real]
```
