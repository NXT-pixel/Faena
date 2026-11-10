# TRD: Zoom de Imagen en Detalle de Producto del Catálogo (Storefront)

**Version:** 1.0  
**Created:** 2026-11-04  
**Location:** `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/`  
**Task Folder:** `tasks/task-product-image-zoom/`  

---

## 1. Overview

Este documento técnico especifica la solución de arquitectura e implementación para incorporar la funcionalidad de **Zoom / Lightbox de Imagen** en el modal de detalle de producto del catálogo público (`Storefront`). La solución permite a los usuarios examinar con nitidez y en gran formato las imágenes de los productos desde dispositivos móviles y de escritorio, enriqueciendo la experiencia de compra y conversión.

**In Scope:**
- Señal reactiva `isImageZoomOpen` en `StorefrontCatalogComponent` (Angular 21 Signals).
- Botón accesible de zoom (`.zoom-trigger-btn`) con ícono de lupa (`fas fa-search-plus`) y cursor `zoom-in` sobre la imagen del producto.
- Modal de Lightbox/Zoom (`.image-zoom-backdrop` y `.image-zoom-dialog`) con imagen en alta resolución y leyenda del producto.
- Cierre accesible mediante botón `(X)`, clic en el backdrop o tecla `Escape` (con jerarquía que no cierra el modal principal).
- Estilos y variables CSS con soporte para temas `light` y `dark`.
- Pruebas unitarias de comportamiento y regresión en Jasmine (`storefront-catalog.component.spec.ts`).

**Out of Scope:**
- Servicios de backend (`CoreService`, `FileManagementService`).
- Galería múltiple de imágenes (se enfoca en la imagen principal actual del producto).
- Bibliotecas externas pesadas de zoom (la solución se implementa nativamente con CSS y Angular Signals para optimizar performance y bundle size).

---

## 2. Architecture

### Component Diagram

```mermaid
graph TD
    classDef uiLayer fill:#4A90E2,stroke:#1C3F94,stroke-width:2px,color:#FFFFFF;
    classDef stateLayer fill:#50C878,stroke:#1E7E34,stroke-width:2px,color:#FFFFFF;
    classDef eventLayer fill:#E67E22,stroke:#A04000,stroke-width:2px,color:#FFFFFF;
    classDef styleLayer fill:#9B59B6,stroke:#5B2C6F,stroke-width:2px,color:#FFFFFF;

    subgraph "Storefront Catalog UI (Angular 21)"
        DOM["storefront-catalog.component.html"]:::uiLayer
        SCSS["storefront-catalog.component.scss"]:::styleLayer
        COMP["StorefrontCatalogComponent (TS)"]:::stateLayer
    end

    subgraph "Reactive State & Event Handling"
        SEL_PROD["selectedProduct() signal"]:::stateLayer
        ZOOM_SIG["isImageZoomOpen() signal"]:::stateLayer
        TRIG_ZOOM["openImageZoom() / closeImageZoom()"]:::eventLayer
        ESC_HOOK["@HostListener('document:keydown.escape')"]:::eventLayer
    end

    DOM -->|Click Image / Button| TRIG_ZOOM
    TRIG_ZOOM -->|Updates State| ZOOM_SIG
    ESC_HOOK -->|Escape Pressed| TRIG_ZOOM
    COMP -->|Exposes| ZOOM_SIG
    COMP -->|Exposes| SEL_PROD
    ZOOM_SIG -->|Renders Lightbox Modal| DOM
    SCSS -->|Theme Variables (Light / Dark)| DOM
```

