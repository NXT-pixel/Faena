# Preserve Approved Price - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/`  
**Total Tasks**: 3 (1 setup + 1 RED + 1 GREEN+VERIFY)  
**Estimated Effort**: 4 hours

---

## Quick Start

### Prerequisites
1. Read `trd-preserve-approved-price.md` for technical context
2. Review `test-spec-preserve-approved-price.md` for test requirements
3. Confirm repo at `Proyecto/growthhacking.PrototypeZero/`

### Execution Order
Tasks must be completed in sequence. RED phase must be completed before GREEN.

**TDD Discipline**:
- RED: Write tests that fail
- GREEN: Implement code to pass tests + run quality gates

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
|------|------|-------|------|------------|--------------|-------|
| 01 | Setup y Aislamiento de Casos de Prueba | setup | XS | 0.5h | None | dotnet-architect |
| 02 | Preservación de Precio y Sincronización de Variantes | red | S | 1.5h | 01 | xunit-tester |
| 03 | Preservación Exacta en Backend y Frontend | green+verify | M | 2h | 02 | aspnet-webapi-backend |

**Legend**:
- **Size**: S (Small), M (Medium), L (Large), XL (Extra Large)
- **Phase**: Setup, RED, GREEN (GREEN includes VERIFY)
- **Agent**: Recommended coding agent from `/agents/coding/`

---

## Task Details

### Phase 1: Setup (Task 01)

Verificar build/tests baseline de CoreService antes de agregar regresión.

#### Task 01: Setup
- **Setup** (`task01-setup-test-isolation.md`): Compilar suite y dejar entorno listo

### Phase 2: TDD Preserve Price (Tasks 02–03)

#### Tasks 02–03: Preserve Approved Price
- **RED** (`task02-red-preserve-approved-price.md`): Escribir `PreserveApprovedPriceTests.cs` (60000 vs 59999, sync variantes, publish exact)
- **GREEN** (`task03-green-preserve-approved-price.md`): Corregir AppService, VariantResolver y componente Angular + VERIFY

---

## Quality Gates

### verify:quick
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
```

### verify
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests
```

### verify:full
```bash
dotnet build services/core/PrototypeZero.CoreService && dotnet test services/core/PrototypeZero.CoreService.Tests
```

---

## Progress Tracking

- [x] Task 01: Setup y Aislamiento de Casos de Prueba (setup)
- [x] Task 02: Preservación de Precio y Sincronización de Variantes (RED)
- [x] Task 03: Preservación Exacta en Backend y Frontend (GREEN+VERIFY)

---

## References

- **TRD**: `trd-preserve-approved-price.md`
- **Test Spec**: `test-spec-preserve-approved-price.md`
- **Design**: `tasks/design-preserve-approved-price.md`
- **Coding Agents**: `/agents/coding/`
- **QA Handoff**: Laura (TRD §7)
- **DevOps Handoff**: Sofía (sin infra nueva)
