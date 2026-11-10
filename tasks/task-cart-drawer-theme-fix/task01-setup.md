# Task 01 (SETUP): Auditoría de colores del carrito

## Objetivo

Inventariar todos los colores fijos del drawer del carrito y confirmar por qué no responden al
tema.

## Hallazgos

### SCSS (`storefront-catalog.component.scss`, bloque `.cart-drawer`)

25 declaraciones de color hardcodeadas, todas pensadas para fondo oscuro:

| Selector | Declaración original |
|----------|----------------------|
| `.cart-drawer` | `background: #131f37` · `border-left: 1px solid rgba(255,255,255,.12)` · `box-shadow: -20px 0 50px rgba(0,0,0,.5)` |
| `.cart-drawer-header` | `border-bottom: 1px solid rgba(255,255,255,.08)` · `h2 color #ffffff` |
| `.cart-empty-state .empty-icon-wrap` | `background rgba(255,255,255,.05)` · `color #64748b` |
| `.cart-empty-state h3` / `p` | `#ffffff` / `#94a3b8` |
| `.cart-item-row` | `background rgba(255,255,255,.03)` · `border rgba(255,255,255,.07)` |
| `.cart-item-media` | `background #1a2944` · fallback `rgba(255,255,255,.2)` |
| `.cart-item-name` / `.cart-item-unit` | `#ffffff` / `#64748b` |
| `.cart-remove-btn` | `#f87171`, hover `#fca5a5` |
| `.cart-item-total` | `#ffffff` |
| `.cart-drawer-footer` | `border-top rgba(255,255,255,.08)` |
| `.cart-total-row` / `strong` | `#cbd5e1` / `#ffffff` |
| `.cart-link-btn` / hover / `.cart-clear-btn` | `#94a3b8` / `#ffffff` / `#f87171` / `#fca5a5` |

Además, `.cart-close-btn` heredaba `.modal-dismiss-btn`, que consume `--sf-modal-dismiss-*`
(valores oscuros fijos, sin variante clara para el carrito).

### HTML (`storefront-catalog.component.html`)

- `div.detail-modal-backdrop.cart-backdrop` no tenía `[attr.data-storefront-theme]`, así que
  heredaba el scrim oscuro del modal (`rgba(6, 11, 24, 0.85)`).
- El CTA de checkout del footer tampoco tenía el atributo (el del modal sí).

### Conclusión

El componente sí sabe el tema (`themeMode()`), pero el carrito nunca lo consumía: ni por tokens
ni por atributo. El fix debe cubrir ambos frentes.

## Artefactos

- Inventario base: `git show HEAD:apps/angular/src/app/public/storefront/storefront-catalog.component.scss`
- Captura del bug: `image.png` adjunta al ticket.

Estado: ✅ COMPLETADO
