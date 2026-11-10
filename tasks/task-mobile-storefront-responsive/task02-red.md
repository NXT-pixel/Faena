---
phase: red
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 02: Unit Tests Specification (RED Phase)

**Phase:** RED (Escribir Pruebas Unitarias)  
**Module:** `apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts`  
**Dependencies:** Task 01  
**Estimated Effort:** 1.0h  

---

## Overview

Escribir pruebas unitarias automatizadas en Jasmine/Karma dentro de `storefront-catalog.component.spec.ts` para validar todas las interacciones de los nuevos overlays y señales móviles antes de implementar la plantilla y estilos finales.

---

## Test Specification (Given-When-Then)

### Test Suite: `StorefrontCatalogComponent - Mobile Interactions`

1. **TC-MOB-001:** `isMobileDrawerOpen` debe iniciar en `false`.
2. **TC-MOB-002:** `toggleMobileDrawer()` debe cambiar el estado a `true`, y `closeMobileDrawer()` debe devolverlo a `false`.
3. **TC-MOB-003:** `isSortSheetOpen` debe iniciar en `false`.
4. **TC-MOB-004:** `openSortSheet()` debe abrir el selector (`true`) y `closeSortSheet()` debe cerrarlo (`false`).
5. **TC-MOB-005:** `selectSortAndClose(mode)` debe actualizar `sortMode` a la opción elegida y cerrar inmediatamente `isSortSheetOpen`.
6. **TC-MOB-006:** `onEscapeKey()` debe cerrar `isSortSheetOpen` prioritariamente si está abierto sin cerrar otros modales.
7. **TC-MOB-007:** `onEscapeKey()` debe cerrar `isMobileDrawerOpen` si el sort sheet está cerrado, antes de cerrar el modal de producto.
8. **TC-MOB-008:** `toggleMobileSearch()` debe alternar `isMobileSearchOpen`.

---

## File Operations

**Files Modified:**
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts`

**Files Created:** None  
**Files Deleted:** None  

---

## Execution Command

```bash
cd Proyecto/growthhacking.PrototypeZero/apps/angular && npx ng test --watch=false --browsers=ChromeHeadless --include="**/storefront-catalog.component.spec.ts"
```
*En la fase RED, los tests fallan si los métodos aún no están implementados o las aserciones no se cumplen.*
