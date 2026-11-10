---
phase: red
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 02: Especificación y Escritura de Pruebas Unitarias (Fase RED)

**Phase:** RED (Write Tests)  
**Module:** `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts`  
**Dependencies:** Task 01  

---

## Overview

Escribir la suite completa de pruebas unitarias en Jasmine para validar el comportamiento del visor de zoom de producto en `StorefrontCatalogComponent`. Las pruebas deben definir el contrato reactivo antes de cualquier cambio en el código fuente y fallar inicialmente (fase RED).

---

## Module Responsibility

**File**: `apps/angular/src/app/public/storefront/storefront-catalog.component.ts`  
**Purpose**: Gestionar el estado reactivo del catálogo público, la activación/desactivación del visor de zoom y la jerarquía de atajos de teclado para la tecla `Escape`.

**Key Functions & Signals to Test**:
- `readonly isImageZoomOpen: Signal<boolean>`
- `openImageZoom(): void`
- `closeImageZoom(): void`
- `onEscapeKey(): void` / `@HostListener('document:keydown.escape')`

---

## Test Specification (Given-When-Then)

### Test Suite: `StorefrontCatalogComponent - Product Image Zoom`

#### Test 1: `should have image zoom closed initially`
- **Given:** Una instancia de `StorefrontCatalogComponent` recién inicializada.
- **When:** Se consulta el valor de `component.isImageZoomOpen()`.
- **Then:** Debe retornar `false`.

#### Test 2: `should open zoom when selected product has mainImageUrl`
- **Given:** Un producto seleccionado asignado a `component.selectedProduct` con una URL válida en `mainImageUrl`.
- **When:** Se ejecuta `component.openImageZoom()`.
- **Then:** `component.isImageZoomOpen()` debe ser `true`.

#### Test 3: `should not open zoom when selected product has no mainImageUrl`
- **Given:** Un producto asignado con `mainImageUrl` en `null` o vacío (`''`).
- **When:** Se ejecuta `component.openImageZoom()`.
- **Then:** `component.isImageZoomOpen()` debe permanecer en `false`.

#### Test 4: `should close zoom when closeImageZoom() is called`
- **Given:** `component.isImageZoomOpen()` en `true`.
- **When:** Se ejecuta `component.closeImageZoom()`.
- **Then:** `component.isImageZoomOpen()` debe ser `false`.
- **And:** El modal de detalle del producto debe permanecer abierto (`isModalOpen()` continúa `true`).

#### Test 5: `should close image zoom first on Escape key without closing product modal`
- **Given:** Tanto `isModalOpen()` como `isImageZoomOpen()` se encuentran en `true`.
- **When:** Se invoca el manejador de la tecla Escape (`component.onEscapeKey()`).
- **Then:** `component.isImageZoomOpen()` pasa a `false`.
- **And:** `component.isModalOpen()` sigue siendo `true`.

#### Test 6: `should close product modal on Escape key when image zoom is already closed`
- **Given:** `isImageZoomOpen()` es `false` e `isModalOpen()` es `true`.
- **When:** Se invoca el manejador de la tecla Escape (`component.onEscapeKey()`).
- **Then:** Se debe delegar el cierre al modal de producto (`closeProductDetail()` o `closeModal()`).

#### Test 7: `should ensure image zoom is closed when product detail modal is dismissed`
- **Given:** `isImageZoomOpen()` es `true`.
- **When:** Se invoca `component.closeProductDetail()`.
- **Then:** `component.isImageZoomOpen()` debe cerrarse (`false`).

---

## Test Data & Fixtures

```typescript
export const testProductWithImage = {
  id: 'prod-001',
  name: 'Collar de perlas con dijes',
  description: 'Collar artesanal.',
  priceAmount: 60000,
  priceCurrency: 'COP',
  categoryName: 'ACCESORIOS',
  categorySlug: 'accesorios',
  mainImageUrl: 'https://cdn.example.com/collar.jpg',
  requiresShipping: true,
  isAvailable: true,
};

export const testProductWithoutImage = {
  id: 'prod-002',
  name: 'Tarjeta Regalo Virtual',
  description: 'Bono digital.',
  priceAmount: 50000,
  priceCurrency: 'COP',
  categoryName: 'BONOS',
  categorySlug: 'bonos',
  mainImageUrl: null,
  requiresShipping: false,
  isAvailable: true,
};
```

---

## File Operations

**Files Created**:
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts`

**Files Modified**:
- None

**Files Deleted**:
- None

---

## Success Criteria

- [ ] Archivo `storefront-catalog.component.spec.ts` creado con todos los escenarios GWT.
- [ ] Mocks mínimos de providers para inicializar el componente de forma aislada.
- [ ] Las pruebas fallan por no existir aún los métodos/señal en `StorefrontCatalogComponent` (Fase RED validada).
- [ ] No se ha modificado la implementación en `storefront-catalog.component.ts`.
