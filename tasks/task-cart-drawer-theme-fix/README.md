# Cart drawer theme fix — índice

- [x] Task 01: Auditoría de colores hardcodeados del carrito y del backdrop.
- [x] Task 02: Reproducción del fallo (claro) y definición del comportamiento esperado.
- [x] Task 03: Tokens `--sf-cart-*` + binding `data-storefront-theme` en el drawer/backdrop.

## Documentos

| Documento | Propósito |
|-----------|-----------|
| [`design-cart-drawer-theme-fix.md`](design-cart-drawer-theme-fix.md) | Problema, causa raíz, alcance y criterios de aceptación |
| [`trd-cart-drawer-theme-fix.md`](trd-cart-drawer-theme-fix.md) | Solución técnica, tokens y handoffs QA/DevOps |
| [`test-spec-cart-drawer-theme-fix.md`](test-spec-cart-drawer-theme-fix.md) | Casos Given-When-Then y evidencia de verificación |
| [`task01-setup.md`](task01-setup.md) | Inventario de colores |
| [`task02-red.md`](task02-red.md) | Fallo reproducido |
| [`task03-green.md`](task03-green.md) | Implementación y verificación |

## Evidencia

- [Carrito con ítems: claro vs oscuro](evidence/cart-drawer-filled-light-vs-dark.png)
- [Carrito vacío: claro vs oscuro](evidence/cart-drawer-empty-light-vs-dark.png)

## Resumen del cambio

`apps/angular/src/app/public/storefront/storefront-catalog.component.{html,scss}`

- 19 tokens `--sf-cart-*` en `:host` y en `:host[data-storefront-theme='dark']`.
- `.cart-drawer` deja de usar colores fijos y consume los tokens.
- El backdrop del carrito y el CTA de checkout reciben `[attr.data-storefront-theme]="themeMode()"`.

Verificación: SCSS compila, `npm run build` exit 0, ESLint del template sin errores y preview
visual en ambos temas.

## Fuera de alcance

- Se detectó que el modal de detalle usa el patrón opuesto (atributo por elemento + overrides
  `light`), en lugar de tokens de tema. Funciona, pero unificarlo sería un refactor aparte.
