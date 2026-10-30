# Task: Fix Detail Modal Theme Consistency

## Problem
The product detail modal in the storefront catalog is hardcoded to use dark colors (dark glassmorphism) even when the catalog is in light mode. It should respect the current `themeMode` of the storefront.

## Context
- Component: `StorefrontCatalogComponent`
- Template: `storefront-catalog.component.html`
- Styles: `storefront-catalog.component.scss`
- Theme mode is managed by `themeMode()` signal (values: 'light', 'dark').

## Proposed Changes

1.  **Update CSS Variables in `storefront-catalog.component.scss`**:
    - The current modal styles (`.detail-modal-card`, `.modal-media-pane`, etc.) use hardcoded colors like `#131f37`, `#1a2a47`, and `#ffffff`.
    - These should be replaced with theme-aware variables.
    - I'll use the existing `--sf-surface`, `--sf-text`, `--sf-heading`, etc., which are already updated based on `[data-storefront-theme]`.

2.  **Refactor Modal Styles**:
    - `.detail-modal-backdrop`: background should be slightly transparent based on theme.
    - `.detail-modal-card`:
        - `background`: `var(--sf-surface)`
        - `border`: `1px solid var(--sf-border)`
        - `color`: `var(--sf-text)`
    - `.modal-media-pane`:
        - `background`: `var(--sf-surface-elevated)` or similar.
    - `.modal-product-title`: `color: var(--sf-heading)`
    - `.modal-sku-line`: `color: var(--sf-text-muted)`
    - `.modal-price-amount`: `color: var(--sf-heading)`
    - `.modal-desc-box`:
        - `h4`: `color: var(--sf-heading)`
        - `p`: `color: var(--sf-text-muted)`

## Step-by-Step Plan
1. Analyze the current hardcoded colors in `storefront-catalog.component.scss` (lines 1099-1309).
2. Create a set of CSS variables for the modal elements that adapt to the `[data-storefront-theme]` attribute.
3. Apply these variables to the modal classes.
4. Verify the change.
