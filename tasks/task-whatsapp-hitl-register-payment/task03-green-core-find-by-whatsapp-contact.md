---
phase: green
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 03: Core FindByWhatsAppContactId - Implementation

**Phase:** GREEN (Implement Code)  
**Module:** `CatalogCustomerAppService.FindByWhatsAppContactIdAsync`  
**Dependencies:** Task 02 (RED phase must be complete)  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Implementar `FindByWhatsAppContactIdAsync` en contrato e implementación Core para devolver el `CatalogCustomerDto` del tenant actual vinculado al contact id, o `null`. Hacer pasar los tests de Task 02 y correr quality gates.

---

## Module Responsibility

**File**: `services/core/PrototypeZero.CoreService/Store/Customers/CatalogCustomerAppService.cs`

**Purpose**: Resolver un cliente de tienda del tenant actual por `WhatsAppContactId` exacto.

**Key Functions**:
- `FindByWhatsAppContactIdAsync(Guid whatsAppContactId): Task<CatalogCustomerDto?>` — match exacto + tenant; Guid vacío → `null`

**Contracts**: Declarar en `ICatalogCustomerAppService`; exponer vía convención ABP o atributo HTTP alineable al proxy Angular (Task 05).

---

## Test Reference

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/Customers/CatalogCustomerFindByWhatsAppContactIdTests.cs` (from Task 02)

Read the tests from Task 02 to understand required behavior. All tests must pass after implementation.

---

## Architecture Patterns

- AppService ABP con autorización `StorePermissions.Customers.Default` (mismo listado).
- Filtrar por `CurrentTenant.Id` y `WhatsAppContactId`; no cruzar tenants.
- Mapear con `ObjectMapper` / patrón ya usado en `GetListAsync` / `GetDetailAsync`.
- Sin migración EF (`WhatsAppContactId` ya existe).

Full patterns: [system-patterns.md](/tasks/context/system-patterns.md). Skills: `abp-core`, `dotnet-patterns`, `csharp-testing`.

---

## Coding Conventions

Follow `rules/project/company-standards.md` and domain skills:

- Validar entrada en AppService/DTO; sin lógica de negocio en controllers.
- Excepciones de dominio / retornos null explícitos; no `try/catch` vacíos.
- TDD: no debilitar ni borrar tests para obtener verde.

---

## Dependencies

**Uses**:
- `IRepository<CatalogCustomer, Guid>`
- `CurrentTenant`
- `ObjectMapper` / mapeo a `CatalogCustomerDto`
- `StorePermissions.Customers.Default`

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `services/core/PrototypeZero.CoreService.Contracts/Store/Customers/ICatalogCustomerAppService.cs`
- `services/core/PrototypeZero.CoreService/Store/Customers/CatalogCustomerAppService.cs`

**Files Deleted**:
- None

---

## Test Issue Handling

If you encounter issues with the tests from Task 02, **pause and report** rather than silently fixing tests. Categories: logic inconsistencies, schema/type mismatches, architectural violations, missing coverage, mock inconsistencies, impossible expectations, validation conflicts, integration mismatches, brittle setup, ambiguous requirements.

**You may fix without asking**: Typos, imports, test helper usage, formatting.

---

## Implementation Checklist

- [ ] Declarar método en `ICatalogCustomerAppService`
- [ ] Implementar `FindByWhatsAppContactIdAsync` en `CatalogCustomerAppService`
- [ ] All Task 02 tests pass (GREEN)
- [ ] No test modifications without user approval
- [ ] Route/HTTP surface usable por proxy Angular (Task 05)

---

## VERIFY: Quality Gates

### verify:quick

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"
```

**Expected**: All FindByWhatsAppContactId tests pass

### verify:full

```bash
dotnet build services/core/PrototypeZero.CoreService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"
```

**Expected**: Build OK; tests green

### Coverage Requirements

- Critical paths: match, miss, empty Guid, tenant isolation — 100%
- Error handling: empty Guid — covered

### Verification Checklist

- [ ] All Task 02 tests pass
- [ ] `verify:quick` passes
- [ ] `verify:full` passes
- [ ] No production code outside listed files

---

## Notes

**For Coding Agent**: Implement only what Task 02 requires. Do not change Angular yet (Task 05).

**TRD Reference**: `trd-whatsapp-hitl-register-payment.md`
