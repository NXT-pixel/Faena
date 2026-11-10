# Task 03 (GREEN): Implementación theme-aware del carrito

## Cambios aplicados

### 1. `storefront-catalog.component.scss`

- Se agregaron **19 tokens `--sf-cart-*`** en `:host` (valores de modo claro) y sus 19
  equivalentes dentro de `:host[data-storefront-theme='dark']`, replicando exactamente los colores
  oscuros previos. Tabla completa en `trd-cart-drawer-theme-fix.md` §4.
- El bloque `.cart-drawer` (y sus hijos) pasó de 25 colores hardcodeados a tokens:
  fondo, borde y sombra del panel; divisor de header/footer; títulos y textos; botón de cierre;
  estado vacío; tarjetas de ítem; media/fallback; acciones destructivas.
- `.cart-close-btn` ahora define su propio `background`/`color`/hover con tokens, porque
  `.modal-dismiss-btn` (que comparte) sigue anclado a la paleta oscura del modal.

### 2. `storefront-catalog.component.html`

```diff
-    <div class="detail-modal-backdrop cart-backdrop" (click)="closeCart()">
+    <div class="detail-modal-backdrop cart-backdrop" [attr.data-storefront-theme]="themeMode()" (click)="closeCart()">
...
             <button
               class="modal-whatsapp-cta"
+              [attr.data-storefront-theme]="themeMode()"
               (click)="checkoutWhatsApp()"
```

El backdrop reutiliza la regla existente de `.detail-modal-backdrop[data-storefront-theme='light']`
(scrim claro + `blur(10px)`), de modo que el carrito y el modal se comportan igual.

### 3. TypeScript

Sin cambios. `themeMode()`, `toggleTheme()` y la persistencia por tenant ya existían.

## Verificación (GREEN)

| Check | Comando | Resultado |
|-------|---------|-----------|
| Compilación SCSS aislada | `sass --no-source-map src/.../storefront-catalog.component.scss` | OK (sin warnings) |
| Tokens en CSS | grep `--sf-cart-bg` | `#ffffff` en `:host` y `#131f37` en `:host[data-storefront-theme=dark]` |
| `.cart-drawer` consume tokens | grep `var(--sf-cart-bg)` | presente |
| Build Angular dev | `npm run build` | exit 0 · `Application bundle generation complete [8.2s]` |
| Bundle contiene bindings | grep `data-storefront-theme` en `storefront-catalog.component-L772KU2F.js` | 76 ocurrencias |
| Lint template | `npx eslint src/app/public/storefront/storefront-catalog.component.html` | 0 errores |

## Evidencia visual (Chrome headless, CSS compilado real)

| Archivo | Contenido |
|---------|-----------|
| `evidence/cart-drawer-filled-light-vs-dark.png` | Carrito con ítems: claro (izq.) vs oscuro (der.) |
| `evidence/cart-drawer-empty-light-vs-dark.png` | Carrito vacío: claro vs oscuro |

En modo claro el panel es blanco con tarjetas `#f4fff3`, textos navy y stepper de marca; el scrim
es claro. En oscuro se mantiene `#131f37` con los mismos contrastes que antes.

## Notas para QA

- El cambio no toca backend ni contratos; alcanza con rebuild del bundle.
- Probar con dos tenants distintos para confirmar que la preferencia `storefront-theme:<tenant>`
  no se mezcla entre tiendas.

Estado: ✅ COMPLETADO
