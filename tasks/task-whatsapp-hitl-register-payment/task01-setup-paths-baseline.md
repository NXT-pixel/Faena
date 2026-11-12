---
phase: setup
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 01: Setup paths / baseline

**Phase:** Setup  
**Dependencies:** None  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Confirmar rutas de Core/Angular afectadas, permisos `Store.Customers` / `Store.Payments.Create`, y los comandos reales de test (`dotnet test`, Karma/Jasmine) antes de las fases RED.

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- None (solo verificación)

**Files Deleted**:
- None

---

## Tasks

### 1. Confirmar rutas Core

**Actions**:
- Ubicar `services/core/PrototypeZero.CoreService/Store/Customers/CatalogCustomerAppService.cs`
- Ubicar `services/core/PrototypeZero.CoreService.Contracts/Store/Customers/ICatalogCustomerAppService.cs`
- Revisar tests de referencia: `services/core/PrototypeZero.CoreService.Tests/Store/Customers/AdminStoreCustomerWhatsAppServiceTests.cs`
- Confirmar que `CatalogCustomer` ya expone `WhatsAppContactId`

**Success Criteria**:
- Rutas y namespaces listos para Task 02/03

### 2. Confirmar rutas Angular / WhatsApp HITL

**Actions**:
- Ubicar `apps/angular/src/app/whatsapp/conversations/conversation-detail/conversation-detail.component.ts` (`registerPayment`)
- Ubicar proxy `apps/angular/src/app/proxy/core-service/store/customers/catalog-customer.service.ts`
- Revisar patrón de util+spec: `whatsapp-contact-label.util.ts` / `.spec.ts`
- Revisar cómo se lanza Karma: `apps/angular/package.json` scripts `test`

**Success Criteria**:
- Comando de test Angular documentado para Tasks 04/05 (si `--include` no aplica, anotar filtro equivalente)

### 3. Permisos y localización

**Actions**:
- Confirmar `StorePermissions.Customers.Default` / `ViewProfile` y UI `Store.Payments.Create` en el botón HITL
- Ubicar `HITL:NoMatchingCustomer` / `HITL:NoPayableOrder` en `Localizations/WhatsAppService/{es,en}.json`

**Success Criteria**:
- Permisos y keys de localización identificados; sin cambios de código en esta tarea

### 4. Baseline de build / test smoke

**Actions**:
- `dotnet build` Core + Tests
- Smoke opcional de un filtro existente en Core.Tests
- No corregir fallos preexistentes fuera de alcance; documentarlos si aparecen

**Success Criteria**:
- Build usable o fallos baseline claramente anotados

---

## Verification

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet build services/core/PrototypeZero.CoreService
dotnet build services/core/PrototypeZero.CoreService.Tests
# Opcional: smoke
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~AdminStoreCustomerWhatsApp"
```

---

## Baseline Notes (2026-11-12)

### Core
- `CatalogCustomerAppService.cs`, `ICatalogCustomerAppService.cs`, `CatalogCustomer.cs` (`WhatsAppContactId`), `AdminStoreCustomerWhatsAppServiceTests.cs` — **OK**
- Namespace: `PrototypeZero.CoreService.Store.Customers`
- Permisos Core: `StorePermissions.Customers.Default` (Get/GetList), `Customers.ViewProfile` (GetDetail), `StorePermissions.Payments.Create` = `Store.Payments.Create`

### Angular / HITL
- `conversation-detail.component.ts` (`registerPayment`), proxy `catalog-customer.service.ts`, `whatsapp-contact-label.util(.spec).ts` — **OK**
- Botón HITL: `*abpPermission="'Store.Payments.Create'"`
- Localización: `HITL:NoMatchingCustomer` / `HITL:NoPayableOrder` en `Localizations/WhatsAppService/{es,en}.json`

### Comando Karma/Jasmine real
- `package.json` **no** define script `"test"` (solo `ng`, `build`, `lint`, …).
- Target existe en `angular.json` → `"test": { "builder": "@angular/build:karma", "karmaConfig": "karma.conf.js" }`.
- Comando esperado (tras `yarn`/`npm install` en `apps/angular`):
  ```bash
  npx ng test --watch=false --browsers=ChromeHeadless --include=**/hitl-register-payment.util.spec.ts
  npx ng test --watch=false --browsers=ChromeHeadless --include=**/conversation-detail*.spec.ts
  ```
  Si `--include` no filtra en esta versión del builder, correr `npx ng test --watch=false --browsers=ChromeHeadless` y validar por nombre de suite.
- `yarn` no está en PATH de esta máquina; Node `v26.13.0` sí. `node_modules` **ausente** en `apps/angular` en este entorno.

### Baseline build / smoke
- **`dotnet` no está instalado / no está en PATH** en este entorno (búsqueda en Program Files / LocalAppData / PATH: sin `dotnet.exe`).
- No se pudo ejecutar `dotnet build` ni el smoke `AdminStoreCustomerWhatsApp`.
- **Acción para Tasks 02+:** instalar/habilitar .NET 10 SDK (`10.0.402` per tech-context) y restaurar deps Angular antes de RED/GREEN. No es un fallo del código del cliente.

---

## Checklist

- [x] Rutas Core / contrato / entidad confirmadas
- [x] Rutas Angular HITL + proxy + util patrón confirmadas
- [x] Comando Karma/Jasmine real anotado
- [x] Permisos y keys HITL localizados
- [x] Baseline build OK o fallos preexistentes documentados
