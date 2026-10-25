# 📁 Directorio `Proyecto/`: Repositorios de la Empresa o Cliente

Este directorio es el **espacio de trabajo de código fuente** de Faena para esta empresa o proyecto en particular.

---

## 🎯 ¿Cómo funciona?

Cuando recibes trabajo o tickets de una empresa o cliente (ej. **Proyecto A**):

1. **Clonas los repositorios de la empresa aquí dentro**:
   ```bash
   cd Proyecto
   git clone git@github.com:empresa-a/backend-api.git
   git clone git@github.com:empresa-a/frontend-portal.git
   # ... cualquier otro repositorio relacionado con este trabajo
   ```

2. **Ajustas las reglas y estándares de la empresa**:
   - Agrega o edita reglas en `rules/project/` (ej. convenciones de nombrado, arquitectura de la empresa, guías de autenticación).
   - Agrega skills específicas en `skills/project/` (ej. SDKs internos de la empresa, librerías compartidas, APIs privadas).

3. **Ejecutas los tickets con Faena**:
   ```bash
   # Faena detectará automáticamente los repos en Proyecto/ y su stack tecnológico
   python faena_cli.py run tasks/tickets/ticket-empresa-01.md

   # O puedes apuntar a un repositorio específico dentro de Proyecto/:
   python faena_cli.py run tasks/tickets/ticket-empresa-01.md --target Proyecto/backend-api
   ```

---

## 🔒 Independencia de Git
- Los repositorios que clones aquí dentro **no contaminan el repositorio de Faena**.
- El archivo `.gitignore` raíz de Faena está configurado para ignorar el contenido de `Proyecto/*` (excepto este README), permitiendo que cada repositorio de la empresa mantenga sus propios remotos (`origin`), ramas (`feature/xxx`) y commits.
- En Faena solo guardas los tickets, el contexto arquitectónico, y las reglas/skills específicas que configures para esa empresa.
