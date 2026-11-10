# Task 02 (RED): Reproducir la desincronización de tema en el drawer

## Objetivo

Fijar el comportamiento esperado (el drawer debe seguir el tema) y demostrar que falla antes del
cambio.

## Given / When / Then

- **Given** el storefront con `themeMode() === 'light'`
- **When** se abre el carrito (`isCartOpen()` en true)
- **Then** el drawer y su backdrop deben usar la paleta clara.

## Resultado obtenido antes del fix (RED)

| Elemento | Esperado (claro) | Obtendido |
|----------|------------------|-----------|
| Fondo del drawer | blanco | `#131f37` |
| Título / textos | navy | `#ffffff` / `#94a3b8` |
| Backdrop | `rgba(237, 255, 236, 0.8)` | `rgba(6, 11, 24, 0.85)` |
| Botón de cierre | claro | `rgba(255,255,255,0.1)` sobre panel claro |
| Tarjetas de ítem | `#f4fff3` | `rgba(255,255,255,0.03)` |

La captura del ticket (`image.png`) muestra exactamente ese estado: catálogo en claro y drawer
oscuro.

## Cómo se evidenció sin suite de UI

El componente se renderiza con datos remotos, así que la comprobación se hizo en dos capas:

1. **CSS compilado**: compilar `storefront-catalog.component.scss` y verificar que no existía
   ninguna variable `--sf-cart-*` ni selector `[data-storefront-theme='light']` que afectara a
   `.cart-drawer`.
2. **DOM/binding**: revisar el template y confirmar que el backdrop del carrito no recibía
   `[attr.data-storefront-theme]`, a diferencia del modal de producto.

Estado: ✅ COMPLETADO (fallo reproducido y documentado)
