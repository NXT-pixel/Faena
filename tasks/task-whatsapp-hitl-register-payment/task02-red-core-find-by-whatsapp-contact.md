---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 02: Core FindByWhatsAppContactId - Tests

**Phase:** RED (Write Tests)  
**Module:** `CatalogCustomerAppService.FindByWhatsAppContactIdAsync`  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Escribir pruebas xUnit que fallen demostrando: match por `WhatsAppContactId` en el tenant actual; `null` si no hay cliente; `null` si Guid vacío; aislamiento multi-tenant; mapeo de nombre/teléfono en el DTO.

---

## Module Responsibility

**File**: `services/core/PrototypeZero.CoreService/Store/Customers/CatalogCustomerAppService.cs`

**Purpose**: Resolver un cliente de tienda del tenant actual por `WhatsAppContactId` exacto.

**Key Functions**:
- `FindByWhatsAppContactIdAsync(Guid whatsAppContactId): Task<CatalogCustomerDto?>` — cliente con contact id + tenant, o `null`

---

## Test Specification

Fuente: `test-spec-whatsapp-hitl-register-payment.md` → suite `CatalogCustomerFindByWhatsAppContactId`

---

## Testing Conventions

Testing conventions come from the client repo, not from this harness:

1. Read `AdminStoreCustomerWhatsAppServiceTests.cs` (u otro test cercano en `Store/Customers`).
2. Copy naming, Arrange-Act-Assert y factories locales.
3. Prefer unit tests con repositorio/stubs sobre integración completa si el módulo bajo prueba puede aislarse; si el AppService exige host ABP, seguir el patrón de tests de AppService ya usado en Core.Tests.

Do not invent a testing style.

```csharp
public class CatalogCustomerFindByWhatsAppContactIdTests
{
    [Fact]
    public async Task Returns_customer_when_WhatsAppContactId_matches_current_tenant()
    {
        // Arrange / Act / Assert — agent fills in
    }
}
```

---

### Test Suite: `CatalogCustomerFindByWhatsAppContactId`

#### Test: Returns_customer_when_WhatsAppContactId_matches_current_tenant
- **Given:** Tenant T1; cliente C con `WhatsAppContactId = G1`
- **When:** `FindByWhatsAppContactIdAsync(G1)` bajo T1
- **Then:** DTO con `Id = C.Id`, `WhatsAppContactId = G1`

#### Test: Returns_null_when_no_customer_has_contact_id
- **Given:** Tenant T1; clientes sin `WhatsAppContactId` o con otro Guid
- **When:** `FindByWhatsAppContactIdAsync(G_unknown)`
- **Then:** `null`

#### Test: Returns_null_when_whatsAppContactId_is_empty
- **Given:** Cualquier estado de repositorio
- **When:** `FindByWhatsAppContactIdAsync(Guid.Empty)`
- **Then:** `null` sin depender de un match accidental

#### Test: Does_not_return_customer_from_another_tenant
- **Given:** Cliente en T2 con `WhatsAppContactId = G1`; current tenant T1
- **When:** `FindByWhatsAppContactIdAsync(G1)` bajo T1
- **Then:** `null`

#### Test: Maps_whatsapp_phone_and_name_on_dto
- **Given:** Cliente match con `FullName` y `WhatsappPhone` poblados
- **When:** Find exitoso
- **Then:** DTO expone esos campos

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/Customers/CatalogCustomerFindByWhatsAppContactIdTests.cs`

---

## Test Data & Fixtures

- Factory local de `CatalogCustomer` con `TenantId`, `WhatsAppContactId`, `WhatsappPhone`, `FullName` (patrón `AdminStoreCustomerWhatsAppServiceTests`)
- Guids distintos para T1/T2 y contact ids

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/Customers/CatalogCustomerFindByWhatsAppContactIdTests.cs`

**Files Modified**:
- None

**Files Deleted**:
- None

---

## Success Criteria

- [x] All tests written following GWT / AAA
- [x] Test file created at specified path
- [x] Tests run and FAIL (RED) por método ausente o comportamiento incorrecto
- [x] No implementation code written in production projects

---

## RED Evidence (2026-11-12)

```text
error CS1061: "CatalogCustomerAppService" no contiene una definición para
"FindByWhatsAppContactIdAsync" ... (×5, líneas 36/54/65/80/95 del test file)
EXIT=1
```

Log: `tasks/task-whatsapp-hitl-register-payment/red-task02-build.log`

Razón correcta: comportamiento ausente (método aún no implementado). Sin cambios en producción.

---

## Notes

**For Coding Agent**: Write comprehensive tests that define the behavior. Tests should fail initially. Do not write any implementation code.

**TRD Reference**: See `trd-whatsapp-hitl-register-payment.md` §4–§6.

**Verify RED**:

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"
```
