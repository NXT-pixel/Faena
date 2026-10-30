# QA Handoff — Catalog layout, banner, theme switch

## What changed
Public catalog (`/store/products/catalog`): search in header, vertical categories on the left, hero banner under the header, light mode default + light/dark toggle. Tenant Branding (SaaS Tenants create/edit) can upload a catalog banner with the logos.

## Prerequisites
- CoreService `App:BrandingUrl` points at the public `tenant-branding/` container URL (trailing slash).
- SaasService Azure blob connection for `tenant-branding`.

## Steps for Laura
1. **Admin banners (light + dark)**
   - Host → SaaS → Tenants → edit tenant → Branding section → upload **Catalog banner (light)** and **Catalog banner (dark)** (~1200×320) → save.
   - Confirm blobs `{tenantId}-catalog-banner-light` and `{tenantId}-catalog-banner-dark` in the branding container.
2. **Storefront layout**
   - Open `/store/products/catalog?tenant=<name>` (anonymous / empty layout).
   - Search is in the top bar (between brand and cart/WhatsApp).
   - Categories are a vertical list on the left (horizontal scroll on narrow screens).
   - Banner sits under the header (placeholder strip if no banner for the active theme).
3. **Contact social handles**
   - Admin Branding → Contact: WhatsApp is a number with country code (e.g. `573218367410`); Facebook / Instagram / X accept **username only**.
   - Storefront shows WhatsApp via `wa.me/{digits}` and `@handle` links for Facebook / Instagram / X.
4. **Sort & display (sidebar)**
   - Under categories: **Ordenar por** — Categorías / Menor precio / Mayor precio / A-Z / Z-A (check on active).
   - Changing sort reloads products from the API with the matching `sorting` param.
   - **Modo de exhibición** — Instaview (4-col grid) vs Lista (horizontal rows: image left, details right).
   - Contact block (if configured) stays below these filters.
5. **Theme**
   - Default is light (brand bone/navy/greens).
   - Toggle sun/moon in the header → dark matches previous catalog look.
   - Reload: theme preference persists per tenant in `localStorage` (`storefront-theme:{tenant}`).
   - Logo and banner switch between `-*-light` / `-*-dark` with the theme when both exist.
6. **Regression**
   - Search debounce still filters products.
   - Category navigation still updates the URL and product grid.
   - Load-more keeps the current sort order.
   - Cart / WhatsApp checkout unchanged.
   - Product modal still works.

## Edge cases
- Missing banner blob → empty banner strip (no broken image).
- Missing logo for current theme → store icon fallback.
- Mobile → categories become a horizontal strip; sort/display options wrap as chips; search full-width under brand/actions.
