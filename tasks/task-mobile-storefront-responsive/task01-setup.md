---
phase: setup
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 01: Scaffolding & Setup de Estado Reactivo Móvil

**Phase:** Setup  
**Module:** `apps/angular/src/app/public/storefront/storefront-catalog.component.ts`  
**Dependencies:** None  
**Estimated Effort:** 0.5h  

---

## Overview

Esta tarea introduce las señales reactivas (`signal`), efectos y métodos base en `StorefrontCatalogComponent` para soportar las interacciones móviles:
- `isMobileDrawerOpen`: Controla la apertura del menú lateral deslizante móvil.
- `isSortSheetOpen`: Controla la apertura del bottom-sheet de ordenamiento en móvil.
- `isMobileSearchOpen`: Controla la barra de búsqueda rápida móvil.
- Integración con `bodyScrollLockEffect` para que al abrir el drawer o el selector de orden se bloquee el scroll del body.
- Manejo de tecla Escape (`@HostListener('document:keydown.escape')`) para cerrar los nuevos overlays en orden de prioridad.

---

## File Operations

**Files Modified:**
- `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.ts`

**Files Created:** None  
**Files Deleted:** None  

---

## Key Interfaces & Signatures to Add

```typescript
// Signals
readonly isMobileDrawerOpen = signal<boolean>(false);
readonly isSortSheetOpen = signal<boolean>(false);
readonly isMobileSearchOpen = signal<boolean>(false);

// Methods
toggleMobileDrawer(): void;
closeMobileDrawer(): void;
openSortSheet(): void;
closeSortSheet(): void;
selectSortAndClose(mode: StorefrontSortMode): void;
toggleMobileSearch(): void;
closeMobileSearch(): void;
```

---

## Verification Criteria

- El componente compila limpiamente sin errores de tipado TypeScript (`npx ng build --configuration development`).
- El efecto `bodyScrollLockEffect` evalúa:
  ```typescript
  this.isModalOpen() || this.isCartOpen() || this.isImageZoomOpen() || this.isMobileDrawerOpen() || this.isSortSheetOpen()
  ```
