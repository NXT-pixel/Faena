# Catalog Import Delete Timeout Fix & Selection Unblock - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/`  
**Total Tasks**: 3 (1 setup + 1 RED + 1 GREEN+VERIFY)  
**Estimated Effort**: 4 hours  

---

## Quick Start

### Prerequisites
1. Leer `trd-catalog-import-delete-fix.md` para contexto técnico y arquitectura de blobs.
2. Revisar `test-spec-catalog-import-delete-fix.md` para especificaciones Given-When-Then.
3. Confirmar que el repositorio objetivo está en `Proyecto/growthhacking.PrototypeZero/`.

### Execution Order
Las tareas deben completarse en estricto orden secuencial. La fase RED debe completarse y fallar por la razón esperada antes de implementar en GREEN.

**Disciplina TDD**:
- RED: Escribir pruebas unitarias que fallen.
- GREEN: Implementar el código hasta que todas las pruebas pasen + ejecutar quality gates.

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
|------|------|-------|------|------------|--------------|-------|
| 01 | Setup y Verificación de Línea Base | setup | XS | 0.5h | None | dotnet-architect |
| 02 | Pruebas RED: Eliminación Concurrente y Selección en Frontend | red | S | 1.5h | 01 | xunit-tester |
| 03 | Implementación GREEN: Optimización Backend y Desbloqueo Frontend | green+verify | M | 2h | 02 | aspnet-webapi-backend |

**Legend**:
- **Size**: XS / S / M / L
- **Phase**: Setup, RED, GREEN+VERIFY
- **Agent**: Rol sugerido en `/agents/coding/`

---

## Task Details

### Phase 1: Setup (Task 01)
- **Setup** (`task01-setup-baseline.md`): Verificar compilación y baseline de pruebas de `CoreService` y `apps/angular`.

### Phase 2: TDD (Tasks 02–03)
- **RED** (`task02-red-delete-optimization-and-selection.md`): Escribir pruebas que fallen para borrado masivo concurrente en `StoreCatalogBlobServiceTests.cs` y desbloqueo de selección en `catalog-import.component.spec.ts`.
- **GREEN+VERIFY** (`task03-green-delete-optimization-and-selection.md`): Implementar `DeleteBlobsParallelAsync` en `StoreCatalogBlobService.cs`, optimizar `DeleteActiveCatalogAsync` y `DeleteDraftsAsync`, remover `[disabled]` de checkboxes en HTML y agregar validación en botón de publicación en TS. Ejecutar quality gates.

---

## Quality Gates

### verify:quick
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
```

### verify:full
```bash
dotnet build services/core/PrototypeZero.CoreService && dotnet test services/core/PrototypeZero.CoreService.Tests
```

---

## Progress Tracking

- [x] Task 01: Setup y Verificación de Línea Base (setup)
- [x] Task 02: Pruebas RED: Eliminación Concurrente y Selección en Frontend (RED)
- [x] Task 03: Implementación GREEN: Optimización Backend y Desbloqueo Frontend (GREEN+VERIFY)

---

## References

- **Design**: `design-catalog-import-delete-fix.md`
- **TRD**: `trd-catalog-import-delete-fix.md`
- **Test Spec**: `test-spec-catalog-import-delete-fix.md`
- **QA Handoff**: Laura (TRD §7)
- **DevOps Handoff**: Sofía (TRD §7)
