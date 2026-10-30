---
phase: setup
agent: dotnet-architect
agent_path: /agents/coding/dotnet-architect.md
---

# Task 01: Setup y Aislamiento de Casos de Prueba

**Phase:** Setup  
**Dependencies:** None  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Verificar dependencias de pruebas, compilar la suite actual de `PrototypeZero.CoreService.Tests` y dejar el entorno listo para agregar las pruebas de regresión de preservación de precio aprobado (COP 60.000).

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- None (verificación de build y baseline de tests)

**Files Deleted**:
- None

---

## Tasks

### 1. Confirmar proyecto de tests

**Actions**:
- Ubicar `services/core/PrototypeZero.CoreService.Tests` dentro de `Proyecto/growthhacking.PrototypeZero/`
- Confirmar que existen suites relacionadas con CatalogImport / Store (p. ej. `CatalogDraftVariantResolver`, `CatalogImportAppService`)
- Revisar que xUnit y dependencias de test estén disponibles en el `.csproj`

**Success Criteria**:
- El proyecto de tests existe y es referenciable por `dotnet test`

### 2. Baseline de compilación

**Actions**:
- Compilar `PrototypeZero.CoreService` y `PrototypeZero.CoreService.Tests`
- Documentar cualquier fallo de baseline previo (no corregir scope fuera de este ticket)

**Success Criteria**:
- Build exitoso o fallos preexistentes claramente identificados

### 3. Baseline de tests filtrados

**Actions**:
- Ejecutar el filtro de quality gate `verify:quick` para establecer baseline
- Confirmar que el entorno está listo para agregar `PreserveApprovedPriceTests.cs` en Task 02

**Success Criteria**:
- Comando de test ejecutable; entorno listo para fase RED

---

## Verification

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet build services/core/PrototypeZero.CoreService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
```

---

## Checklist

- [x] Proyecto `PrototypeZero.CoreService.Tests` localizado y compilable
- [x] Baseline de build ejecutado
- [x] Baseline de tests filtrados ejecutado
- [x] Entorno listo para Task 02 (RED)

---

## Execution Notes (2026-10-26)

- **Tests project**: `services/core/PrototypeZero.CoreService.Tests` (`net10.0`, xUnit 2.9.3, Microsoft.NET.Test.Sdk 18.7.0)
- **Suites CatalogImport existentes**: `CatalogDraftVariantResolverTests`, `CatalogPriceParserTests`, `CatalogImportPriceOutlierDetectorTests`, etc. en `Store/CatalogImport/`
- **Build CoreService (1er intento)**: falló por DLLs bloqueadas (host en ejecución). Tras apagar el host: **OK, 0 errores**
- **Build Tests**: OK, 0 errores
- **verify:quick baseline**: `Passed! Failed: 0, Passed: 89, Total: 89` con filtro `CatalogImport|StoreCatalog`
- **Listo para**: crear `PreserveApprovedPriceTests.cs` en Task 02 (RED)