### User Interaction Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Cliente / Usuario
    participant Modal as Modal Detalle Producto
    participant Comp as StorefrontCatalogComponent
    participant Zoom as Visor Lightbox Zoom

    User->>Modal: Clic en imagen o botón lupa (.zoom-trigger-btn)
    Modal->>Comp: openImageZoom()
    Comp->>Comp: isImageZoomOpen.set(true)
    Comp-->>Zoom: Renderiza overlay con imagen en alta resolución
    Note over User,Zoom: Usuario examina el producto en pantalla completa

    alt Cierre por botón (X) o clic en fondo
        User->>Zoom: Clic en botón cerrar o backdrop
        Zoom->>Comp: closeImageZoom()
    else Cierre por teclado Escape
        User->>Comp: Presiona Escape
        Comp->>Comp: Detecta isImageZoomOpen() == true -> closeImageZoom()
    end

    Comp->>Comp: isImageZoomOpen.set(false)
    Comp-->>Modal: Visor se cierra; usuario permanece en detalle de producto
```

---

## 3. Technology Stack

| Technology | Version | Justification |
| :--- | :--- | :--- |
| **Angular Core / Signals** | `~21.2.0` | Reactividad nativa con `signal()`, `computed()` y OnPush change detection |
| **FontAwesome Icons** | `v6 / ABP` | Iconografía estándar existente en la solución (`fa-search-plus`, `fa-times`, `fa-expand`) |
| **SCSS / CSS Variables** | CSS Moderno | Transiciones fluidas, backdrop-filter blur y compatibilidad nativa con temas `[data-storefront-theme]` |
| **Jasmine / Karma** | `jasmine-core: ~4.0.0` | Framework de pruebas unitarias configurado en `apps/angular` |

*Nota: No se incorporan dependencias npm adicionales.*

---

## 4. Module Responsibilities

### 1. `storefront-catalog.component.ts`
- **Ubicación:** `apps/angular/src/app/public/storefront/storefront-catalog.component.ts`
- **Responsabilidad:** Gestionar el estado reactivo del catálogo, apertura/cierre del visor de zoom y jerarquía de atajos de teclado.
- **Propiedades y Métodos Clave:**
  - `readonly isImageZoomOpen = signal<boolean>(false)`: Controla la visibilidad del lightbox de zoom.
  - `openImageZoom(): void`: Abre el visor si el producto seleccionado tiene `mainImageUrl`.
  - `closeImageZoom(): void`: Cierra el lightbox sin alterar el modal de producto.
  - `@HostListener('document:keydown.escape') onEscapeKey(): void`: Cierra el zoom prioritariamente si está abierto; si no, delega a `closeProductDetail()`.
  - Actualización en `closeProductDetail()`: Garantiza que `isImageZoomOpen.set(false)` se ejecute al cerrar el detalle.

### 2. `storefront-catalog.component.html`
- **Ubicación:** `apps/angular/src/app/public/storefront/storefront-catalog.component.html`
- **Responsabilidad:** Definir la estructura semántica y accesible del trigger de zoom y del overlay de visualización en gran escala.
- **Estructura Clave:**
  - Contenedor de imagen en modal con botón de zoom flotante accesible (`.zoom-trigger-btn`).
  - Bloque `@if (isImageZoomOpen() && selectedProduct(); as prod)` para el modal de lightbox con atributos ARIA (`role="dialog"`, `aria-modal="true"`).

### 3. `storefront-catalog.component.scss`
- **Ubicación:** `apps/angular/src/app/public/storefront/storefront-catalog.component.scss`
- **Responsabilidad:** Estilizar el botón de zoom, el overlay de pantalla completa y la imagen ampliada con soporte de temas claro/oscuro.
- **Variables y Clases:**
  - `.zoom-trigger-btn`: Posicionamiento flotante sobre la imagen con efecto hover sutil.
  - `.image-zoom-backdrop`: Fondo semitransparente con `backdrop-filter: blur(8px)`.
  - `.image-zoom-container`: Centrado flexible con contención de aspect-ratio y scroll/pan seguro.

---

## 5. Testing Strategy

**Distribución de Pruebas:**
- **80% Unit Tests (Jasmine):** Validación del ciclo de vida del signal, triggers de apertura/cierre, listener de Escape y exclusión de zoom para productos sin imagen.
- **20% Integration / Visual Verification:** Verificación de renderizado en DOM, accesibilidad ARIA y transición de temas.

**Mockable Boundaries:**
- Mocks mínimos para `ActivatedRoute`, `Router`, `PublicStorefrontService` y servicios de configuración ABP.

**Quality Gates:**
```bash
# Angular build check
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular build

