# [PageName] Execution Package

**Page:** [PageName]
**Created:** [Date]
**Prototype:** [URL]
**Status:** Ready for Execution

---

## How to Execute

This package is directly executable. No TRD required.

**Workflow:**
1. Invoke: "Execute next task from [page-name]-execution.md"
2. AI reads first unchecked `- [ ]` item
3. AI reads linked blueprint, implements component
4. User verifies against prototype
5. User confirms verification passed
6. AI marks checkbox `- [x]` in execution package
7. Repeat until all tasks complete

---

## Data Strategy

### For NEW Components (🔧 Mock)

Use mock data until wire-up phase:

```tsx
// Replace with real data hooks in wire-up phase
const mock[EntityName] = [
  {
    id: '1',
    // ... entity fields
  },
];
```

### For REFACTOR/ENHANCEMENT Components (✅ Wired)

**Preserve existing data layer.** Only update UI/styling.

```tsx
// ✅ KEEP existing data fetching — only update UI
const { data: products } = useProducts(); // Existing hook — DO NOT REPLACE
```

---

## Resolved Decisions (REFACTOR/ENHANCEMENT Only)

<!-- Include this section for any REFACTOR or ENHANCEMENT components -->
<!-- These decisions OVERRIDE raw blueprint comparisons -->

### [ComponentName] Decisions

| Feature | Decision | Execution Task |
|---------|----------|----------------|
| [Feature1] | ✅ KEEP | Update styling to match blueprint |
| [Feature2] | ❌ REMOVE | Remove from component |
| [Feature3] | ❌ SKIP | Do not implement |

<!-- Repeat for each REFACTOR/ENHANCEMENT component -->

---

## Verification

For each component:
1. Open prototype at [URL]
2. Open implementation in dev server
3. Compare side-by-side at each breakpoint:
   - [width1] - [breakpoint1]
   - [width2] - [breakpoint2]
   - [width3] - [breakpoint3]
4. **Spacing check:** Run `auditSpacing()` on both, compare computed values
5. Visually indistinguishable = verified ✓

---

## Execution Checklist

### Phase 1: Components

<!-- Repeat for each component in build order -->

- [ ] **[ComponentName]** ([NEW/ENHANCEMENT/REFACTOR], [🔧 Mock / ✅ Wired])
  - Blueprint: `[component-name]/[component-name]-blueprint.md`
  - Analysis: `[component-name]/[component-name]-implementation-analysis.md` (if exists)
  - Create/Update: `src/features/[feature]/components/[ComponentName].tsx`
  - Data: [🔧 Use mock data / ✅ Preserve existing hooks]
  - Key Changes: [FROM RESOLVED DECISIONS — list specific updates]
  - States: [default, hover, focus, disabled, loading — as applicable]
  - Verify: Compare to prototype at all breakpoints

### Phase 2: Page Assembly

- [ ] **[PageName] Page**
  - Blueprint: `[page-name]-assembly-blueprint.md`
  - Create: `src/pages/[PageName].tsx`
  - **Page wrapper classes:** Verify outer container matches blueprint EXACTLY
    - ⚠️ Check for conflicting classes like `container mx-auto` vs `flex-1`
  - Layout: Use exact classes from blueprint
  - Components: Import and place all Phase 1 components
  - Verify: Full page matches prototype at all breakpoints

### Phase 3: Final Verification

**⚠️ DO NOT SKIP — catches layout bugs that component checks miss.**

- [ ] **Side-by-Side Visual Comparison**
  - Open prototype and implementation at each breakpoint
  - Check page STRUCTURE (not just components):
    - [ ] Page wrapper/container width behavior
    - [ ] Content fills available space correctly
  - **Check wide breakpoints (≥1280px):**
    - [ ] Content expands to fill viewport (no narrow centered column)
  - **Check actual rendered appearance:**
    - [ ] Background colors match visually (not just class names)
    - [ ] No unintended nested color blocks
  - All states work (hover, focus, loading)
  - Ready for wire-up or PR

- [ ] **Spacing Audit** ⚠️ CRITICAL
  - Run on prototype, then on implementation, compare results:
    ```javascript
    // Extract spacing for key elements
    function auditSpacing(selector) {
      const el = document.querySelector(selector);
      if (!el) return { error: 'not found' };
      const s = getComputedStyle(el);
      return {
        selector,
        padding: { top: s.paddingTop, right: s.paddingRight, bottom: s.paddingBottom, left: s.paddingLeft },
        margin: { top: s.marginTop, right: s.marginRight, bottom: s.marginBottom, left: s.marginLeft },
        gap: s.gap
      };
    }
    // Run for each element from blueprints:
    // auditSpacing('[selector-from-blueprint]');
    ```
  - **Compare values:** Any mismatch > 4px = FAIL — fix before proceeding
  - **Common drift:** `py-4` (16px) instead of `py-2` (8px), `mt-8` (32px) instead of `mt-2` (8px)

---

## Component Summary

| Component | Type | Blueprint | Target File | Data Status |
|-----------|------|-----------|-------------|-------------|
| [ComponentName] | [NEW/ENHANCEMENT/REFACTOR] | `[link]` | `[path]` | [🔧 Mock / ✅ Wired / ⚠️ Partial] |

---

## Existing Components (Reuse)

These are already implemented — import, don't rebuild:

| Component | Source | Used In |
|-----------|--------|---------|
| Button | shadcn/ui | [ComponentName] |
| [etc] | [source] | [usage] |

---

## Design System Changes

<!-- If any tokens were added during blueprint generation -->

| Token Added | Value | Rationale |
|-------------|-------|-----------|
| [None / List any added] | | |

---

## Visual Reference

- **Prototype URL:** [Link]
- **Screenshots:** `[page-name]-screenshots/`
  - `[width1]-[breakpoint1].png`
  - `[width2]-[breakpoint2].png`
  - ...

---

## Completion

When all checkboxes marked:
- ✅ UI implementation complete
- ✅ Ready for wire-up phase (if needed) or PR review

