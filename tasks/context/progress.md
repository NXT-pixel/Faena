# Project Progress
**Created**: 2026-10-25T03:19:55.675128+00:00
**Last Updated**: 2026-10-27T17:51:00Z
**Branch**: bug/duplicated-categories

## Active Status
- AI Factory y Harness Faena operacionales al 100%.
- Repo activo en `Proyecto/`: `growthhacking.PrototypeZero` (.NET 10 + ABP Framework 10.5.0 + Angular 21).

## Resumen de Tickets y Estado Actual

### 1. Ticket `79082 Bug [Catalog] Prevent duplicate categories within the same tenant` (Completado)
- **Alcance**: Prevenir la creación de categorías con nombres equivalentes (variando en acentos, mayúsculas o espacios múltiples como `"Anillos"` y `"  anÍllos  "`) dentro del mismo tenant, y reutilizar automáticamente categorías existentes durante la importación con IA.
- **Implementación**:
  - `CatalogCategoryNormalizer.cs`: Normalización canónica Unicode FormD, descarte de diacríticos y colapso regex de espacios `\s+`.
  - `CatalogCategoryDuplicateValidator.cs`: Validación multi-tenant con exclusión de la propia entidad en actualizaciones.
  - `CatalogCategoryAppService.cs`: Intercepción en `CreateAsync` y `UpdateAsync` arrojando `UserFriendlyException(L["Category:AlreadyExists"])`.
  - `CatalogDraftCategoryResolver.cs` & `CatalogImportAppService.cs`: Reutilización de categorías existentes durante la publicación de borradores extraídos por IA.
  - Localización en `es.json` y `en.json` con soporte completo en español e inglés.
- **Verificación**:
  - 36 pruebas unitarias e integración TDD dedicadas pasando al 100% (24 de normalización + 12 de duplicados/importación).
  - 804 tests de `CoreService.Tests` ejecutados y pasando con 0 fallos.
  - Build de Angular 21 completado exitosamente en 11.06 segundos sin errores.

### 2. Ticket `[Catalog] BUG Preserve approved exact price when publishing AI-extracted products` (Completado)
- **Alcance**: Evitar que precios aprobados por el usuario (ej. COP 60.000) se alteren a COP 59.999 al publicar borradores debido a desajustes en variantes hijas extraídas por OCR/IA.
- **Implementación**:
  - `CatalogDraftVariantResolver.cs`: Incorporados métodos `SyncVariantPrices` y `ExpandVariants`.
  - `CatalogImportAppService.cs`: Sincronización obligatoria al actualizar, aprobar y publicar borradores.
  - `create-update-catalog-draft.component.ts` & `.html`: Sincronización reactiva del formulario en Angular con `(change)="onPriceAmountChange()"` y `syncVariantPrices()`.
  - `PreserveApprovedPriceTests.cs`: Suite TDD con 8 pruebas unitarias/integración xUnit passing 100%.
- **Verificación**:
  - 776 tests de `CoreService.Tests` pasados exitosamente.
  - Angular build completado sin advertencias críticas ni errores.
  - Handoff detallado para QA (Laura) preparado.

### 2. Infraestructura y Webhooks de WhatsApp (Completado)
- Corrección de visibilidad del túnel VS Code DevTunnel (`44368` en modo `Public`).
- Webhooks entrantes de 360Dialog operando exitosamente.
- Diagnóstico mediante inyección de logs en `D360Controller.cs`.

## Siguientes Pasos
- Empaquetar el commit de la solución en la rama `bug/preserve-price` con identidad corporativa (`Santiago.guerrero@pevaar.com`).
- Desplegar/entregar a Laura (QA) para la validación funcional en el entorno de pruebas.
- Continuar con el siguiente ticket de backlog según la priorización del Product Owner.
