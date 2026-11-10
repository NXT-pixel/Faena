# Requerimientos y Diseño: Zoom de Imagen en Detalle de Producto del Catálogo

**Fecha:** 2026-11-04  
**Ticket Origen:** Zoom en imagen de producto al abrirlo en el catálogo público (`Storefront`)  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero` (`apps/angular/`)  

---

## 1. Resumen Ejecutivo y Objetivos

Actualmente, cuando un cliente abre el modal de detalle de un producto en el storefront público de la tienda (`CapillArte` u otros tenants), la imagen del producto se visualiza con dimensiones acotadas (`max-height: 400px; object-fit: cover`) dentro del contenedor `.modal-media-pane`, sin posibilidad de examinar detalles finos (texturas, dijes, acabados, empaques o etiquetas).

Este requerimiento introduce una funcionalidad interactiva de **Zoom / Lightbox de Alta Definición** accesible directamente desde la imagen del modal de producto, permitiendo al usuario:
1. Identificar visualmente que la imagen es ampliable (mediante un botón / icono de lupa flotante y cursor interactivo).
2. Abrir una vista ampliada (lightbox/zoom viewer) a pantalla completa o modal de inspección detallada.
3. Desplazar/explorar la imagen ampliada o cerrar cómodamente el visor (tecla `Escape`, botón de cierre o clic fuera).

---

## 2. Personas y Actores

- **Usuario Final / Cliente del Catálogo**: Comprador que navega por la tienda web o móvil y desea ver en detalle los atributos del producto antes de agregarlo al carrito o pedirlo por WhatsApp.
- **Equipo Interno**:
  - **Tech Lead**: David / Santiago (revisión de contratos y arquitectura de UI en Angular 21).
  - **QA Asignado**: Laura (certificación de responsividad, interacciones táctiles y desktop, y compatibilidad con temas light/dark).
  - **DevOps**: Sofía (sin impacto en infraestructura ni variables de entorno).

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

### Escenario 1: Indicador de zoom disponible en el modal de detalle
- **Dado** que el usuario abre el modal de detalle de un producto que posee imagen (`mainImageUrl`),
- **Cuando** visualiza el contenedor de la imagen (`.modal-media-pane`),
- **Entonces** debe visualizar un botón o indicador accesible de zoom (ícono de lupa / expandir `fas fa-search-plus` o `fas fa-expand`), con etiqueta accesible (`aria-label`) y cursor interactivo (`cursor: zoom-in`).

### Escenario 2: Apertura del visor ampliado (Lightbox / Zoom View)
- **Dado** que el usuario está en el modal de detalle de producto,
- **Cuando** hace clic sobre la imagen o sobre el botón de zoom,
- **Entonces** se despliega una vista ampliada/lightbox de la imagen centrada en pantalla con fondo semitransparente, manteniendo la máxima nitidez y resolución original de la imagen.

### Escenario 3: Cierre de la vista de zoom
- **Dado** que el usuario tiene abierta la vista de zoom ampliada,
- **Cuando** presiona el botón de cerrar `(X)`, hace clic en el fondo oscuro, o presiona la tecla `Escape`,
- **Entonces** el visor de zoom se cierra suavemente y el usuario regresa al modal de detalle del producto sin perder su contexto (ni cantidad seleccionada ni scroll).

### Escenario 4: Comportamiento cuando el producto no tiene imagen
- **Dado** un producto que no cuenta con `mainImageUrl` (muestra fallback con ícono `fas fa-box-open`),
- **Cuando** se abre el modal de detalle,
- **Entonces** no debe mostrarse la opción de zoom ni activarse ningún comportamiento interactivo de ampliación sobre el fallback.

---

## 4. Alcance Técnico

### En Alcance (In Scope)
- **Frontend Angular 21** (`apps/angular`):
  - Modificación de [`storefront-catalog.component.html`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.html):
    - Añadir botón de activación de zoom y trigger de clic en la imagen dentro de `.modal-media-pane`.
    - Añadir capa/modal de Lightbox / Visor de Zoom con controles de cierre y soporte de accesibilidad.
  - Modificación de [`storefront-catalog.component.ts`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.ts):
    - Signal reactivo `isImageZoomOpen = signal<boolean>(false)`.
    - Métodos reactivos `openImageZoom()` y `closeImageZoom()`.
    - Listener de teclado para tecla `Escape` con jerarquía (cierra primero el zoom antes del modal principal).
  - Modificación de [`storefront-catalog.component.scss`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.scss):
    - Estilos para el botón de zoom sobre la imagen (`.zoom-trigger-btn`).
    - Estilos y animaciones de transición para el visor ampliado (`.image-zoom-overlay`, `.zoomed-image-container`).
    - Compatibilidad con temas `light` y `dark`.
  - Pruebas unitarias en [`storefront-catalog.component.spec.ts`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.spec.ts) validando la reactividad y los estados del zoom.

### Fuera de Alcance (Out of Scope)
- Modificaciones en servicios backend (`CoreService`, `FileManagementService`).
- Carga de imágenes suplementarias o galerías multiproducto (se mantiene enfocado en la imagen principal actual del producto).
- Redimensionamiento o compresión server-side.

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Validar apertura de zoom al hacer clic en la imagen y en el botón de lupa.
  - Probar cierre con clic fuera, botón `(X)` y tecla `Escape`.
  - Certificar responsividad en resoluciones móviles (375px, 414px) y desktop (>1200px).
  - Validar que en productos sin imagen el placeholder no active zoom.
  - Validar soporte tanto en modo claro (`light`) como modo oscuro (`dark`).
- **Handoff a DevOps (Sofía)**:
  - Sin dependencias de infraestructura, variables de entorno ni pipelines.

---

## 6. Próximo Paso

Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas Given-When-Then:

👉 **Arrastra al chat:**
`@commands/2-create-trd.md tasks/task-product-image-zoom/design-product-image-zoom.md`
