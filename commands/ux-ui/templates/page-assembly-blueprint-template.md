# [PageName] Page Assembly Blueprint

<!--
TEMPLATE INSTRUCTIONS:
- This document describes how components assemble within main-content
- Reference component blueprints — don't duplicate their details
- Focus on layout, composition, and page-level visual behavior
- Capture TRIGGER + VISUAL RESPONSE + MOTION for states and interactions
- Exclude technical implementation (state management, API calls, URL handling)
-->

**Page:** [PageName]
**Route:** [/path/to/page]
**Created:** [Date]
**Status:** Draft | Ready for Review | Approved

---

## What This Document Captures

This blueprint documents **what you see and when** — the complete visual experience of the page.

| ✅ In Scope | ❌ Out of Scope (defer to TRD) |
|-------------|-------------------------------|
| Trigger + Visual Response + Motion | Technical implementation |
| What loading state looks like | What API call triggers loading |
| How filter change animates | How filter state is stored |
| When scroll triggers animation | IntersectionObserver config |

---

## Purpose

[1-2 sentences describing the page's purpose and primary user goal]

---

## Visual Reference

- **Source:** [Figma link / Screenshot path / URL]
- **Breakpoints captured:** [List all breakpoints from PAGE-STRUCTURE.txt]

---

## Content Regions

<!-- Map the main-content area into logical regions -->

```
┌─────────────────────────────────────────────────────────────────┐
│  main-content                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  REGION: Page Header                                      │  │
│  │  [Title, subtitle, primary actions]                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────┐  ┌───────────────────────────────────────┐ │
│  │ REGION:         │  │ REGION: Primary Content               │ │
│  │ Filters         │  │ [Main content area]                   │ │
│  │                 │  │                                       │ │
│  │                 │  │                                       │ │
│  │                 │  │                                       │ │
│  └─────────────────┘  └───────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  REGION: Pagination                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Assembly

### Region: [Region Name]

| Component | Blueprint/Source | Notes |
|-----------|------------------|-------|
| [PageTitle] | Existing: `components/PageTitle.tsx` | Main page heading |
| [ActionButton] | shadcn/ui Button | "Add Product" action |

### Region: [Region Name]

| Component | Blueprint/Source | Notes |
|-----------|------------------|-------|
| [CatalogFilter] | `catalog-filter-blueprint.md` | New component |
| [FilterGroup] | Existing: `components/FilterGroup.tsx` | Used within CatalogFilter |

### Region: [Region Name]

| Component | Blueprint/Source | Notes |
|-----------|------------------|-------|
| [CatalogGrid] | `catalog-grid-blueprint.md` | New component |
| [ProductCard] | `product-card-blueprint.md` | Rendered per item |
| [EmptyState] | Existing: `components/EmptyState.tsx` | When filter returns 0 |

### Region: [Region Name]

| Component | Blueprint/Source | Notes |
|-----------|------------------|-------|
| [Pagination] | shadcn/ui | Standard pagination |

---

## Page Layout

### Layout Structure

```css
/* Conceptual layout — not literal CSS */
main-content {
  display: flex;
  flex-direction: column;
  gap: spacing-24;
}

.content-body {
  display: grid;
  grid-template-columns: 280px 1fr;  /* Filters | Grid */
  gap: spacing-24;
}
```

### Layout Tokens

| Property | Token | Value |
|----------|-------|-------|
| Region gap (vertical) | spacing-24 | 24px |
| Filter/Grid gap | spacing-24 | 24px |
| Filter column width | — | 280px (fixed) |
| Grid column | — | 1fr (flexible) |
| Max content width | size-container-max-width | 1280px |

---

## Alignment Rules

<!-- Document sibling elements that must share visual alignment -->
<!-- This prevents bugs where padding is added to one child but not another -->

| Elements | Alignment Rule | Implication |
|----------|---------------|-------------|
| [Element1] / [Element2] | Share same left edge | Padding on container only |
| [Element3] / [Element4] | Independent | Each controls own padding |

<!--
Example:
| CatalogToolbar / ProductGrid | Share same left edge | px-6 on container, not children |
| Breadcrumb / PageHeader | Independent | Each has own horizontal padding |
-->

---

## Inter-Component Spacing

<!--
CRITICAL: Document the gaps BETWEEN components — these fall outside individual component blueprints.
Someone must OWN each gap. Measure computed values to verify.
-->

| Between | → And | Spacing | Class | Owner Element | Computed | Status |
|---------|-------|---------|-------|---------------|----------|--------|
| PageHeader | → ContentBody | [value]px | `[class]` | [which element has the class] | [computed]px | ✅/⚠️ |
| Sidebar | → ProductGrid | [value]px | `[class]` | [which element] | [computed]px | ✅/⚠️ |
| [Region/Component] | → [Region/Component] | [value]px | `[class]` | [which element] | [computed]px | ✅/⚠️ |

<!--
Spacing can come from:
- margin-top on the lower element
- margin-bottom on the upper element
- gap on the parent flex/grid container
- padding on a wrapper

Document WHERE the spacing class lives so implementers know which element to modify.

Standard Tailwind spacing reference:
  mt-2/mb-2/gap-2 = 8px
  mt-4/mb-4/gap-4 = 16px
  mt-6/mb-6/gap-6 = 24px
  mt-8/mb-8/gap-8 = 32px

If computed ≠ expected: Mark as ⚠️ MISMATCH and investigate.
-->

---

## Responsive Behavior

<!-- Document layout at EVERY breakpoint from PAGE-STRUCTURE.txt -->

| Breakpoint | Layout Changes |
|------------|----------------|
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |
| [From PAGE-STRUCTURE.txt] | [Layout at this breakpoint] |

### Breakpoint Details

<!-- Create a section for EACH breakpoint from PAGE-STRUCTURE.txt -->

#### [Breakpoint Name] ([Width])
- [Region restructuring at this breakpoint]
- [Component visibility/layout changes]  
- [Grid column changes]
- [Navigation/filter behavior]

<!-- Repeat for all breakpoints from PAGE-STRUCTURE.txt -->

---

## Page States

<!-- Document what you SEE in each state, what TRIGGERS it, and HOW it transitions -->

| State    | Trigger         | Visual Response                   | Motion                      |
| -------- | --------------- | --------------------------------- | --------------------------- |
| Loading  | Page load       | Skeleton in grid, filters visible | Instant                     |
| Loaded   | Data received   | Grid populated with cards         | Cards fade in, 50ms stagger |
| Empty    | Zero results    | EmptyState centered in grid       | Fade in 200ms               |
| Error    | API failure     | Error banner above grid           | Slide down 300ms            |
| Filtered | Filters applied | Filter badges above grid          | Badge scale-in              |

### State Transitions

<!-- Document motion between states when observable -->

| From → To        | Motion                                |
| ---------------- | ------------------------------------- |
| Loading → Loaded | Skeleton fades out, cards stagger in  |
| Loaded → Empty   | Grid cross-fades to EmptyState        |
| Any → Error      | Banner slides down from top           |

---

## Page-Level Interactions

<!-- Document trigger → visual response → motion for interactions spanning components -->

| Trigger                  | Visual Response                | Motion                             |
| ------------------------ | ------------------------------ | ---------------------------------- |
| User selects filter      | Grid shows filtered items      | Cross-fade 300ms                   |
| User selects sort        | Grid reorders                  | Items shuffle 200ms                |
| User clicks page number  | New page of items              | Fade out → scroll top → fade in    |
| User clicks "Clear all"  | Filters reset, full grid shown | Badges scale-out, grid cross-fades |
| Scroll to product area   | Cards enter viewport           | Slide up with 50ms stagger         |

<!--
Focus on what you SEE, not technical details:

✅ Include: "Grid cross-fades to new items"
❌ Exclude: "URL updates with filter params"

✅ Include: "Scroll to top"
❌ Exclude: "window.scrollTo implementation"
-->

---

## Display Requirements Summary

<!-- High-level requirements for the page — component blueprints have details -->

| Requirement | Location |
|-------------|----------|
| Product count | Page header ("Showing X of Y products") |
| Active filter indicators | Above grid or in filter panel |
| Sort control | Above grid, right-aligned |
| Results per page | Pagination area |

---

## Component Blueprints Referenced

<!-- List of component blueprints created during decomposition that this page uses -->

| Component | Blueprint | Purpose |
|-----------|-----------|---------|
| CatalogFilter | `catalog-filter-blueprint.md` | Filter panel for product catalog |
| CatalogGrid | `catalog-grid-blueprint.md` | Grid layout for product cards |
| ProductCard | `product-card-blueprint.md` | Individual product display |

---

## Existing Components Referenced

<!-- Components that already exist and will be reused -->

| Component | Source | Notes |
|-----------|--------|-------|
| PageTitle | `components/PageTitle.tsx` | Standard page header |
| FilterGroup | `components/FilterGroup.tsx` | Collapsible filter sections |
| EmptyState | `components/EmptyState.tsx` | "No results" state |
| Button | shadcn/ui | Various actions |
| Pagination | shadcn/ui | Page navigation |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| [Date] | Filters in `main-content`, not shell sidebar | Page-specific filters shouldn't be in global shell |
| [Date] | Mobile filters as modal, not accordion | Better UX for complex filter sets on small screens |

---

## Related Documents

- **Shell reference:** `docs/ux-ui/PAGE-STRUCTURE.txt`
- **Design system:** `docs/ux-ui/DESIGN-SYSTEM.md`
- **Component blueprints:** See "Component Blueprints Referenced" section

