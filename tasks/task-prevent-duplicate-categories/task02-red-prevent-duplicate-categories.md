---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 02: Suite TDD Anti-Duplicados - Tests

**Phase:** RED (Write Tests)  
**Module:** `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryDuplicateTests.cs`  
**Dependencies:** Task 01  

---

## Overview

Escribir las pruebas automatizadas que definan el comportamiento de prevención de categorías duplicadas tanto en la gestión manual (`CatalogCategoryAppService`) como en la publicación de productos de catálogo con IA (`CatalogImportAppService`). Las pruebas deben fallar inicialmente (fase RED) al ejecutarse contra el código actual, evidenciando que actualmente se permiten categorías duplicadas como `"Anillos"` y `"  anÍllos  "`.

---

## Module Responsibility

**File**: `services/core/PrototypeZero.CoreService/Store/Categories/CatalogCategoryAppService.cs`  
**Purpose**: Administrar las operaciones CRUD de categorías de catálogo, impidiendo nombres duplicados equivalentes en el mismo tenant.

**File**: `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`  
**Purpose**: Resolver o crear categorías durante la publicación de borradores extraídos por IA, reutilizando la categoría existente si ya existe una con nombre equivalente.

---

## Test Specification

### Test Suite 1: `CatalogCategoryDuplicateTests`
**File**: `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryDuplicateTests.cs`

#### Test: CreateAsync_ThrowsUserFriendlyException_WhenEquivalentNameExistsInSameTenant
- **Given:** Un tenant con una categoría existente llamada `"Anillos"`.
- **When:** Se invoca `CreateAsync` con un DTO cuyo nombre es `"  anÍllos  "` en el mismo tenant.
- **Then:** El método lanza `UserFriendlyException`.
- **And:** El repositorio no recibe ninguna nueva inserción de categoría.

#### Test: CreateAsync_Succeeds_WhenSameNameExistsInDifferentTenant
- **Given:** El Tenant A posee la categoría `"Anillos"`.
- **When:** El Tenant B invoca `CreateAsync` con el nombre `"Anillos"`.
- **Then:** La categoría se persiste exitosamente en el Tenant B sin lanzar excepciones.

#### Test: CreateAsync_Succeeds_WhenNameIsDistinct
- **Given:** Un tenant con la categoría `"Anillos"`.
- **When:** Se invoca `CreateAsync` con `"Collares"`.
- **Then:** La categoría se guarda exitosamente.

#### Test: UpdateAsync_ThrowsUserFriendlyException_WhenRenamingToExistingCategoryInSameTenant
- **Given:** En el tenant existen dos categorías: `"Anillos"` (ID 1) y `"Pulseras"` (ID 2).
- **When:** Se invoca `UpdateAsync` sobre el ID 2 intentando renombrarla a `"ANILLOS"` o `"ánillos"`.
- **Then:** Se lanza `UserFriendlyException` bloqueando el cambio.

#### Test: UpdateAsync_Succeeds_WhenUpdatingSameCategoryWithoutChangingNameOrJustCasing
- **Given:** La categoría `"Anillos"` (ID 1) con `DisplayOrder = 1`.
- **When:** Se invoca `UpdateAsync(ID 1, { Name = "ANILLOS", DisplayOrder = 2 })`.
- **Then:** La actualización es exitosa y no se produce bloqueo contra sí misma.

---

### Test Suite 2: `CatalogImportDuplicateCategoryTests`
**File**: `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/CatalogImportDuplicateCategoryTests.cs`

#### Test: ResolveOrCreateCategoryAsync_ReusesExistingCategory_WhenAiDraftSuggestsEquivalentName
- **Given:** Una lista en memoria de categorías de la tienda que contiene `"Anillos"`.
- **When:** Un borrador de producto extraído por IA contiene `CategoryName = "  anÍllos  "`.
- **Then:** La resolución retorna la instancia de la categoría `"Anillos"` existente.
- **And:** No se inserta una nueva fila en el repositorio de categorías.

#### Test: ResolveOrCreateCategoryAsync_CreatesNewCategory_WhenNoEquivalentExists
- **Given:** Una lista en memoria sin categorías equivalentes a `"Relojes"`.
- **When:** Se procesa un borrador con `CategoryName = "Relojes"`.
- **Then:** Se crea y retorna una nueva categoría `"Relojes"`.

---

## Test Data & Fixtures

```csharp
var tenantA = Guid.NewGuid();
var tenantB = Guid.NewGuid();

var category1 = new CatalogCategory
{
    Id = Guid.NewGuid(),
    TenantId = tenantA,
    Name = "Anillos",
    DisplayOrder = 1,
    IsActive = true
};

var category2 = new CatalogCategory
{
    Id = Guid.NewGuid(),
    TenantId = tenantA,
    Name = "Pulseras",
    DisplayOrder = 2,
    IsActive = true
};
```

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryDuplicateTests.cs`
- `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/CatalogImportDuplicateCategoryTests.cs`

**Files Modified**:
- None

**Files Deleted**:
- None

---

## Success Criteria

- [ ] Las pruebas de duplicados manuales y de importación IA están escritas siguiendo formato Given-When-Then.
- [ ] Los archivos de test residen en las rutas especificadas.
- [ ] Las pruebas se ejecutan y **FALLAN (Fase RED)** debido a que el código actual aún no implementa la validación ni la normalización.
- [ ] No se implementa código productivo en esta tarea.

---

## Notes

**For Coding Agent**: Escribe las pruebas unitarias y de integración que definan el contrato estricto de no-duplicidad por tenant. No implementes el código de solución en esta fase.
