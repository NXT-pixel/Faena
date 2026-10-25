# [ComponentName] Blueprint

<!--
TEMPLATE INSTRUCTIONS:
- Replace [bracketed placeholders] with actual values
- Delete sections marked OPTIONAL if not applicable
- Decision Log only records USER choices from delta resolution prompts (not agent decisions)
- When filling this template, ASK THE USER if anything is unclear—do not assume or guess
-->

**Component:** [ComponentName]
**Page Context:** [Which page(s) this appears on]
**Created:** [Date]
**Status:** Draft | Ready for Review | Approved

---

## Purpose

[1-2 sentences describing what this component does and its role in the UI]

---

## Visual Reference

<!-- Page-level screenshots are shared across all component blueprints. Captured once per page, not per component. -->

- **Source:** [Reference design URL]
- **Screenshots:** `[page-name]-screenshots/` folder (page-level, shared with other components)

<!--
BREAKPOINTS: Read from docs/ux-ui/PAGE-STRUCTURE.txt — do NOT hardcode.
Add one row per breakpoint defined in PAGE-STRUCTURE.txt.
-->

| Breakpoint | File | This Component's Location |
| ---------- | ---- | ------------------------- |
| [From PAGE-STRUCTURE.txt] | `[width]-[name].png` | [e.g., "Full width, below hero"] |
| [From PAGE-STRUCTURE.txt] | `[width]-[name].png` | [e.g., "2-column grid"] |
| ... | ... | ... |

<!-- Exception: For overlay components (modals, dropdowns), add component-specific screenshots showing the overlay open. -->

---

## Composition

### Building Blocks Used

<!-- List existing components this is built from -->

| Component      | Source                        | Usage             |
| -------------- | ----------------------------- | ----------------- |
| [Button]       | shadcn/ui                     | Primary action    |
| [Badge]        | shadcn/ui                     | Status indicator  |
| [ProductImage] | `components/ProductImage.tsx` | Product thumbnail |

### New Elements

<!-- Elements that need to be created as part of this component -->

| Element        | Description                                           |
| -------------- | ----------------------------------------------------- |
| [PriceDisplay] | Shows current price + optional strikethrough original |

---

## Design Tokens (CSS Variables)

<!--
Extract CSS variables used by this component. This preserves theming capability that would be lost
if we only captured resolved values. Run the extraction script from Agent 4 documentation (Step 4a).
-->

| Variable                                       | Resolved Value | Usage in Component |
| ---------------------------------------------- | -------------- | ------------------ |
| `--card`                                       | #f9fafb        | Card background    |
| `--foreground`                                 | #101828        | Text color         |
| `--primary`                                    | #3770ea        | Button background  |
| `--border`                                     | #eaecf0        | Card border        |
| [Add all CSS variables used by this component] |                |                    |

---

## Token Mapping

### Colors

| Usage          | Token          | Value   | Notes         |
| -------------- | -------------- | ------- | ------------- |
| Background     | `--card`       | #f9fafb |               |
| Border         | `--border`     | #eaecf0 |               |
| Title text     | `--foreground` | #101828 |               |
| Price text     | `--foreground` | #101828 |               |
| Original price | `Gray 400`     | #98a2b3 | Strikethrough |
| Sale badge bg  | `Red 500`      | #de3730 |               |

### Typography

| Element        | Token | Tailwind                                     |
| -------------- | ----- | -------------------------------------------- |
| Title          | H4    | `text-xl font-semibold tracking-tight`       |
| Price          | Large | `text-lg font-semibold`                      |
| Original price | Muted | `text-sm text-muted-foreground line-through` |

### Spacing

| Property       | Token      | Value |
| -------------- | ---------- | ----- |
| Padding        | spacing-16 | 16px  |
| Gap (internal) | spacing-8  | 8px   |
| Border radius  | radius.md  | 8px   |

### Shadows

| State   | Token     | Value                      |
| ------- | --------- | -------------------------- |
| Default | shadow.sm | 0 1px 2px rgba(0,0,0,0.05) |
| Hover   | shadow.md | 0 4px 6px rgba(0,0,0,0.1)  |

---

## Computed Spacing Measurements

<!--
CRITICAL: Extract actual computed values using browser DevTools.
Verify Tailwind classes produce expected pixel values.
This catches implementation drift before it happens.

Run on each major element:
  const styles = getComputedStyle(element);
  console.log({
    paddingTop: styles.paddingTop,
    paddingBottom: styles.paddingBottom,
    marginTop: styles.marginTop,
    gap: styles.gap
  });
-->

| Element | Property | Tailwind Class | Expected (px) | Computed (px) | Status |
|---------|----------|----------------|---------------|---------------|--------|
| Container | padding-top | `py-[X]` | [expected] | [computed] | ✅/⚠️ |
| Container | padding-bottom | `py-[X]` | [expected] | [computed] | ✅/⚠️ |
| Container | padding-left | `px-[X]` | [expected] | [computed] | ✅/⚠️ |
| Container | padding-right | `px-[X]` | [expected] | [computed] | ✅/⚠️ |
| [Element] | margin-top | `mt-[X]` | [expected] | [computed] | ✅/⚠️ |
| [Element] | gap | `gap-[X]` | [expected] | [computed] | ✅/⚠️ |

