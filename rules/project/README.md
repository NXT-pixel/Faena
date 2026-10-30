# 📏 Reglas Específicas de la Empresa / Proyecto (`rules/project/`)

Las reglas colocadas en esta carpeta tienen **máxima prioridad** en Faena. 

Utiliza este espacio para documentar y hacer cumplir los estándares particulares de la empresa o cliente:

- **Convenciones de código**: Estilos de nombrado, linting estricto, formato de comentarios.
- **Arquitectura exigida**: Clean Architecture, Vertical Slice, CQRS, convenciones de DTOs / Entities.
- **Seguridad y secretos**: Reglas sobre autenticación, tokens JWT, headers de tenant, CORS.
- **Testing**: Cobertura mínima exigida por la empresa (ej. 80%), frameworks de test obligatorios (`jest`, `pytest`, `xunit`).

Los agentes de Faena **no cargan esta carpeta automáticamente**. Las reglas de aquí se aplican porque `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `OPENCODE.md` y `.cursorrules` ordenan leer `rules/project/` antes de analizar o modificar código en `Proyecto/`. Escribe las reglas en `.md` y el agente las lee con su herramienta de lectura de archivos.
