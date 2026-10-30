# Technical Requirements Document (TRD): Product Detail Modal Theme Consistency

## 1. Problem Statement
The product detail modal in the storefront catalog uses hardcoded dark theme colors even when the catalog is set to light mode. This creates a jarring visual inconsistency for users.

## 2. Scope
- Modify `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/storefront-catalog.component.scss`.
- No changes to the TypeScript logic or HTML structure are required, as the theme mode is already correctly managed via `[attr.data-storefront-theme]`.

## 3. Technical Solution
Replace hardcoded hex colors in the `.detail-modal-*` CSS classes with the existing theme-aware CSS variables defined in the `:host` block of the same file.

### Key Changes in `storefront-catalog.component.scss`:
- `.detail-modal-backdrop`: Change `background: rgba(6, 11, 24, 0.85)` to a more neutral transparent color or a variable if applicable.
- `.detail-modal-card`:
    - `background`: `var(--sf-surface)`
    - `border`: `1px solid var(--sf-border)`
    - `color`: `var(--sf-text)`
- `.modal-media-pane`:
    - `background`: `var(--sf-surface-elevated)`
- `.modal-product-title`: `color: var(--sf-heading)`
- `.modal-sku-line`: `color: var(--sf-text-muted)`
- `.modal-price-amount`: `color: var(--sf-heading)`
- `.modal-desc-box h4`: `color: var(--sf-heading)`
- `.modal-desc-box p`: `color: var(--sf-text-muted)`

## 4. Impact Analysis
- **Frontend**: Visual consistency improved.
- **Backend**: No impact.
- **Performance**: No impact.

## 5. Team Coordination & Handoffs
- **QA Handoff**: Verify modal colors in both Light and Dark modes.
- **DevOps Handoff**: None.