<!--
Standard Tailwind spacing reference:
  p-1/m-1/gap-1 = 4px
  p-2/m-2/gap-2 = 8px
  p-3/m-3/gap-3 = 12px
  p-4/m-4/gap-4 = 16px
  p-6/m-6/gap-6 = 24px
  p-8/m-8/gap-8 = 32px

If computed ≠ expected: Mark as ⚠️ MISMATCH and investigate parent constraints or CSS specificity.
-->

---

## Spacing Decisions

<!-- Document rationale for compact or unusual spacing to prevent implementers from "fixing" intentional values -->

| Context | Value | Rationale |
|---------|-------|-----------|
| [e.g., Vertical padding] | `py-2` (8px) | [e.g., Compact header maximizes content area] |
| [e.g., Internal gaps] | `gap-2` (8px) | [e.g., Dense layout fits more items visible] |

---

## Layout

### Structure (Visual Reference)

<!-- ASCII diagram for human reviewers — shows spatial relationships -->

```
┌─────────────────────────────┐
│  [Image - 1:1 aspect]       │
├─────────────────────────────┤
│  [Badge] (optional, overlay)│
├─────────────────────────────┤
│  [Title]                    │
│  [Price] [OriginalPrice]    │
│  [AddToCartButton]          │
└─────────────────────────────┘
```

### Structure (Machine-Readable)

<!-- Hierarchical breakdown for AI agent to replicate layout -->

| Element         | Parent       | Position    | Sizing                  | Notes                                    |
| --------------- | ------------ | ----------- | ----------------------- | ---------------------------------------- |
| Container       | —            | —           | Full width of grid cell | Flex column, gap-2                       |
| Image           | Container    | First child | Aspect 1:1, full width  | Overflow hidden                          |
| Badge           | Image        | Overlay     | Auto                    | Position: top-2 right-2, only if present |
| ContentStack    | Container    | After Image | Full width              | Flex column, gap-2                       |
| Title           | ContentStack | First       | Full width              | Max 2 lines, ellipsis                    |
| PriceRow        | ContentStack | Second      | Full width              | Flex row, items-baseline, gap-2          |
| Price           | PriceRow     | First       | Auto                    | —                                        |
| OriginalPrice   | PriceRow     | Second      | Auto                    | Only if discounted                       |
| AddToCartButton | ContentStack | Last        | Full width              | —                                        |

### CSS/Tailwind Implementation Hints

```
Container: flex flex-col gap-2 p-4 rounded-md border bg-card
Image container: aspect-square relative overflow-hidden
Badge position: absolute top-2 right-2
Content stack: flex flex-col gap-2
Price row: flex items-baseline gap-2
```

---

## Responsive Behavior

<!-- Document how THIS component changes at EACH breakpoint from PAGE-STRUCTURE.txt. Do not describe parent/sibling behavior. -->

| Breakpoint            | This Component's Behavior    |
| --------------------- | ---------------------------- |
| [From PAGE-STRUCTURE] | [How this component changes] |
| [From PAGE-STRUCTURE] | [How this component changes] |
| [From PAGE-STRUCTURE] | [How this component changes] |

### Breakpoint-Specific Changes

<!-- Only if this component itself changes at breakpoints (not layout changes from parent grid) -->

| Breakpoint | Change                           |
| ---------- | -------------------------------- |
| [bp name]  | [e.g., Button becomes icon-only] |

### Scaling Behavior

<!--
Document how this component scales. Measured by resizing browser to each breakpoint in PAGE-STRUCTURE.txt.

Width Types:
- fixed:[value] — Component maintains exact pixel width (e.g., fixed:256px)
- fluid:fill — Component expands to fill available container space
- percentage:[value] — Component uses percentage width (e.g., percentage:50%)

Alignment:
- left | center | right | stretch
-->

| Element   | Width Type    | Alignment | Breakpoint Notes                       |
| --------- | ------------- | --------- | -------------------------------------- |
| Container | [fluid:fill]  | [stretch] | [e.g., "fills grid cell at all sizes"] |
| [Element] | [fixed:256px] | [left]    | [e.g., "hidden below md"]              |

---

## States

### Derived from Reference

<!-- States that were observable in the design source -->

| State                                     | Trigger         | Visual Changes               | Token Mapping                   |
| ----------------------------------------- | --------------- | ---------------------------- | ------------------------------- |
| Default                                   | Initial render  | Base styling                 | —                               |
| Hover                                     | Mouse over card | Elevated shadow, slight lift | `shadow.md`, `translateY(-4px)` |
| [Add states observed in reference design] |                 |                              |                                 |

### Could Not Determine

<!-- States that are relevant but not visible in the reference — need design/eng input -->

| State    | Why Relevant          | Needs Decision                  |
| -------- | --------------------- | ------------------------------- |
| Focus    | Keyboard navigation   | Ring style? Offset?             |
| Disabled | Out of stock scenario | Opacity level? Button behavior? |
| Loading  | Initial data fetch    | Skeleton? Spinner?              |
| Error    | Failed to load image  | Fallback image? Icon?           |

---

## Decision Log

<!-- Record USER choices from delta resolution prompts. If no deltas were resolved, leave this section empty or write "No deltas resolved." Do NOT log agent decisions. -->

| Date   | Decision                  | User Choice                                            |
| ------ | ------------------------- | ------------------------------------------------------ |
| [Date] | Strikethrough price color | User chose `Gray 400` over `Gray 500` (delta option 1) |
| [Date] | Hover lift effect         | User chose to add `-translate-y-1` to DESIGN-SYSTEM.md |

