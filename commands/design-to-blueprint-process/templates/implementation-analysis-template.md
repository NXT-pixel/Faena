# [ComponentName] Implementation Analysis

<!--
TEMPLATE INSTRUCTIONS:
- Replace [bracketed placeholders] with actual values
- Delete sections marked OPTIONAL if not applicable
- Implementation Type determines which TRD structure section to keep
- Decision Points require product owner resolution before TRD creation
- When filling this template, present options to the user—do not assume or guess

⛔ BLOCKING REQUIREMENT:
The "TRD Readiness Gate" section at the end of this document MUST have all items
checked before TRD creation can proceed. TRD creators are NOT authorized to make
assumptions for unresolved decisions—they must return to this document and get
explicit resolution first.
-->

**Source Blueprint:** [component-name]-blueprint.md
**Current Implementation:** [path/to/component.tsx] ([X] lines)
**Analyzed:** [Date]
**Status:** Draft | Pending Decisions | Ready for TRD

---

## Summary

| Metric              | Value                                    |
| ------------------- | ---------------------------------------- |
| Implementation Type | [NEW / ENHANCEMENT / REFACTOR / REWRITE] |
| Similarity Score    | [X]%                                     |
| Elements to Add     | [N]                                      |
| Elements to Remove  | [N]                                      |
| Elements to Change  | [N]                                      |
| Elements to Keep    | [N]                                      |
| Estimated Effort    | [X] hours                                |

---

## Implementation Type: [TYPE]

<!--
One of:
- NEW: No existing implementation found
- ENHANCEMENT: Existing component is close (≥85% similarity, ≤2 extra elements)
- REFACTOR: Significant restructuring needed (50-84% similarity)
- REWRITE: Major differences (<50% similarity, >5 extra elements)
-->

[Explanation of why this type was determined based on similarity score and element analysis]

---

## Blueprint Elements

<!-- Elements extracted from the blueprint (target state) -->

| Element            | Type    | Blueprint Specification        |
| ------------------ | ------- | ------------------------------ |
| [Product Title]    | Display | Clickable, navigates to detail |
| [Brand Name]       | Display | Gray text, smaller font        |
| [Stock Status]     | Display | Green "In Stock" indicator     |
| [Price]            | Display | Simple $X,XXX.XX format        |
| [Add to Cart]      | Action  | Primary CTA, full width        |
| [Configure Button] | Action  | Secondary, conditional         |

---

## Current Implementation Elements

<!-- OPTIONAL: Delete this section if Implementation Type is NEW -->
<!-- Elements found in the existing codebase implementation -->

| Element          | Current Behavior            | Line Reference |
| ---------------- | --------------------------- | -------------- |
| [Model Number]   | Large font-mono display     | :168-171       |
| [Spec/Desc]      | Title display               | :175-180       |
| [Brand + Vendor] | Two lines with icons        | :209-226       |
| [PricingStack]   | Complex multi-price display | :238-242       |
| [Certifications] | Badge row                   | :245-247       |
| [CAD/Revit]      | Icon display                | :254           |
| [Add to Project] | Primary button              | :260           |

---

## Similarity Analysis

<!-- OPTIONAL: Delete this section if Implementation Type is NEW -->

| Metric                                       | Value |
| -------------------------------------------- | ----- |
| Blueprint Elements                           | [N]   |
| Current Elements                             | [N]   |
| Matching Elements                            | [N]   |
| Missing Elements (in blueprint, not current) | [N]   |
| Extra Elements (in current, not blueprint)   | [N]   |
| Changed Elements (present but different)     | [N]   |

**Similarity Score:** [N]% ([Matching] / [Matching + Missing + Extra])

---

## Detailed Comparison

### Elements to REMOVE ❌

<!-- OPTIONAL: Delete if no elements to remove -->
<!-- Elements in current implementation that should not exist in target state -->

| Current Element    | Why Remove                 | Line Reference |
| ------------------ | -------------------------- | -------------- |
| [Model Number]     | Not in blueprint           | :168-171       |
| [Vendor Name]      | Blueprint shows brand only | :209-226       |
| [Certifications]   | Not in reference design    | :245-247       |
| [CAD/Revit Assets] | Not in blueprint           | :254           |

### Elements to CHANGE 🔄

<!-- OPTIONAL: Delete if no elements to change -->
<!-- Elements present in both but with different behavior/appearance -->

| Current Element         | Target State             | Notes                                     |
| ----------------------- | ------------------------ | ----------------------------------------- |
| "Add to Project" button | "Add to Cart" button     | Primary CTA label change                  |
| PricingStack            | Simple price display     | Replace complex component with simple     |
| Button layout           | Primary + dual secondary | Add to Cart + (Configure \| View Details) |

### Elements to ADD ➕

<!-- OPTIONAL: Delete if no elements to add -->
<!-- Elements in blueprint that don't exist in current implementation -->

| New Element         | Location                     | Priority |
| ------------------- | ---------------------------- | -------- |
| Stock Status Badge  | After category, before price | HIGH     |
| Simple price format | After stock badge            | HIGH     |

### Elements to KEEP ✅

<!-- OPTIONAL: Delete if Implementation Type is NEW -->
<!-- Elements that match between blueprint and current implementation -->

| Existing Element           | Notes             |
| -------------------------- | ----------------- |
| ProductImage with carousel | Matches blueprint |
| CompareCheckbox            | Matches blueprint |
| CategoryBadge              | Matches blueprint |
| Card hover states          | Matches blueprint |

---

## Recommended Task Structure

<!-- Keep only the section matching the Implementation Type -->

### For NEW Implementation

