# Task 01: Review existing SCSS and identify all hardcoded modal colors

## Description
Identify all hardcoded colors (hex values like `#...`) in the `.detail-modal-*` and `.modal-*` classes within `storefront-catalog.component.scss`.

## Findings

### Colors identified in `.detail-modal-*` and `.modal-*` classes:

| Location | Selector | Hardcoded Color | Line |
|----------|----------|-----------------|------|
| Modal backdrop background | `.detail-modal-backdrop` | `rgba(6, 11, 24, 0.85)` | 1103 |
| Modal card background | `.detail-modal-card` | `#131f37` | 1114 |
| Modal dismiss button background | `.modal-dismiss-btn` | `rgba(255, 255, 255, 0.1)` | 1133 |
| Modal dismiss button hover | `.modal-dismiss-btn:hover` | `rgba(255, 255, 255, 0.2)` | 1144 |
| Modal dismiss text | `.modal-dismiss-btn` | `#94a3b8` | 1135 |
| Modal dismiss hover text | `.modal-dismiss-btn:hover` | `#ffffff` | 1145 |
| Modal media background | `.modal-media-pane` | `#1a2a47` | 1164 |
| Media fallback icon | `.modal-media-fallback` | `rgba(255, 255, 255, 0.15)` | 1179 |
| Category crumb text | `.modal-cat-crumb` | `var(--sf-brand-green)` (OK - variable) | 1192 |
| Product title | `.modal-product-title` | `#ffffff` | 1200 |
| SKU line text | `.modal-sku-line` | `#64748b` | 1204 |
| SKU strong text | `.modal-sku-line strong` | `#94a3b8` | 1209 |
| Price strip border top | `.modal-price-strip` | `rgba(255, 255, 255, 0.08)` | 1219 |
| Price strip border bottom | `.modal-price-strip` | `rgba(255, 255, 255, 0.08)` | 1220 |
| Price amount | `.modal-price-amount` | `#ffffff` | 1227 |
| Stock badge background | `.modal-stock-badge` | `rgba(50, 185, 95, 0.15)` | 1231 |
| Stock badge border | `.modal-stock-badge` | `rgba(50, 185, 95, 0.3)` | 1232 |
| Stock badge text | `.modal-stock-badge` | `#34d399` | 1233 |
| Description heading h4 | `.modal-desc-box h4` | `#cbd5e1` | 1250 |
| Description paragraph | `.modal-desc-box p` | `#94a3b8` | 1256 |
| Shipping note background | `.modal-shipping-note` | `rgba(255, 255, 255, 0.05)` | 1265 |
| Shipping note border | `.modal-shipping-note` | `rgba(255, 255, 255, 0.08)` | 1266 |
| Shipping note text | `.modal-shipping-note` | `#cbd5e1` | 1270 |
| Shipping note icon | `.modal-shipping-note i` | `#06b6d4` | 1274 |
| WhatsApp CTA background | `.modal-whatsapp-cta` | `var(--sf-brand-green)` (OK - variable) | 1289 |
| WhatsApp CTA text | `.modal-whatsapp-cta` | `#ffffff` | 1290 |
| WhatsApp CTA hover | `.modal-whatsapp-cta:hover` | `var(--sf-brand-blue)` (OK - variable) | 1305 |

## Summary Statistics
- **Total hardcoded colors found:** 24 instances
- **Variables already used:** 3 instances (`--sf-brand-green`, `--sf-brand-blue`)
- **Colors needing refactoring to CSS custom properties:** 21 instances

## Recommended Action Items
1. Create a new CSS custom property section for modal-specific colors in the root or component scope
2. Replace all hardcoded hex values with appropriate variables
3. Ensure dark mode compatibility by mapping to existing `--sf-bg` and `--sf-text` themes
4. Update hover states to use theme-aware colors instead of hardcoded whites

Status: ✅ **COMPLETED**
