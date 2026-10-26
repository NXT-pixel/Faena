---
description: Reglas y estándares obligatorios de desarrollo para esta empresa
globs: Proyecto/**/*
alwaysApply: true
---
# Estándares de Ingeniería de la Empresa

Estas reglas aplican a todos los repositorios dentro del directorio `Proyecto/`.

## 1. Convenciones de Arquitectura
- Separación clara entre capas de dominio, infraestructura y presentación.
- Todo endpoint de API debe validar parámetros de entrada usando schemas/DTOs.
- No colocar lógica de negocio directamente dentro de controladores o rutas HTTP.

## 2. Estándares de Pruebas (TDD)
- Todo nuevo feature o corrección de bug DEBE incluir pruebas unitarias o de integración.
- Los tests deben seguir la estructura Arrange-Act-Assert (o Given-When-Then).
- No hacer mock indiscriminado de tipos internos de dominio.

## 3. Manejo de Errores y Logging
- Utilizar códigos de error estructurados o excepciones específicas de dominio.
- Nunca silenciar excepciones con bloques `try/catch` vacíos.
- No imprimir credenciales ni datos sensibles en logs.

## 4. Identidad Git Corporativa (Pre-Commit Gate)
- **PROHIBIDO hacer commit o push con cuentas personales** (ej. `@gmail.com`, cuentas personales de GitHub).
- **Verificación Obligatoria de Identidad Git**:
  Antes de ejecutar `git commit` o `git push` en cualquier repositorio dentro de `Proyecto/<repo>`, el agente DEBE verificar la configuración local del repositorio:
  ```bash
  git -C Proyecto/<repo> config --local user.email
  git -C Proyecto/<repo> config --local user.name
  ```
  Si `user.email` o `user.name` locales no están configurados o no coinciden con la identidad corporativa definida en `tasks/context/team-context.md`:
  1. Configurar la identidad corporativa localmente en ese repositorio:
     ```bash
     git -C Proyecto/<repo> config --local user.name "<Nombre Corporativo>"
     git -C Proyecto/<repo> config --local user.email "<email@empresa.com>"
     ```
  2. NUNCA depender de la configuración global (`~/.gitconfig`), ya que suele contener la cuenta personal del desarrollador.
