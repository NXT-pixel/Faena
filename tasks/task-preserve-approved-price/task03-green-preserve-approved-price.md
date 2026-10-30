---
phase: green
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 03: Preservación Exacta en Backend y Frontend - Implementation

**Phase:** GREEN (Implement Code)  
**Module:** `CatalogImportAppService` / `CatalogDraftVariantResolver` / `create-update-catalog-draft.component.ts`  
**Dependencies:** Task 02 (RED phase must be complete)  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Implementar las correcciones en el backend (`CatalogImportAppService.cs`, `CatalogDraftVariantResolver.cs`) y frontend (`create-update-catalog-draft.component.ts`) para garantizar que el precio aprobado se sincronice con las variantes y se publique exactamente en `CatalogProducts`. Ejecutar quality gates hasta aprobación completa.

---

## Module Responsibility

**Files**:
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogDraftVariantResolver.cs`
- `apps/angular/src/app/store/catalog-import/create-update-catalog-draft/create-update-catalog-draft.component.ts`

**Purpose**: Preservar `PriceAmount` exacto (`decimal(18,2)` / number sin drift) desde revisión UI hasta publicación, evitando sobrescritura por variantes obsoletas (59.999).

**Key Functions**:
- `UpdateDraftAsync` / `PublishDraftAsync` / `TryExpandVariants` — backend
- `SyncVariantPrices` / parse-serialize variantes — resolver
- `onPriceAmountChange` / `buildUpdateDto` / `markReviewCompleted` — Angular

---

## Test Reference

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/PreserveApprovedPriceTests.cs` (from Task 02)

Read the tests from Task 02 to understand required behavior. All tests must pass after implementation.

---

## Architecture Patterns

Seguir patrones del TRD (`trd-preserve-approved-price.md` §2–§4):

- Usar `decimal` en C# para montos; nunca `double`/`float` en la ruta de precio
- Sincronizar variantes con el precio padre aprobado antes de persistir/publicar
- En `TryExpandVariants`, no permitir que variantes desactualizadas sobrescriban el precio confirmado
- En Angular, al cambiar el precio principal, propagar a variantes asociadas cuando aplique y construir DTO coherente

**Frontend agent de apoyo** (cambios UI): `/agents/coding/angular-developer.md`

---

## Coding Conventions

- Coincidir con estilo existente en CatalogImport / Store
- No agregar dependencias NuGet/npm nuevas
- No migraciones de esquema (columna ya es `decimal(18,2)`)
- No modificar modelo de visión multimodal de AiService

---

## Dependencies

**Uses**:
- Entidades `CatalogProductDraft`, `CatalogProduct`
- DTOs `UpdateCatalogProductDraftDto`, `ExtractedCatalogVariantDto`
- Mapper `CatalogProductDraftMapper` (si requiere ajuste mínimo para cumplir tests, reportar si está fuera de Files Modified del TRD)

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogDraftVariantResolver.cs`
- `apps/angular/src/app/store/catalog-import/create-update-catalog-draft/create-update-catalog-draft.component.ts`

**Files Deleted**:
- None

---

## Test Issue Handling

If you encounter issues with the tests from Task 02, **pause and report** rather than silently fixing tests. Report issues in these categories:

1. **Test Logic Inconsistencies** - Tests contradict each other or expect impossible states
2. **Schema/Type Mismatches** - Test expectations don't match actual schemas or type definitions
3. **Architectural Violations** - Tests expect patterns that violate documented architecture
4. **Missing Critical Coverage** - Critical paths or required validations are not tested
5. **Test Data/Mock Inconsistencies** - Mock data violates constraints or has invalid relationships
6. **Impossible Expectations** - Tests expect behavior that can't be guaranteed (timing, async, etc.)
7. **Validation Rule Conflicts** - Tests expect validation outcomes that contradict schemas
8. **Integration Point Mismatches** - Tests expect interfaces that don't match actual components
9. **Test Setup Problems** - Tests are brittle, share mutable state, or missing setup
10. **Ambiguous Requirements** - Tests have unclear behavior or multiple valid interpretations

**When reporting**: Describe the issue, affected tests, the conflict, and your proposed resolution. Ask permission before modifying tests.

**You may fix without asking**: Typos, imports, test helper usage, formatting.

---

## Implementation Checklist

- [x] Fix backend so approved price 60000 publishes exactly (never 59999 from stale variants)
- [x] Sync / resolve variant prices on parent price update
- [x] Align Angular draft modal so price changes stay coherent in payload
- [x] All Task 02 tests pass (GREEN phase validation)
- [x] No test modifications without user approval
- [x] Code follows patterns from TRD

---

## VERIFY: Quality Gates

Once implementation is complete and all tests pass, run quality gates from `Proyecto/growthhacking.PrototypeZero/`:

### verify:quick (< 5 seconds)

```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
```

**Expected**: No failures on CatalogImport / StoreCatalog filter

### verify (< 30 seconds)

```bash
dotnet test services/core/PrototypeZero.CoreService.Tests
```

**Expected**: All CoreService tests pass

### verify:full (< 2 minutes)

```bash
dotnet build services/core/PrototypeZero.CoreService && dotnet test services/core/PrototypeZero.CoreService.Tests
```

**Expected**: Build + tests green

### Coverage Requirements

- Flujos de precio y variantes: 100% (ruta crítica)
- Regresión COP 60.000 vs 59.999: 100%

### Verification Checklist

- [x] All PreserveApprovedPrice tests pass
- [x] `verify:quick` passes
- [x] `verify` passes
- [x] `verify:full` passes
- [x] Coverage on critical price path met
- [x] No new compiler errors in CoreService / Angular draft component

---

## Notes

**For Coding Agent**: Implement code to make all tests from Task 02 pass. Follow architecture patterns from TRD. Run quality gates to ensure implementation quality.

**If you find test issues**: Pause and report using the categories above. Do not modify tests without user approval.

**TRD Reference**: See `trd-preserve-approved-price.md`.

**QA Handoff (Laura)**: Tras VERIFY, preparar pasos de verificación UI (import-catalog, modal draft, grilla productos) con payload COP 60.000 vs variante 59.999.

**If quality gates fail**: Fix issues before marking task complete. Task is only done when all quality gates pass.
