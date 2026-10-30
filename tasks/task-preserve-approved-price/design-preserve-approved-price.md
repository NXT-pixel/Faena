# Requerimientos y Diseño: Preservar Precio Exacto Aprobado al Publicar Productos de Catálogo IA

**Fecha:** 2026-10-26  
**Ticket Origen:** `[Catalog] BUG Preserve approved exact price when publishing AI-extracted products`  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero/`  

---

## 1. Resumen Ejecutivo y Objetivos
Cuando un usuario importa un catálogo digital mediante extracción asistida por IA o revisa los borradores generados en el módulo de catálogo, el precio del producto (sea extraído o corregido manualmente por el administrador, ej. COP 60.000) debe persistirse, publicarse y mostrarse con total exactitud.

Actualmente, un producto revisado con precio de referencia COP 60.000 se persiste o visualiza tras la publicación como COP 59.999. El objetivo es eliminar cualquier transformación, truncamiento, artefacto de punto flotante o desajuste de unidad, garantizando que el valor confirmado por el usuario en el borrador se conserve íntegro en `Store.CatalogProducts`, en los registros persistidos y en la interfaz de usuario.

---

## 2. Personas y Actores
- **Usuario Final / Rol**: Administrador de Tienda / Operador de Catálogo (revisa borradores extraídos y publica productos).
- **Equipo Interno**:
  - **Tech Lead**: Santiago (Pevaar) / David
  - **QA Asignado**: Laura (QA Engineer)
  - **DevOps**: Sofía (Cloud/DevOps)

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

### Escenario 1: Publicación de un borrador con precio exacto aprobado
- **Dado** un borrador de producto extraído por IA con precio confirmado o corregido en COP 60.000 (o cualquier valor entero/decimal válido).
- **Cuando** el usuario ejecuta la acción de publicar el borrador (`PublishDraftsAsync`).
- **Entonces** el producto publicado en `Store.CatalogProducts` se persiste con `PriceAmount = 60000.00`.
- **Y** la visualización en la tabla de productos, detalle y APIs expone exactamente `60.000,00 COP` sin alteración de una unidad (sin mostrar 59.999,00).

### Escenario 2: Edición y guardado del borrador previo a la publicación
- **Dado** un borrador de producto en estado de revisión (`RequireReview` o `Ready`).
- **Cuando** el usuario edita el campo de precio a `60000` y guarda el borrador (`UpdateDraftAsync` / `MarkDraftReviewedAsync`).
- **Entonces** el valor `PriceAmount` del borrador se mantiene exactamente en `60000.00`.
- **Y** no se aplican heurísticas de redondeo o recuperación destructiva que modifiquen el precio aprobado manualmente.

### Escenario 3: Idempotencia en edición y guardado posterior del producto publicado
- **Dado** un producto ya publicado con precio COP 60.000.
- **Cuando** se edita o se vuelve a guardar cualquier propiedad del producto desde la grilla o modal.
- **Entonces** el precio se preserva en COP 60.000 sin sufrir decrementos ni alteraciones.

---

## 4. Alcance Técnico

### En Alcance (In Scope):
1. **Backend (`services/core/PrototypeZero.CoreService`)**:
   - `Store/CatalogImport/CatalogImportAppService.cs`: Flujo de `PublishDraftAsync`, `TryExpandVariants`, `UpdateDraftAsync`.
   - `Store/CatalogImport/CatalogPriceParser.cs` & `CatalogImportPriceOutlierDetector.cs`: Reglas de parseo numérico y recuperación para evitar conversiones flotantes erróneas o restas espurias.
   - `Store/ObjectMapping/CatalogProductDraftMapper.cs`: Mapeo DTO <-> Entidad para borradores y productos.
   - `Store/Products/CatalogProductAppService.cs`: Persistencia y actualización de `CatalogProduct.PriceAmount`.
   - Pruebas unitarias de regresión en `services/core/PrototypeZero.CoreService.Tests`.

2. **Frontend (`apps/angular`)**:
   - `apps/angular/src/app/store/catalog-import/create-update-catalog-draft/`: Validación y envío del formulario `priceAmount`.
   - `apps/angular/src/app/store/catalog-products/`: Formateo de moneda y edición en grilla/detalle.

### Fuera de Alcance (Out of Scope):
- Modificaciones en modelos de lenguaje o prompts de visión en `AiService` (la extracción ya provee candidatos; el bug reportado ataca la fase de revisión/publicación y persistencia).
- Cambios en el motor de pagos (Wompi) o pasarelas de cobro.

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Caso de prueba de certificación: Cargar catálogo con imagen de muestra ("Set $60.000").
  - En la pantalla de revisión de borradores, establecer o confirmar COP 60.000.
  - Publicar el borrador y certificar en la tabla de productos (`/store/products`), en el modal de detalle y en la base de datos SQL (`Store.CatalogProducts.PriceAmount`) que el valor sea exactamente `60000.00`.
  - Probar valores limítrofes (`10.000`, `50.000`, `99.999`, `100.000`).

- **Handoff a DevOps (Sofía)**:
  - No se requieren nuevas variables de entorno ni cambios de infraestructura. La corrección es a nivel de código de aplicación y tests en `PrototypeZero.CoreService` y `apps/angular`.

---

## 6. Próximo Paso
Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:
Arrastra al chat:
`@commands/2-create-trd.md tasks/design-preserve-approved-price.md`
