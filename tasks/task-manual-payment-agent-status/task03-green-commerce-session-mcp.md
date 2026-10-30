---
phase: green
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 03: Resolver + OrderTools + DTOs - Implementation

**Phase:** GREEN (Implement Code) + VERIFY  
**Module:** `CustomerCommerceSessionResolver` / `OrderTools` / MCP DTOs  
**Dependencies:** Task 02 (RED phase must be complete)  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Implementar el resolver de sesión comercial, cablearlo en `GetCustomerActiveCommerceOrder` (fallback Paid/Shipped + ReminderHint + `NewPurchaseAllowed = true` en lugar de `null`), y exponer `IsPaid` en el historial MCP. Ejecutar quality gates hasta verde.

---

## Module Responsibility

**Files**:
- `services/core/PrototypeZero.CoreService/Store/Orders/CustomerCommerceSessionResolver.cs` (nuevo; o path acordado en Task 01)
- `services/core/PrototypeZero.CoreService/Store/Tools/OrderTools.cs`
- `services/core/PrototypeZero.CoreService.Contracts/Store/Orders/Mcp/CatalogOrderHistoryEntryMcpDto.cs`
- `services/core/PrototypeZero.CoreService.Contracts/Store/Orders/Mcp/CustomerActiveCommerceOrderMcpDto.cs` (solo si hace falta documentar/usar campos existentes)

**Purpose**: La tool de sesión activa no debe confundir «sin checkout» con «sin pago».

**Key Functions**:
- `SelectActiveOrLatestFulfillable` / `BuildPaidFulfillmentReminderHint`
- `GetCustomerActiveCommerceOrder` — usar resolver; mapear Paid fulfillable con hint
- `GetUserOrderHistory` — poblar `IsPaid`

---

## Test Reference

**Test Files** (Task 02):
- `.../Tests/Store/Orders/CustomerCommerceSessionResolverTests.cs`
- `.../Tests/Store/Orders/CatalogOrderHistoryIsPaidTests.cs` (si separado)

Leer los tests RED para el contrato. Todos deben pasar tras la implementación.

---

## Architecture Patterns

Seguir TRD §2–§4:

- Precedencia: Draft/PendingPayment > OnCredit/PaymentReminder > último Paid/Shipped
- Paid fulfillable: `NewPurchaseAllowed = true`; ReminderHint prohíbe pedir pago / reiniciar checkout; mutaciones ya fallan fuera de Draft/PendingPayment
- No cambiar semántica Wompi ni crédito
- `IsPaid` vía `CatalogOrderStatusProjection.IsPaid`

---

## Coding Conventions

- Estilo existente en `OrderTools` / Store Orders
- Sin dependencias NuGet nuevas
- Helper estático/puro preferido para unit-test sin host MCP
- Actualizar `[Description]` de `GetCustomerActiveCommerceOrder` si el contrato cambia (Paid fallback)

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService/Store/Orders/CustomerCommerceSessionResolver.cs` (o path elegido)

**Files Modified**:
- `services/core/PrototypeZero.CoreService/Store/Tools/OrderTools.cs`
- `services/core/PrototypeZero.CoreService.Contracts/Store/Orders/Mcp/CatalogOrderHistoryEntryMcpDto.cs`

**Files Deleted**:
- None

---

## Test Issue Handling

If you encounter issues with the tests from Task 02, **pause and report** rather than silently fixing tests. Report issues in these categories:

1. **Test Logic Inconsistencies**
2. **Schema/Type Mismatches**
3. **Architectural Violations**
4. **Missing Critical Coverage**
5. **Test Data/Mock Inconsistencies**
6. **Impossible Expectations**
7. **Validation Rule Conflicts**
8. **Integration Point Mismatches**
9. **Test Setup Problems**
10. **Ambiguous Requirements**

**Minor fixes allowed without asking**: typos, missing imports, helper usage, formatting, mock boilerplate.

---

## Implementation Notes

- No snippets de solución completos: el agente implementa según tests + TRD
- Al mapear Paid: reutilizar campos del DTO existentes (`Status`, `ReminderHint`, `NewPurchaseAllowed`, items/address del pedido)
- No incluir Paid en el filtro “open checkout” usado para mutaciones; el fallback es solo lectura/fulfillment

---

## VERIFY

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet build services/core/PrototypeZero.CoreService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CustomerCommerceSessionResolver|FullyQualifiedName~CatalogOrderHistoryIsPaid|FullyQualifiedName~CatalogOrderStatus"
```

**Expected**: Build OK; todos los tests de Task 02 en verde.

### Verification Checklist

- [x] Resolver implementado y testeado
- [x] `GetCustomerActiveCommerceOrder` usa fallback Paid/Shipped (no null ambiguo)
- [x] ReminderHint de Paid correcto
- [x] `IsPaid` en historial MCP
- [x] Quality gates verdes
- [x] Sin cambios fuera de alcance (Wompi, OCR, Angular)

---

## Checklist

- [x] Implementación completa según RED
- [x] VERIFY ejecutado y pasando (23 passed)
- [x] Checkbox Task 03 marcado en `README.md`

---

## Next

Arrastra: `@tasks/task-manual-payment-agent-status/task04-red-paid-order-prompts.md` (si aún no) o continuar con Task 05/06
