# Requerimientos y Diseño: Prevenir Categorías Duplicadas en el Mismo Tenant

**Fecha:** 2026-10-27  
**Ticket Origen:** 79082 Bug [Catalog] Prevent duplicate categories within the same tenant  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero/`  

---

## 1. Resumen Ejecutivo y Objetivos

Actualmente, el sistema permite la creación de categorías con nombres comercialmente idénticos o equivalentes dentro de un mismo tenant (ej. `"Anillos"` y `"  anÍllos  "`), generando duplicidad en el catálogo, confusión para los clientes en el storefront y fragmentación de productos en el portal administrativo. Esta duplicidad ocurre tanto en la creación/edición manual de categorías en el módulo de catálogo como en la importación automática de catálogos mediante IA.

El objetivo de este requerimiento es implementar una validación robusta de nombres equivalentes (insensible a mayúsculas/minúsculas, espacios en blanco y diacríticos/acentos) que:
1. Impida la creación o actualización manual de categorías duplicadas dentro del mismo tenant mediante un error descriptivo para el usuario.
2. Reutilice inteligentemente las categorías existentes durante la importación y publicación de catálogos con IA cuando la categoría sugerida sea equivalente a una ya existente.
3. Respete estrictamente el aislamiento multitenant, permitiendo que diferentes tenants posean categorías con el mismo nombre sin interferencias.

---

## 2. Personas y Actores

- **Usuario Final / Rol**:
  - Administrador de Tienda / Operador de Catálogo: Gestiona categorías manualmente o aprueba borradores de catálogo extraídos con IA.
  - Cliente del Storefront: Visualiza categorías consolidadas y limpias sin duplicados.
- **Equipo Interno**:
  - **Tech Lead**: David / Santiago (Pevaar) — Validación de la estrategia de normalización y reglas de negocio ABP.
  - **QA Asignado**: Laura — Certificación de pruebas manuales, casos de acentos, espacios y pruebas de aislamiento multitenant.
  - **DevOps**: Sofía — Sin requerimientos de infraestructura nueva ni cambios de variables de entorno.

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

### Escenario 1: Intento de creación manual de categoría duplicada con variación de acentos y espacios
- **Dado** que existe una categoría con nombre `"Anillos"` en el tenant activo
- **Cuando** el administrador intenta crear una nueva categoría con el nombre `"  anÍllos  "` en el mismo tenant
- **Entonces** el sistema rechaza la operación con una excepción de negocio amigable (`UserFriendlyException`), indicando que ya existe una categoría con un nombre equivalente
- **Y** no se persiste ningún registro duplicado en la base de datos.

### Escenario 2: Actualización de categoría a un nombre existente en el mismo tenant
- **Dado** que existen las categorías `"Anillos"` y `"Pulseras"` en el mismo tenant
- **Cuando** el administrador edita la categoría `"Pulseras"` y cambia su nombre a `"anillos"` o `"Ánillos"`
- **Entonces** el sistema bloquea la actualización y notifica al usuario que el nombre entra en conflicto con otra categoría existente.

### Escenario 3: Actualización de una categoría preservando su propio nombre o ajustando formato
- **Dado** que existe la categoría `"Anillos"` con ID `X`
- **Cuando** el administrador edita dicha categoría cambiando atributos (ej. orden o estado) o ajustando su capitalización a `"ANILLOS"`
- **Entonces** el sistema permite el guardado exitoso sin disparar falso positivo de duplicidad contra sí misma.

### Escenario 4: Reutilización de categoría existente durante la importación de catálogo con IA
- **Dado** que en el tenant existe la categoría `"Anillos"`
- **Y** el operador publica un borrador de catálogo con IA donde un producto tiene asignada la categoría `"anÍllos"` o `" Anillos "`
- **Entonces** el servicio de importación (`CatalogImportAppService`) detecta la equivalencia semántica/fonética
- **Y** asigna el producto a la categoría existente `"Anillos"`, sin insertar una nueva categoría en la base de datos.

### Escenario 5: Independencia estricta entre diferentes tenants (Aislamiento Multi-Tenant)
- **Dado** que en el Tenant A existe la categoría `"Anillos"`
- **Cuando** un administrador del Tenant B crea una categoría `"Anillos"` o `"anÍllos"`
- **Entonces** el sistema permite la creación exitosa en el Tenant B, asegurando que las reglas de unicidad no colisionen entre inquilinos distintos.

---

## 4. Alcance Técnico

### En Alcance (In Scope)
1. **Normalizador Canónico de Nombres de Categoría**:
   - Reutilización o extensión de `StoreTextSearchNormalizer` para comparación uniforme:
     - Trim de espacios al inicio, al final y colapso de espacios múltiples internos.
     - Eliminación de acentos/diacríticos (`NormalizationForm.FormD` descartando `NonSpacingMark`).
     - Conversión a minúsculas (`ToLowerInvariant`).
2. **Validación en Backend (`PrototypeZero.CoreService`)**:
   - **`CatalogCategoryAppService`**: Sobrescribir `CreateAsync` y `UpdateAsync` para verificar duplicados equivalentes en el tenant actual antes de insertar o modificar en repositorio.
   - **`CatalogImportAppService`**: Ajustar `ResolveOrCreateCategoryAsync` para buscar categorías existentes utilizando comparación normalizada en lugar de igualdad ordinal estricta.
   - **Localización**: Agregar claves de localización amigables en los archivos JSON de localización de CoreService (ej. `CategoryAlreadyExists`).
3. **Pruebas Automatizadas TDD**:
   - Suite de pruebas unitarias e integración en `PrototypeZero.CoreService.Tests` cubriendo creación manual, edición, importación con IA y aislamiento multitenant.

### Fuera de Alcance (Out of Scope)
- Modificación del esquema de base de datos o migraciones de índices únicos complejos a nivel de motor SQL (la validación se resuelve a nivel de servicio de aplicación y lógica de dominio para soportar normalización de diacríticos independiente del collation de BD).
- Fusión retroactiva automática de categorías históricas duplicadas ya creadas previamente (este ticket se enfoca en prevención y reutilización a partir de ahora).

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Validar casos de prueba en `/store/catalog-categories`:
    - Creación con mayúsculas/minúsculas (`ANILLOS` vs `anillos`).
    - Creación con tildes y diacríticos (`Anillos` vs `anÍllos` vs `ànillos`).
    - Creación con espacios espurios (`"  Anillos  "`).
    - Edición de categoría existente hacia un nombre duplicado.
    - Edición de la misma categoría sin modificar el nombre (evitar falsos positivos).
    - Carga de catálogo con IA en `/store/products/import-catalog` verificando que no se creen categorías gemelas.
    - Validación multitenant (Tenant 1 y Tenant 2 deben poder usar el mismo nombre independientemente).
- **Handoff a DevOps (Sofía)**:
  - No requiere intervención de infraestructura ni configuración de variables de entorno.

---

## 6. Próximo Paso

Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:  
Arrastra al chat:
```bash
@commands/2-create-trd.md tasks/design-prevent-duplicate-categories.md
```