# Angular tests execution
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular test --watch=false
```

---

## 6. Task Breakdown

| Task | Name | Phase | Files Created | Files Modified | Dependencies | Est. | Agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Scaffolding & Setup | setup | None | None | None | 0.5h | angular-developer |
| **02** | Unit Tests Specification (RED) | red | `storefront-catalog.component.spec.ts` | None | 01 | 1.5h | angular-developer |
| **03** | Zoom Implementation & Styles (GREEN) | green+verify | None | `storefront-catalog.component.ts`, `storefront-catalog.component.html`, `storefront-catalog.component.scss` | 02 | 2.0h | angular-developer |

### Task Details

#### Task 01: Scaffolding & Setup
- **Fase:** setup
- **Descripción:** Preparar el entorno de desarrollo y validar dependencias y estructura de archivos del módulo storefront.
- **Archivos:** Inspección de `apps/angular/src/app/public/storefront/`.

#### Task 02: Unit Tests Specification (RED Phase)
- **Fase:** red
- **Descripción:** Crear especificación de pruebas unitarias en `storefront-catalog.component.spec.ts` que valide:
  - Inicialización con `isImageZoomOpen` en `false`.
  - `openImageZoom()` conmuta a `true` únicamente si el producto tiene imagen.
  - `closeImageZoom()` restaura `isImageZoomOpen` a `false`.
  - Presionar Escape cierra el zoom primero sin cerrar el modal del producto.
- **Archivos Creados:** `apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts`

#### Task 03: Zoom Implementation & Styles (GREEN + VERIFY)
- **Fase:** green+verify
- **Descripción:** Implementar el estado reactivo en TypeScript, markup en HTML con directivas `@if`, estilos en SCSS y verificar con `yarn build`.
- **Archivos Modificados:**
  - `storefront-catalog.component.ts`
  - `storefront-catalog.component.html`
  - `storefront-catalog.component.scss`

---

## 7. Team Coordination & Handoffs

### QA Handoff (Laura)
- **Superficie de Prueba:** Catálogo público storefront (ej. `/store/products/catalog`).
- **Casos de Verificación Clave:**
  1. Abrir un producto con imagen -> Verificar presencia del botón de lupa y cursor `zoom-in`.
  2. Hacer clic en la imagen o botón -> Se despliega el visor a pantalla completa con imagen en alta nitidez.
  3. Cierre mediante botón `(X)`, clic en backdrop o tecla `Escape` -> Vuelve al modal de detalle sin cerrar el producto ni perder selecciones.
  4. Abrir un producto sin imagen (fallback caja) -> Confirmar que no hay opción de zoom disponible.
  5. Validar correcta visualización tanto en modo `light` como en modo `dark`.

### DevOps Handoff (Sofía)
- **Variables de Entorno:** Ninguna.
- **Infraestructura:** Ningún cambio en pipelines, contenedores ni Azure.

---

## 8. Reference Documents

- **Test Specification:** [`tasks/task-product-image-zoom/test-spec-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/test-spec-product-image-zoom.md)
- **Design Document:** [`tasks/task-product-image-zoom/design-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/design-product-image-zoom.md)
- **Target Repository:** `Proyecto/growthhacking.PrototypeZero/apps/angular/`
- **Team Context:** [`tasks/context/team-context.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/context/team-context.md)

---

## Summary

La solución implementa un zoom reactivo y accesible mediante Angular Signals dentro de `StorefrontCatalogComponent`, proporcionando una experiencia fluida e integrada sin librerías externas.

**Estimated Effort:** ~4 horas  
**Risk Level:** Low  
**Dependencies:** Ninguna externa  

---

👉 **Siguiente paso:** Arrastra al chat:
`@commands/3-create-tasks.md tasks/task-product-image-zoom/trd-product-image-zoom.md`
