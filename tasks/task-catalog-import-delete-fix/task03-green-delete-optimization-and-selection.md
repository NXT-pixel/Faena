---
phase: green+verify
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 03: Implementación GREEN: Optimización Backend y Desbloqueo Frontend

**Phase:** GREEN + VERIFY  
**Dependencies:** Task 02  
**Location:** `Proyecto/growthhacking.PrototypeZero/`  

---

## Overview

Implementar la optimización del backend en `StoreCatalogBlobService` y `CatalogImportAppService` utilizando paralelización con `Parallel.ForEachAsync` y consolidación de cuota, y modificar la plantilla y el componente de Angular en `catalog-import.component` para desbloquear la selección de borradores incompletos y restringir la validación de publicación al botón correspondiente. Ejecutar todos los quality gates hasta que todas las pruebas pasen en verde.

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/StoreCatalogBlobService.cs`
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
- `apps/angular/src/app/store/catalog-import/catalog-import.component.html`
- `apps/angular/src/app/store/catalog-import/catalog-import.component.ts`

**Files Deleted**:
- None

---

## Tasks

### 1. Implementar eliminación concurrente en `StoreCatalogBlobService.cs`
**Actions**:
- Agregar `public virtual async Task DeleteBlobsParallelAsync(IReadOnlyCollection<string> blobNames, CancellationToken cancellationToken = default)`.
- Usar `Parallel.ForEachAsync` con `ParallelOptions { MaxDegreeOfParallelism = 12, CancellationToken = cancellationToken }`.
- Para cada blob, eliminar mediante `blobClient.DeleteIfExistsAsync()` acumulando el tamaño liberado en una variable con operaciones atómicas (`Interlocked.Add`).
- Al finalizar el paralelismo, si el tamaño total liberado es mayor a 0, invocar `await quotaService.RemoveUsedAsync(totalReleasedBytes)` exactamente una vez.

**Success Criteria**:
- Las pruebas unitarias de `StoreCatalogBlobService` pasan exitosamente.

### 2. Refactorizar `CatalogImportAppService.cs`
**Actions**:
- En `DeleteActiveCatalogAsync`:
  - Reemplazar el bucle síncrono `foreach (var blobName in imageBlobNames) { await TryDeleteImportImageAsync(blobName); }` por una llamada a `_blobService.DeleteBlobsParallelAsync(imageBlobNames)`.
- En `DeleteDraftsAsync`:
  - Optimizar la recolección de blobs de imágenes no referenciadas y eliminarlos en paralelo.

**Success Criteria**:
- Pruebas de integración de `CatalogImportAppService` pasan al 100%.

### 3. Ajustar plantilla Angular (`catalog-import.component.html`)
**Actions**:
- En el checkbox de fila:
  - Eliminar `[disabled]="!canPublish(row)"`.
- En el botón "Publicar seleccionados":
  - Ajustar `[disabled]="selectedDraftIds().size === 0 || isPublishing() || !canPublishSelection()"`.

**Success Criteria**:
- Los checkboxes de borradores incompletos se muestran habilitados en la UI.

### 4. Ajustar controlador Angular (`catalog-import.component.ts`)
**Actions**:
- Actualizar `toggleSelectAll(checked: boolean)` para alternar la selección de todos los ítems de `result().items` sin filtrar por status.
- Crear la señal computada `canPublishSelection = computed(() => ...)` que valide si todos los IDs seleccionados corresponden a borradores con estado distinto a `Incomplete`.
- Actualizar `allSelected = computed(() => ...)` para reflejar si todos los elementos de la tabla están seleccionados.

**Success Criteria**:
- La suite de pruebas de Angular pasa en verde.

### 5. Quality Gates de Verificación (VERIFY)
**Actions**:
- Ejecutar:
  ```bash
  dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
  dotnet build services/core/PrototypeZero.CoreService
  ```

**Success Criteria**:
- 0 errores de compilación y 100% de tests aprobados.

---

## Verification Results (GREEN & VERIFY Phase Complete)

### Backend (xUnit & Build)
- `dotnet build services/core/PrototypeZero.CoreService`: **0 Errors**, 401 Warnings.
- `dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"`: **109 Passed, 0 Failed, 0 Skipped**.
- `dotnet test services/core/PrototypeZero.CoreService.Tests`: **866 Passed, 0 Failed, 17 Skipped** (100% pass rate).

### Frontend (Karma & Angular Build)
- `npx ng test --watch=false --browsers=ChromeHeadless --include "src/app/store/catalog-import/**/*.spec.ts"`: **5 Passed, 0 Failed** (TOTAL: 5 SUCCESS).
- `npm run build`: **0 Errors** (Application bundle generation complete).

### Git Corporate Identity
- `git config --local user.name`: `Santiago`
- `git config --local user.email`: `Santiago.guerrero@pevaar.com` (Verificado con `team-context.md`).
