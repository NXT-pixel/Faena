---
phase: green+verify
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 03: Implementación de UI Móvil y Estilos SCSS (GREEN + VERIFY)

**Phase:** GREEN + VERIFY (Implementación y Calidad)  
**Modules:**
- `apps/angular/src/app/public/storefront/storefront-catalog.component.html`
- `apps/angular/src/app/public/storefront/storefront-catalog.component.scss`  
**Dependencies:** Task 02  
**Estimated Effort:** 2.0h  

---

## Overview

Implementar la estructura HTML semántica y las reglas de diseño SCSS para que la vista móvil (`viewport <= 768px`) replique exactamente la referencia estilo Kyte (`maria-isabel-accesorios.catalog.kyte.site`), manteniendo intacta la vista de escritorio (`> 768px`).

---

## Componentes de la Solución

1. **Header Móvil (`.storefront-navbar`)**:
   - Botón hamburguesa `☰` (`.mobile-menu-btn`) visible solo en pantallas `<= 768px`.
   - Logo centrado o proporcionado para altura de navbar (~44px).
   - Botón de carrito con insignia en la derecha.
   - En móviles, los botones secundarios (idioma, tema) se trasladan al drawer lateral.

2. **Drawer Lateral Deslizable (`.mobile-drawer-backdrop`)**:
   - Animación `slide-in` desde la izquierda.
   - Contiene: Logo e información del negocio, dirección y datos de contacto, accesos directos a WhatsApp, Instagram, Facebook y X, selector de idioma y botón de tema oscuro/claro.

3. **Carrusel Horizontal de Categorías (`.mobile-category-bar`)**:
   - Botón de búsqueda rápida `🔍` a la izquierda.
   - Pestañas con scroll horizontal táctil: `TODO` y categorías en mayúsculas.
   - Indicador visual de categoría activa con subrayado (`border-bottom`).

4. **Barra de Acción Móvil (`.mobile-action-bar`)**:
   - Badge de categoría activa a la izquierda.
   - Botón `ORDENAR POR` con icono `≡` a la derecha.

5. **Modal / Bottom Sheet de Ordenamiento (`.sort-sheet-backdrop`)**:
   - Diálogo inferior elegante con las opciones de ordenamiento y selección activa.

6. **Tarjetas de Producto Horizontales en Móvil (`.store-card`)**:
   - En pantallas `<= 768px`: Disposición horizontal flex (`flex-direction: row`).
   - Izquierda: Contenedor de imagen cuadrada (`aspect-ratio: 1 / 1`, aprox. 110px a 130px de ancho) con esquinas redondeadas (`border-radius: 14px`).
   - Derecha: Bloque de información con título en negrita (`line-clamp: 2`), categoría/subtítulo atenuado en gris, y precio destacado en color de acento.

---

## Quality Gates & Verification

```bash
# 1. Pruebas Unitarias Automatizadas
cd Proyecto/growthhacking.PrototypeZero/apps/angular && npx ng test --watch=false --browsers=ChromeHeadless --include="**/storefront-catalog.component.spec.ts"

# 2. Compilación de Producción
cd Proyecto/growthhacking.PrototypeZero/apps/angular && yarn build
```

**Criterios de Aceptación:**
- Todas las pruebas unitarias pasan con éxito (0 fallos).
- `ng build` compila con código de salida `0`.
- El layout en pantallas móviles se adapta fluidamente sin scrolls horizontales en el contenedor principal.