```
## Recommended: Single TRD

- Tasks 01-02: Create component scaffold and base structure
- Tasks 03-04: Implement display elements ([list key elements])
- Tasks 05-06: Implement interactive elements ([list actions])
- Tasks 07-08: Add states and accessibility
- Tasks 09-10: Tests and documentation

Estimated effort: [X] hours
```

### For ENHANCEMENT Implementation

```
## Recommended: Single TRD

- Tasks 01-02: Add [new element 1]
- Tasks 03-04: Add [new element 2]
- Tasks 05-06: Update [changed behavior]
- Tasks 07-08: Tests for new functionality

Estimated effort: [X] hours
```

### For REFACTOR Implementation

```
## Recommended: TWO TRDs

### TRD 1: Base Restructure (~[X] hours)

- Tasks 01-02: Remove [list elements to remove]
- Tasks 03-04: Create replacement sub-components
- Tasks 05-06: Restructure component layout
- Tasks 07-08: Update styling to match blueprint
- Tasks 09-10: Update existing tests

### TRD 2: Enhancements (~[Y] hours)

Depends on: TRD 1 completion

- Tasks 01-08: Enhancement features from blueprint

Total estimated effort: [X + Y] hours
```

### For REWRITE Implementation

```
## Decision Required

**Option A: Incremental Refactor**

- Keep existing component, apply changes gradually
- Higher risk of regressions, lower isolation
- Estimated: [X] hours

**Option B: Create V2 Component**

- Create [ComponentName]V2 as new component
- Migrate usage incrementally
- Archive original when refactor complete
- Estimated: [Y] hours (includes refactor effort)

Recommendation: [Option A/B based on risk analysis]
Rationale: [Why this option is preferred]
```

---

## Decision Points ❓

<!-- Decisions that require product owner input before TRD creation -->

### Features in Current Implementation NOT in Blueprint

<!-- Features that exist in current code but aren't in the blueprint target state -->

| Feature            | Question                          | Impact if Keep              |
| ------------------ | --------------------------------- | --------------------------- |
| [Model Number]     | Keep or remove from catalog card? | Update blueprint to include |
| [Vendor Name]      | Keep or remove?                   | Update blueprint to include |
| [Certifications]   | Move to detail page or keep?      | Affects card complexity     |
| [CAD/Revit Assets] | Move to detail page or keep?      | Affects card scope          |

### Conflicting Requirements

<!-- Cases where blueprint and current implementation conflict -->

| Issue         | Current              | Blueprint     | Resolution Needed          |
| ------------- | -------------------- | ------------- | -------------------------- |
| Primary CTA   | "Add to Project"     | "Add to Cart" | Which label is correct?    |
| Price Display | Complex PricingStack | Simple format | Is complex pricing needed? |

### Resolved Decisions

<!-- Document any questions that arose during analysis AND their resolutions -->
<!-- ⚠️ All questions MUST be resolved before proceeding — no open questions allowed -->

| Question | Resolution | Rationale |
|----------|------------|-----------|
| [Question that was identified] | [How it was resolved] | [Why this decision was made] |

---

## Alternative Approaches

<!-- OPTIONAL: Only include for REWRITE type or when tradeoffs exist -->

### Approach 1: [Name]

- **Description:** [What this approach involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Estimated Effort:** [X] hours

### Approach 2: [Name]

- **Description:** [What this approach involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Estimated Effort:** [X] hours

### Recommendation

[Which approach is recommended and why]

---

## TRD Readiness Gate

<!--
⛔ BLOCKING CHECKLIST — TRD creation CANNOT proceed until ALL items are checked.

TRD creators are NOT authorized to:
- Make assumptions for unresolved decisions
- Skip decision points marked as pending
- Proceed with "reasonable" defaults

If any item below is unchecked, STOP and resolve it first.
-->

### Decision Resolution Status

<!-- Copy each decision point from above and document its resolution -->

| Decision Point | Status                   | Resolution         | Resolved By | Date   |
| -------------- | ------------------------ | ------------------ | ----------- | ------ |
| [Decision 1]   | ✅ Resolved / ⏳ Pending | [What was decided] | [Name]      | [Date] |
| [Decision 2]   | ✅ Resolved / ⏳ Pending | [What was decided] | [Name]      | [Date] |

### Gate Checklist

<!-- ALL items must be checked before TRD creation -->

- [ ] **All decision points resolved** — No ⏳ Pending items in table above
- [ ] **Blueprint updated** — If any decisions changed the target state, blueprint reflects those changes
- [ ] **Implementation type confirmed** — Product owner agrees with NEW/ENHANCEMENT/REFACTOR/REWRITE classification
- [ ] **Effort estimate reviewed** — Stakeholder acknowledges estimated hours
- [ ] **TRD structure approved** — Agreement on single TRD vs multiple TRDs approach

### Gate Status

**Current Status:** ⛔ BLOCKED — Decisions pending / ✅ CLEARED — Ready for TRD

**Cleared By:** [Name]
**Cleared Date:** [Date]

<!--
If status is BLOCKED, TRD creation must not proceed.
Return to Decision Points section and resolve all pending items.
-->

---

## Next Steps

<!-- These steps can only proceed after TRD Readiness Gate is CLEARED -->

1. [ ] Verify TRD Readiness Gate status is ✅ CLEARED
2. [ ] Create TRD(s) based on recommended structure
3. [ ] Reference this implementation analysis in TRD header
4. [ ] Generate implementation tasks

---

## Related Documents

- **Blueprint:** [`[component-name]-blueprint.md`](./[component-name]-blueprint.md)
- **Current Implementation:** `[path/to/component.tsx]`
- **Decomposition:** [`[page-name]-decomposition.md`](./[page-name]-decomposition.md)
