# Prevent Duplicate Categories Within Same Tenant - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/`  
**Total Tasks**: 3 (1 setup + 1 RED + 1 GREEN+VERIFY)  
**Estimated Effort**: 4 hours  

---

## Quick Start

### Prerequisites
1. Leer `trd-prevent-duplicate-categories.md` para el contexto de arquitectura y diseño.
2. Revisar `test-spec-prevent-duplicate-categories.md` para los escenarios de prueba Given-When-Then.
3. Confirmar que el repositorio de trabajo es `Proyecto/growthhacking.PrototypeZero/`.

### Execution Order
Las tareas deben ejecutarse en estricto orden secuencial. La fase RED debe completarse y fallar antes de iniciar la fase GREEN.

**TDD Discipline**:
- **Setup**: Dejar listo el scaffolding y pruebas de normalización.
- **RED**: Escribir pruebas que definan el comportamiento anti-duplicados y verificar que fallen.
- **GREEN**: Implementar la lógica para pasar las pruebas y ejecutar los quality gates.

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
|:---:|---|:---:|:---:|:---:|:---:|---|
| **01** | Setup y Pruebas Unitarias Normalizador | setup | XS | 0.5h | None | dotnet-architect |
| **02** | Suite TDD Anti-Duplicados | red | S | 1.5h | 01 | xunit-tester |
| **03** | Implementación Anti-Duplicados y Normalizador | green+verify | M | 2.0h | 02 | aspnet-webapi-backend |

**Legend**:
- **Size**: XS (<1h), S (1-2h), M (2-4h)
- **Phase**: Setup, RED, GREEN (GREEN incluye sección VERIFY con quality gates)
- **Agent**: Agente recomendado de `/agents/coding/`

---

## Task Details

### Phase 1: Setup (Task 01)
- **Setup** (`task01-setup-category-normalizer-tests.md`): Crear suite de pruebas de normalización canónica en `CatalogCategoryNormalizerTests.cs`.

### Phase 2: TDD Anti-Duplicados (Tasks 02–03)
- **RED** (`task02-red-prevent-duplicate-categories.md`): Escribir `CatalogCategoryDuplicateTests.cs` y `CatalogImportDuplicateCategoryTests.cs` evidenciando el fallo por duplicidad no controlada.
- **GREEN+VERIFY** (`task03-green-prevent-duplicate-categories.md`): Implementar `CatalogCategoryNormalizer.cs`, actualizar `CatalogCategoryAppService`, `CatalogImportAppService` y archivos de localización + ejecutar quality gates.

---

## Quality Gates

### verify:quick (< 10 seconds)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCategory|FullyQualifiedName~CatalogImport"
```

### verify (< 45 seconds)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests
```

### verify:full (< 2 minutes)
```bash
dotnet build services/core/PrototypeZero.CoreService && dotnet test services/core/PrototypeZero.CoreService.Tests
```

---

## Progress Tracking

- [x] Task 01: Setup y Pruebas Unitarias Normalizador (setup)
- [x] Task 02: Suite TDD Anti-Duplicados (red)
- [x] Task 03: Implementación Anti-Duplicados y Normalizador (green+verify)

---

## References

- **TRD**: [`trd-prevent-duplicate-categories.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-prevent-duplicate-categories/trd-prevent-duplicate-categories.md)
- **Test Spec**: [`test-spec-prevent-duplicate-categories.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-prevent-duplicate-categories/test-spec-prevent-duplicate-categories.md)
- **Design Document**: [`tasks/design-prevent-duplicate-categories.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/design-prevent-duplicate-categories.md)
- **Coding Agents**: `/agents/coding/`
- **QA Handoff**: Laura (TRD §7)
- **DevOps Handoff**: Sofía (TRD §7)
