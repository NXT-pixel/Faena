---
phase: green
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 03: Implementación y Estilos de Zoom en Catálogo (Fase GREEN + VERIFY)

**Phase:** GREEN (Implement Code + Verify Quality Gates)  
**Module:** `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/`  
**Dependencies:** Task 02 (Fase RED completada y tests fallando por la razón correcta)  

---

## Overview

Implementar la lógica reactiva en TypeScript (`StorefrontCatalogComponent`), la estructura semántica y accesible en HTML y los estilos visuales en SCSS con soporte completo para temas `light` y `dark`. Una vez implementado, ejecutar las pruebas unitarias y la verificación de compilación (Fase VERIFY).

---

## Module Responsibility

- **TypeScript (`storefront-catalog.component.ts`):**
  - Añadir la señal reactiva `readonly isImageZoomOpen = signal<boolean>(false)`.
  - Implementar `openImageZoom(): void` (validando que `selectedProduct()?.mainImageUrl` exista).
  - Implementar `closeImageZoom(): void`.
  - Añadir `@HostListener('document:keydown.escape') onEscapeKey(): void` con jerarquía de cierre.
  - Asegurar que `closeProductDetail()` cierre el zoom si estuviese activo.

- **HTML (`storefront-catalog.component.html`):**
  - Envolver la imagen del modal `.modal-media-pane` con trigger interactivo (`cursor: zoom-in`) y botón flotante de lupa `.zoom-trigger-btn` con ícono `fas fa-search-plus` y atributos `aria-label`.
  - Añadir bloque reactivo `@if (isImageZoomOpen() && selectedProduct(); as prod)` para el diálogo de Lightbox/Zoom con botón de cierre `(X)`, backdrop semitransparente e imagen ampliada.

- **SCSS (`storefront-catalog.component.scss`):**
  - Estilos para `.zoom-trigger-btn` (posición flotante, hover sutil, accesibilidad visual).
  - Estilos para `.image-zoom-backdrop` (blur glassmorphism, z-index superior `1050`, fade-in).
  - Estilos para `.image-zoom-dialog` e `.image-zoom-full` (aspect-ratio preservado, tamaño máximo contenido dentro de pantalla sin desbordamiento destructivo).
  - Soporte de tema claro (`light`) y oscuro (`dark`) mediante las variables existentes `--sf-modal-*` o `:host[data-storefront-theme]`.

---

## Test Reference

**Test File:** `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts` (creado en Task 02).  
Todas las pruebas de la suite deben pasar en verde tras la implementación.

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.ts`
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.html`
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.scss`

**Files Deleted**:
- None

---

## Test Issue Handling

Si durante la implementación encuentras incongruencias en los tests de Task 02, **pausa y reporta** antes de modificar los tests:
- Conflictos con los tipos DTO existentes (`PublicStorefrontProductDto`).
- Incompatibilidades de inyección de dependencias en el módulo de Angular.
- Casos donde los tests exijan estados no representables en el ciclo de vida del componente.

---

## Implementation Checklist

- [ ] Añadir señal `isImageZoomOpen` y métodos en `storefront-catalog.component.ts`
- [ ] Añadir listener de tecla `Escape` con jerarquía
- [ ] Agregar botón de lupa y lightbox en `storefront-catalog.component.html`
- [ ] Agregar estilos y soporte temático en `storefront-catalog.component.scss`
- [ ] Todas las pruebas de Task 02 pasan a estado GREEN

---

## VERIFY: Quality Gates

### 1. verify:quick (Compilación Angular & Types)
```bash
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular build
```
**Resultado esperado:** Compilación exitosa con 0 errores de TypeScript y 0 errores de templates Angular.

### 2. verify:tests (Ejecución de Pruebas Unitarias)
```bash
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular test --watch=false
```
**Resultado esperado:** Todas las pruebas de `storefront-catalog.component.spec.ts` pasan satisfactoriamente.

### 3. Verification Checklist
- [ ] `verify:quick` pasa sin errores
- [ ] `verify:tests` pasa en verde
- [ ] Compatibilidad verificada con temas `light` y `dark`
- [ ] Atributos de accesibilidad ARIA presentes
