---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 02: Preservación de Precio y Sincronización de Variantes - Tests

**Phase:** RED (Write Tests)  
**Module:** `CatalogImportAppService` / `CatalogDraftVariantResolver` / `CatalogProductDraftMapper`  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Crear pruebas unitarias y de integración que fallen evidenciando: (1) un borrador con precio COP 60.000 no debe publicarse con precio modificado o heredado erróneamente de variantes desactualizadas (59.999); (2) la actualización del precio padre debe sincronizar o resolver variantes huérfanas de precio; (3) `PublishDraftAsync` mantiene la precisión exacta de `PriceAmount` para productos nuevos y existentes.

---

## Module Responsibility

**Files**:
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogImportAppService.cs`
- `services/core/PrototypeZero.CoreService/Store/CatalogImport/CatalogDraftVariantResolver.cs`
- `services/core/PrototypeZero.CoreService/Store/ObjectMapping/CatalogProductDraftMapper.cs`

**Purpose**: Garantizar que el precio aprobado por el operador se preserve exactamente (`decimal(18,2)`) desde borrador hasta producto publicado, sin degradación a 59.999 ni desincronización de variantes.

**Key Functions**:
- `UpdateDraftAsync(Guid id, UpdateCatalogProductDraftDto input)` - Persiste precio aprobado y sincroniza variantes
- `PublishDraftsAsync(List<Guid> draftIds)` / `PublishDraftAsync(...)` - Publica sin alterar `PriceAmount`
- `TryExpandVariants(CatalogProductDraft draft)` - Expande variantes sin sobrescribir precio aprobado
- `ParseVariants` / `SerializeVariants` / `SyncVariantPrices` - Consistencia decimal en variantes
- `ApplyUpdate` / `ToDto` - Mapeo exacto de `PriceAmount`

---

## Test Specification

Fuente: `test-spec-preserve-approved-price.md`

---

## Testing Conventions

Usar xUnit + patrones existentes en `PrototypeZero.CoreService.Tests` (Arrange / Act / Assert, nombres descriptivos Given-When-Then). Seguir convenciones de suites CatalogImport existentes.

```csharp
public class PreserveApprovedPriceTests
{
    [Fact]
    public async Task PublishDraftsAsync_WithApprovedPrice60000_PersistsExactAmount()
    {
        // Arrange / Act / Assert
    }
}
```

---

### Test Suite: `PreserveApprovedPriceTests`

#### Test: Publicar borrador simple con precio aprobado COP 60.000 persiste exactamente 60.000 en CatalogProducts
- **Given:** Un borrador en base de datos con nombre "Set en rodio", categoría "Set en rodio" y `PriceAmount = 60000.00m`
- **When:** Se ejecuta `PublishDraftsAsync([draft.Id])`
- **Then:** Se inserta en `Store.CatalogProducts` un producto con `PriceAmount = 60000.00m` y `PriceCurrency = "COP"`
- **And:** El borrador se elimina de `Store.CatalogProductDrafts`

#### Test: Publicar borrador no permite que variantes obsoletas sobreescriban el precio aprobado de 60.000 con 59.999
- **Given:** Un borrador cuyo precio aprobado fue actualizado a `60000.00m`, pero que contenía en `VariantsJson` una variante extraída previamente con `59999.00m`
- **When:** Se ejecuta la publicación del borrador
- **Then:** El producto resultante se publica con el precio confirmado de `60000.00m` y nunca con `59999.00m`

#### Test: Actualización de producto existente al republicar respeta el nuevo precio aprobado
- **Given:** Un producto ya existente en el catálogo con `Name = "Set en rodio"` y `PriceAmount = 59999.00m`
- **And:** Un nuevo borrador con el mismo nombre normalizado y `PriceAmount = 60000.00m`
- **When:** Se ejecuta `PublishDraftsAsync([draft.Id])`
- **Then:** El producto existente se actualiza a `PriceAmount = 60000.00m`

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/PreserveApprovedPriceTests.cs`

```csharp
public class PreserveApprovedPriceTests
{
    // Agent fills in: publish exact 60000, stale variant 59999 must not win, update existing product
}
```

---

### Test Suite: `CatalogDraftVariantResolver` (incluir en el mismo archivo o helpers del suite PreserveApprovedPrice según estilo del repo)

#### Test: Deserialización de variantes preserva el valor decimal exacto
- **Given:** JSON de variantes con precio `60000.00` y `59999.00`
- **When:** `CatalogDraftVariantResolver.ParseVariants(json)`
- **Then:** `PriceAmount` idéntico a `60000m` y `59999m`, sin redondeo

#### Test: Sincronización de variantes hereda el precio padre cuando no tienen precio específico
- **Given:** Borrador con precio padre actualizado a `60000.00` y variantes asociadas
- **When:** Se ejecuta sincronización de precios hacia las variantes
- **Then:** Variantes dependientes del precio base quedan en `60000.00`

#### Test: Serialización de variantes conserva los montos decimales sin mutación
- **Given:** Lista de variantes con montos enteros y decimales COP
- **When:** `SerializeVariants(variants)` y re-deserialización
- **Then:** Sin desviación de unidad

---

### Test Suite: `CatalogProductDraftMapper` (casos de regresión de precio; pueden vivir en PreserveApprovedPriceTests o extender suite existente)

#### Test: ApplyUpdate asigna el precio exacto del DTO al borrador
- **Given:** Draft con `PriceAmount = 59999.00` y DTO con `PriceAmount = 60000.00`
- **When:** `CatalogProductDraftMapper.ApplyUpdate(draft, input)`
- **Then:** `draft.PriceAmount == 60000.00m` y `PriceCurrency == "COP"`

#### Test: ToDto expone el precio aprobado sin conversiones flotantes
- **Given:** Draft con `PriceAmount = 60000.00m`
- **When:** `ToDto(draft)`
- **Then:** `dto.PriceAmount == 60000.00m`

---

## Test Data & Fixtures

Según `test-spec-preserve-approved-price.md` (Fixture conceptual `CatalogDraftPriceTestData`):
- `CreateDraft(name: "Set en rodio", price: 60000m, category: "Set en rodio")`
- `CreateDraftWithVariants(name: "Set en rodio", parentPrice: 60000m, variantPrice: 59999m)`
- Casos límite: COP 59.999, COP 60.000, COP 145.000

**Mocks sugeridos** (límites del TRD):
- `IRepository<CatalogProductDraft, Guid>`, `IRepository<CatalogProduct, Guid>`
- `IProductSearchIndexService`, `CatalogCategoryService`

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/CatalogImport/PreserveApprovedPriceTests.cs`

**Files Modified**:
- None

**Files Deleted**:
- None

---

## Success Criteria

- [x] All tests written following GWT format from test-spec
- [x] Test file created at specified path under `Proyecto/growthhacking.PrototypeZero/`
- [x] Tests run and FAIL (RED phase validation) — evidencian bug de 59.999 / pérdida de precisión
- [x] No implementation code written

---

## Notes

**For Coding Agent**: Write comprehensive tests that define the behavior. Tests should fail initially. Do not write any implementation code.

**TRD Reference**: See `trd-preserve-approved-price.md` for architecture context.  
**Test Spec Reference**: See `test-spec-preserve-approved-price.md`.
