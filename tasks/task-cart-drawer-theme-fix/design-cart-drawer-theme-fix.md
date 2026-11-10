# Task: Cart drawer respeta el modo claro/oscuro del storefront

## 1. Problema reportado

Al abrir el panel lateral del carrito ("Tu pedido") en el catálogo público, el panel se ve
siempre con el tema oscuro (`#131f37`, textos blancos, scrim negro) aunque el storefront esté
en modo claro. El usuario detectó la inconsistencia a simple vista: todo el catálogo cambia de
tema, pero el drawer y su backdrop no.

Evidencia: captura `image.png` (1638x1033) donde la tienda está en modo claro y el drawer se
renderiza oscuro con el scrim oscuro encima del catálogo.

## 2. Causa raíz

El componente ya gestiona el tema con la señal `themeMode()` (`'light' | 'dark'`), expuesta como
atributo en el host (`host: { '[attr.data-storefront-theme]': 'themeMode()' }`). El modal de
detalle de producto (fix anterior, `task-modal-theme-fix`) recibe el atributo por elemento y sus
estilos lo tienen en cuenta.

La sección del carrito quedó fuera de ese patrón:

1. **SCSS**: `.cart-drawer` y sus hijos (`.cart-drawer-header`, `.cart-empty-state`,
   `.cart-item-row`, `.cart-item-media`, `.cart-drawer-footer`, etc.) usaban ~25 declaraciones de
   color hardcodeadas en modo oscuro (`#131f37`, `#1a2944`, `#ffffff`, `#94a3b8`, `#64748b`,
   `rgba(255, 255, 255, ...)`, `#f87171`, `#fca5a5`) sin ninguna variante para modo claro.
2. **HTML**: el backdrop del carrito (`div.detail-modal-backdrop.cart-backdrop`) no llevaba
   `[attr.data-storefront-theme]`, por lo que tampoco aplicaba la regla de scrim claro que sí usa
   el modal (`rgba(237, 255, 236, 0.8)`); el carrito se pintaba con el scrim oscuro
   `rgba(6, 11, 24, 0.85)`.
3. El botón de cierre (`.cart-close-btn`, que hereda `.modal-dismiss-btn`) tomaba los tokens
   `--sf-modal-dismiss-*` (pensados para fondo oscuro), ilegibles sobre un panel claro.

## 3. Alcance

- `apps/angular/src/app/public/storefront/storefront-catalog.component.scss`
- `apps/angular/src/app/public/storefront/storefront-catalog.component.html`

Sin cambios en TypeScript: `themeMode()` ya existe, ya se persiste por tenant en `localStorage`
y ya se expone en el host.

## 4. Solución propuesta

1. Definir un juego de tokens `--sf-cart-*` dentro de `:host` (valores de modo claro) y sus
   equivalentes en el bloque `:host[data-storefront-theme='dark']`, replicando exactamente los
   colores oscuros actuales (cero cambio visual en modo oscuro).
2. Refactorizar el bloque `.cart-drawer` para consumir esos tokens.
3. Propagar `[attr.data-storefront-theme]="themeMode()"` al backdrop del carrito y al CTA de
   WhatsApp del footer, igual que el modal, para que el scrim y los estados de hover respondan
   al tema.

## 5. Criterios de aceptación

- En modo claro el drawer es blanco, con texto navy y bordes suaves; el scrim es claro.
- En modo oscuro el drawer mantiene píxel a píxel los colores actuales.
- El toggle de tema re-colorea el drawer en caliente, sin cerrarlo ni recargar.
- El tema persiste por tenant (`storefront-theme:<tenant>`), como el resto del storefront.
