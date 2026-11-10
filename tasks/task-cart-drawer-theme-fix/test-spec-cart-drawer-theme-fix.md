# Test Spec: Cart drawer theme-aware

## Precondiciones

- Storefront público accesible en `/<tenant>/catalog`.
- Tema del storefront controlado por el botón sol/luna del navbar (`themeMode()`).
- Preferencia persistida en `localStorage['storefront-theme:<tenant>']`.

## Casos

### TC-01 — Carrito vacío en modo claro
**Given** el storefront en modo claro
**When** el usuario abre el carrito sin ítems
**Then**
- el panel tiene fondo blanco (`#ffffff`) y borde izquierdo `rgba(25, 67, 131, 0.14)`;
- el título "Tu pedido" y "Tu carrito está vacío" se ven en navy (`#16213f`);
- el texto de ayuda usa navy al 60 % y el icono de carrito navy al 45 %;
- el scrim del backdrop es claro (`rgba(237, 255, 236, 0.8)` con blur), no negro;
- el botón "Seguir viendo" conserva el degradado verde/azul de marca con texto blanco.

### TC-02 — Carrito con ítems en modo claro
**Given** el storefront en modo claro con al menos dos productos
**When** el usuario abre el carrito
**Then**
- cada tarjeta de ítem usa fondo `#f4fff3` y borde `rgba(25, 67, 131, 0.1)`;
- nombre y total por línea en navy; precio unitario navy al 60 %;
- el stepper muestra botones verdes de marca y valor navy;
- el icono de eliminar es `#dc2626` y pasa a `#b91c1c` en hover;
- el footer separa con `rgba(22, 33, 63, 0.1)`, "Total" navy al 72 % y el monto navy;
- "Seguir comprando" navy al 60 % (hover navy), "Vaciar carrito" `#dc2626`.

### TC-03 — Sin regresión en modo oscuro
**Given** el storefront en modo oscuro
**When** el usuario abre el carrito (vacío y con ítems)
**Then** el resultado es idéntico al comportamiento previo: fondo `#131f37`, textos `#ffffff`
/ `#94a3b8` / `#64748b`, borde `rgba(255, 255, 255, 0.12)`, rojo `#f87171` y scrim oscuro.

### TC-04 — Cambio de tema con el drawer abierto
**Given** el carrito abierto
**When** el usuario pulsa el toggle sol/luna (si es visible con el drawer abierto) o reabre el drawer tras cambiarlo
**Then** el drawer se re-colorea al tema activo sin cerrarse ni recargar la página.

### TC-05 — Botón de cierre
**Given** el drawer abierto en modo claro
**When** el usuario observa el botón de cierre
**Then** el círculo es `rgba(22, 33, 63, 0.06)` con icono `#4b5a78`; en hover sube a
`rgba(22, 33, 63, 0.12)` con icono navy. En oscuro mantiene `rgba(255, 255, 255, 0.1)` / `#94a3b8`.

### TC-06 — Persistencia del tema
**Given** el usuario elige modo oscuro
**When** recarga el storefront y abre el carrito
**Then** el drawer sigue en oscuro (misma preferencia `storefront-theme:<tenant>`).

## Verificación automática ejecutada

| Check | Comando | Resultado |
|-------|---------|-----------|
| SCSS compila de forma aislada | `sass src/app/public/storefront/storefront-catalog.component.scss` | OK |
| Tokens light y dark en el CSS compilado | grep `--sf-cart-bg` | 2 definiciones (`:host` y `:host[data-storefront-theme=dark]`) |
| Build Angular (templates + estilos) | `npm run build` | OK — `Application bundle generation complete` |
| Atributo propagado al bundle | grep `data-storefront-theme` en `storefront-catalog.component-*.js` | 76 ocurrencias |
| Lint del template | `npx eslint src/app/public/storefront/storefront-catalog.component.html` | 0 errores |

## Evidencia visual

Las capturas siguientes se generaron compilando el SCSS real del componente y renderizando
el markup del drawer con Chrome headless en ambos temas (ver `evidence/`):

- `evidence/cart-drawer-filled-light-vs-dark.png`
- `evidence/cart-drawer-empty-light-vs-dark.png`
