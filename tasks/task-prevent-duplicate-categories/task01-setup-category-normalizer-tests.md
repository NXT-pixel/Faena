---
phase: setup
agent: dotnet-architect
agent_path: /agents/coding/dotnet-architect.md
---

# Task 01: Setup y Pruebas Unitarias Normalizador

**Phase:** Setup  
**Module:** `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryNormalizerTests.cs`  
**Dependencies:** None  

---

## Overview

Configurar la suite de pruebas unitarias para la normalización canónica de nombres de categorías (`CatalogCategoryNormalizerTests`). Esta tarea establece el baseline de testing para las reglas de comparación fonético-ortográfica (eliminación de diacríticos, mayúsculas/minúsculas y espacios en blanco colapsados).

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/Categories/CatalogCategoryNormalizerTests.cs`

**Files Modified**:
- None

**Files Deleted**:
- None

---

## Tasks

### Step 1: Estructurar la suite de pruebas para el Normalizador

**Actions**:
- Crear el directorio `services/core/PrototypeZero.CoreService.Tests/Store/Categories/` si no existe.
- Crear el archivo de pruebas `CatalogCategoryNormalizerTests.cs` con pruebas para:
  - `Normalize`: trim y lowercase de nombres estándar.
  - `Normalize`: descarte de diacríticos/tildes (`anÍllos`, `Ánillos`, `Ànillos`, `ánillös`).
  - `Normalize`: colapso de múltiples espacios intermedios (`"Set   de   anillos"` -> `"set de anillos"`).
  - `Normalize`: manejo de cadenas vacías o nulas sin excepciones.
  - `AreEquivalent`: retorno `true` ante variaciones ortográficas de la misma categoría.
  - `AreEquivalent`: retorno `false` ante categorías distintas.

**Success Criteria**:
- El archivo de pruebas compila o define el contrato exacto esperado para `CatalogCategoryNormalizer`.

---

## Verification

```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCategoryNormalizerTests"
```

---

## Checklist

- [ ] Directorio `Store/Categories/` listo en el proyecto de tests
- [ ] Pruebas unitarias de normalización creadas según la especificación
- [ ] Verificación baseline ejecutada
