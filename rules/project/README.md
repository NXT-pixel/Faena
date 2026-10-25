# 📏 Reglas Específicas de la Empresa / Proyecto (`rules/project/`)

Las reglas colocadas en esta carpeta tienen **máxima prioridad** en Faena. 

Utiliza este espacio para documentar y hacer cumplir los estándares particulares de la empresa o cliente:

- **Convenciones de código**: Estilos de nombrado, linting estricto, formato de comentarios.
- **Arquitectura exigida**: Clean Architecture, Vertical Slice, CQRS, convenciones de DTOs / Entities.
- **Seguridad y secretos**: Reglas sobre autenticación, tokens JWT, headers de tenant, CORS.
- **Testing**: Cobertura mínima exigida por la empresa (ej. 80%), frameworks de test obligatorios (`jest`, `pytest`, `xunit`).

Cualquier archivo `.mdc` o `.md` creado aquí será cargado automáticamente por los agentes de Faena al analizar y ejecutar tareas en los repositorios de `Proyecto/`.
