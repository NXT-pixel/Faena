---
phase: green
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 03: Implementación Anti-Duplicados y Normalizador

**Phase:** GREEN (Implement Code + VERIFY)  
**Module:** `services/core/PrototypeZero.CoreService.Contracts/Store/Categories/CatalogCategoryNormalizer.cs`  
**Dependencies:** Task 02 (RED phase must be complete and failing)  

---

## Overview

Implementar la solución integral para evitar categorías duplicadas en el mismo tenant. Esto comprende la creación de `CatalogCategoryNormalizer` para normalizar cadenas fonético-ortográficas, la sobreescritura de `CreateAsync` y `UpdateAsync` en `CatalogCategoryAppService` con validación defensiva en el tenant activo, la adaptación de `ResolveOrCreateCategoryAsync` en `CatalogImportAppService` para reutilizar categorías existentes al publicar borradores con IA, y las claves de localización en español e inglés.

---

## Module Responsibility

1. **`CatalogCategoryNormalizer`**:
   - Ruta: `services/core/PrototypeZero.CoreService.Contracts/Store/Categories/CatalogCategoryNormalizer.cs`
   - Función: Provee los métodos `Normalize(string? name)` y `AreEquivalent(string? a, string? b)` para eliminar diacríticos, mayúsculas y espacios redundantes.
2. **`CatalogCategoryAppService`**:
   - Ruta: `services/core/PrototypeZero.CoreService/Store/Categories/CatalogCategoryAppService.cs`
   - Función: Intercepta `CreateAsync` y `UpdateAsync` para lanzar `UserFriendlyException(L["Category:AlreadyExists"])` cuando ya exista una categoría equivalente en el tenant.
3. **`CatalogImportAppService`**:
   - Ruta: `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
   - Función: Utiliza `CatalogCategoryNormalizer.AreEquivalent` en `ResolveOrCreateCategoryAsync` para reutilizar la categoría existente si la sugerida por la IA coincide fonéticamente.
4. **Localización CoreService**:
   - Rutas: `Localizations/CoreService/es.json` y `Localizations/CoreService/en.json`
   - Función: Suministrar traducciones de `Category:AlreadyExists`.

---

## Test Reference

- **Test Files**:
  - `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryNormalizerTests.cs` (Task 01)
  - `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryDuplicateTests.cs` (Task 02)
  - `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/CatalogImportDuplicateCategoryTests.cs` (Task 02)

Todas las pruebas escritas en Task 01 y Task 02 deben pasar a verde (GREEN) al finalizar la implementación.

---

## Architecture Patterns

- **Normalización Canónica**:
  - Descomposición en `NormalizationForm.FormD` eliminando caracteres con categoría `UnicodeCategory.NonSpacingMark`.
  - Colapso de espacios intermedios consecutivos usando regex `\s+` o split-join a espacio simple.
- **Validación Multi-Tenant**:
  - El filtrado de categorías existentes debe aprovechar el filtro automático de ABP (`IMultiTenant`) o consultar con `c.TenantId == CurrentTenant.Id`.
  - En `UpdateAsync`, se debe excluir la propia categoría evaluada (`c.Id != id`) para permitir guardar la misma categoría o cambiar únicamente mayúsculas/minúsculas sin error.
- **Localización ABP**:
  - Lanzar `UserFriendlyException(L["Category:AlreadyExists"])` para que el frontend de Angular reciba el mensaje traducido en el toast/modal de error.

---

## Dependencies

- `PrototypeZero.CoreService.Contracts`
- `PrototypeZero.CoreService.Store.Categories`
- `PrototypeZero.CoreService.Store.CatalogImport`
- `Volo.Abp.Domain.Repositories`
- `Volo.Abp.MultiTenancy`
- `Volo.Abp.UserFriendlyException`

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Contracts/Store/Categories/CatalogCategoryNormalizer.cs`

**Files Modified**:
- `services/core/PrototypeZero.CoreService/Store/Categories/CatalogCategoryAppService.cs`
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
- `Localizations/CoreService/es.json`
- `Localizations/CoreService/en.json`

**Files Deleted**:
- None

---

## Test Issue Handling

Si encuentras discrepancias entre los tests de la Task 02 y las definiciones de tipos o arquitectura, **pausa y reporta** antes de modificar los tests:
1. Inconsistencias lógicas de las pruebas.
2. Desajustes en contratos de interfaces o repositorios ABP.
3. Violaciones del aislamiento multi-tenant.

**Cambios menores permitidos sin consultar**: imports faltantes, nombres de variables en pruebas, ajustes de aserción tipográfica.

---

## Implementation Checklist

- [ ] Crear `CatalogCategoryNormalizer.cs` en `PrototypeZero.CoreService.Contracts`.
- [ ] Implementar `Normalize` y `AreEquivalent` con descomposición de diacríticos y colapso de espacios.
- [ ] Agregar validación `EnsureUniqueNameAsync` en `CatalogCategoryAppService` para `CreateAsync` y `UpdateAsync`.
- [ ] Excluir la categoría actual en `UpdateAsync` para permitir actualizaciones legítimas.
- [ ] Actualizar `CatalogImportAppService.ResolveOrCreateCategoryAsync` para reutilizar categorías mediante `CatalogCategoryNormalizer.AreEquivalent`.
- [ ] Agregar las claves `"Category:AlreadyExists"` en `Localizations/CoreService/es.json` y `en.json`.
- [ ] Verificar que todas las pruebas pasen (GREEN).

---

## VERIFY: Quality Gates

Una vez finalizada la implementación, ejecutar los quality gates en orden:

### verify:quick (< 10 seconds)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCategory|FullyQualifiedName~CatalogImport"
```
**Expected**: Todas las pruebas de categorías e importación pasan exitosamente (100% GREEN).

### verify (< 45 seconds)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests
```
**Expected**: Toda la suite de CoreService pasa sin regresiones.

### verify:full (< 2 minutes)
```bash
dotnet build services/core/PrototypeZero.CoreService && dotnet test services/core/PrototypeZero.CoreService.Tests
```
**Expected**: Compilación limpia y 0 fallos en tests.

---

## Notes

**For Coding Agent**: Asegúrate de que la validación en `CatalogCategoryAppService` aplique `await Repository.GetListAsync()` (o consulta filtrada) dentro del scope del tenant actual. `IMultiTenant` de ABP aísla automáticamente por inquilino.
