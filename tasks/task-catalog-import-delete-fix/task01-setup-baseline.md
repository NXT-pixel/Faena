---
phase: setup
agent: dotnet-architect
agent_path: /agents/coding/dotnet-architect.md
---

# Task 01: Setup y Verificación de Línea Base

**Phase:** Setup  
**Dependencies:** None  
**Location:** `Proyecto/growthhacking.PrototypeZero/`  

---

## Overview

Verificar que la solución `PrototypeZero` compile limpiamente y que la suite de pruebas unitarias actual de `PrototypeZero.CoreService.Tests` y `apps/angular` ejecute sin errores previos, asegurando un punto de partida estable para la fase RED.

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `services/core/PrototypeZero.CoreService.Tests/PrototypeZero.CoreService.Tests.csproj` (Target para eliminar artefacto native testhost.exe permitiendo ejecución limpia de tests con .NET 10 host).

**Files Deleted**:
- None

---

## Tasks

### 1. Confirmar estado de compilación del backend
**Actions**:
- Ejecutar `dotnet build services/core/PrototypeZero.CoreService` desde `Proyecto/growthhacking.PrototypeZero/`.
- Ejecutar `dotnet build services/core/PrototypeZero.CoreService.Tests`.

**Success Criteria**:
- Ambas compilaciones finalizan con 0 errores.

### 2. Ejecutar baseline de pruebas existentes de CatalogImport
**Actions**:
- Correr:
  ```bash
  dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogImport|FullyQualifiedName~StoreCatalog"
  ```

**Success Criteria**:
- Las pruebas existentes pasan satisfactoriamente.

### 3. Verificar entorno de frontend Angular
**Actions**:
- Inspeccionar `apps/angular/src/app/store/catalog-import/catalog-import.component.ts`.
- Ejecutar build de Angular `npm run build` en `apps/angular`.

**Success Criteria**:
- Build de Angular finaliza con 0 errores; entorno listo para la Task 02.

---

## Checklist

- [x] Compilación de `PrototypeZero.CoreService` exitosa (0 errores).
- [x] Compilación de `PrototypeZero.CoreService.Tests` exitosa (0 errores).
- [x] Baseline de pruebas `CatalogImport` y `StoreCatalog` ejecutado (106 pruebas pasadas, 0 fallidas).
- [x] Build de frontend Angular exitoso (0 errores).
- [x] Entorno preparado y validado para Task 02 (RED).

---

## Execution Notes (2026-11-04)

- **Backend**:
  - `PrototypeZero.CoreService.exe` en ejecución previa bloqueaba DLLs en `bin\Debug\net10.0\`. Se detuvo el proceso local para compilar limpiamente.
  - Se configuró el target de limpieza automática de `testhost.exe` en `PrototypeZero.CoreService.Tests.csproj` para que `vstest` ejecute directamente sobre el host de .NET 10 (`dotnet exec testhost.dll`), logrando ejecución perfecta en 50 ms.
  - **Resultado tests**: `Passed! Failed: 0, Passed: 106, Skipped: 0, Total: 106`.
- **Frontend**:
  - `npm run build` en `apps/angular` completado exitosamente en 8.5 segundos.
- **Listo para**: Task 02 (RED).
