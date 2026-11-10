---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 02: Pruebas RED: Eliminación Concurrente y Selección en Frontend

**Phase:** RED  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`  

---

## Overview

Escribir las pruebas automatizadas que definen el comportamiento esperado según la especificación (`test-spec-catalog-import-delete-fix.md`). Estas pruebas DEBEN fallar inicialmente (fase RED) antes de realizar la implementación en Task 03.

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/CatalogImportDeleteOptimizationTests.cs`

**Files Modified**:
- `apps/angular/src/app/store/catalog-import/catalog-import.component.spec.ts`

**Files Deleted**:
- None

---

## Tasks

### 1. Escribir pruebas unitarias para `StoreCatalogBlobService`
**Actions**:
- En `CatalogImportDeleteOptimizationTests.cs`:
  - Test que verifique que un método concurrente `DeleteBlobsParallelAsync` invoque el borrado de una lista de blobs y descuente la cuota acumulada en una sola llamada a `quotaService.RemoveUsedAsync(totalBytes)` en lugar de N llamadas separadas.
  - Test que verifique que si la lista de blobs está vacía, no se ejecuten llamadas remotas de cuota ni borrado.

**Success Criteria**:
- Las pruebas fallan por compilación o aserción porque `DeleteBlobsParallelAsync` aún no existe en `StoreCatalogBlobService`.

### 2. Escribir pruebas para `CatalogImportAppService.DeleteActiveCatalogAsync`
**Actions**:
- Test que simule la presencia de 50 borradores con imágenes y verifique que `DeleteActiveCatalogAsync`:
  - Limpie los borradores en base de datos.
  - Invoque la eliminación concurrente de las imágenes asociadas.
  - Restablezca el estado del catálogo importado a `CatalogImportStatus.Idle`.

**Success Criteria**:
- La prueba falla o verifica que la rutina actual aún usa el bucle secuencial.

### 3. Escribir pruebas de frontend en `catalog-import.component.spec.ts`
**Actions**:
- Test que valide que una fila con `status = CatalogProductDraftStatus.Incomplete` no tenga la casilla de selección deshabilitada.
- Test que valide que `toggleSelectAll(true)` agregue a la selección todos los elementos incluyendo los de estado `Incomplete`.
- Test que confirme que el botón "Publicar seleccionados" permanezca inactivo (`disabled`) si se encuentra seleccionado un borrador incompleto.

**Success Criteria**:
- Las pruebas de Angular fallan al comprobar que actualmente el checkbox está deshabilitado para incompletos.

---

## Verification Results (RED Phase Confirmed)

### Backend (xUnit)
Command: `dotnet test Proyecto/growthhacking.PrototypeZero/services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImportDeleteOptimizationTests"`
Output:
- `DeleteBlobsParallelAsync_ShouldDeleteBlobsAndDeductQuotaOnce`: **FAILED** (`System.NotImplementedException`)
- `DeleteBlobsParallelAsync_EmptyCollection_ShouldReturnZeroWithoutCallingQuota`: **FAILED** (`System.NotImplementedException`)
- `CollectImportImageBlobNames_FiltersWhitespaceAndReturnsDistinct`: **PASSED**
- Status: **RED verified** (Failed: 2, Passed: 1)

### Frontend (Karma / Jasmine Headless)
Command: `npx ng test --watch=false --browsers=ChromeHeadless --include "src/app/store/catalog-import/**/*.spec.ts"`
Output:
- `canPublishSelected should be false when selection includes incomplete draft (RED expectation)`: **FAILED** (`Error: Expected undefined to be false`)
- `toggleSelectAll should select ALL items including incomplete drafts for deletion (RED expectation)`: **FAILED** (`Error: Expected false to be true`)
- `should create component`: **PASSED**
- Status: **RED verified** (TOTAL: 2 FAILED, 1 SUCCESS)
