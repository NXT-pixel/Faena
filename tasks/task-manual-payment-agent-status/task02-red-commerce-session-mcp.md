---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 02: Sesión MCP + historial IsPaid - Tests

**Phase:** RED (Write Tests)  
**Module:** `CustomerCommerceSessionResolver` / historial MCP `IsPaid`  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Escribir pruebas que fallen evidenciando: (1) con solo pedido `Paid` la sesión comercial no es null y expone hint de fulfillment; (2) `Draft`/`PendingPayment`/`OnCredit` tienen prioridad sobre `Paid`; (3) historial MCP expone `IsPaid=true` para Paid/Shipped.

---

## Module Responsibility

**Files (a implementar en GREEN)**:
- `services/core/PrototypeZero.CoreService/Store/Orders/CustomerCommerceSessionResolver.cs` (o bajo `Store/Tools/`)
- `services/core/PrototypeZero.CoreService/Store/Tools/OrderTools.cs`
- `services/core/PrototypeZero.CoreService.Contracts/Store/Orders/Mcp/CatalogOrderHistoryEntryMcpDto.cs`

**Purpose**: Seleccionar checkout/crédito abierto o último fulfillable pagado; exponer `IsPaid` en historial.

**Key Functions**:
- `SelectActiveOrLatestFulfillable(IEnumerable<CatalogOrder> orders): CatalogOrder?`
- `BuildPaidFulfillmentReminderHint(CatalogOrder order): string`
- Proyección `IsPaid` en entradas de historial

---

## Test Specification

Fuente: `test-spec-manual-payment-agent-status.md` (módulos Resolver + History)

---

## Testing Conventions

xUnit + Arrange/Act/Assert. Seguir estilo de `CatalogOrderStatusProjectionTests.cs`. Preferir unit tests puros sobre el resolver (sin levantar MCP host).

```csharp
public sealed class CustomerCommerceSessionResolverTests
{
    [Fact]
    public void SelectActiveOrLatestFulfillable_WithOnlyPaid_ReturnsPaidOrder()
    {
        // Arrange / Act / Assert
    }
}
```

---

### Test Suite: `CustomerCommerceSessionResolverTests`

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/Orders/CustomerCommerceSessionResolverTests.cs`

#### Test: Solo pedido Paid → retorna ese pedido
- **Given:** Lista con un `CatalogOrder` `Paid` (y opcionalmente `Shipped` legacy)
- **When:** `SelectActiveOrLatestFulfillable(orders)`
- **Then:** Retorna ese pedido; no retorna null

#### Test: Draft tiene prioridad sobre Paid
- **Given:** Un `Draft` y un `Paid`
- **When:** Se selecciona la sesión
- **Then:** Retorna el `Draft`

#### Test: PendingPayment tiene prioridad sobre Paid
- **Given:** `PendingPayment` y `Paid`
- **When:** Se selecciona la sesión
- **Then:** Retorna `PendingPayment`

#### Test: OnCredit / PaymentReminder tienen prioridad sobre Paid
- **Given:** `OnCredit` (o `PaymentReminder`) y `Paid`
- **When:** Se selecciona la sesión
- **Then:** Retorna el de crédito/recordatorio

#### Test: Cancelled no se usa como fulfillable
- **Given:** Solo pedidos `Cancelled`
- **When:** Se selecciona la sesión
- **Then:** Retorna null

#### Test: Hint de Paid prohíbe reinicio de pago/checkout
- **Given:** Pedido `Paid` con `OrderNumber` conocido
- **When:** `BuildPaidFulfillmentReminderHint(order)`
- **Then:** Texto indica pagado/fulfillment; menciona `GetOrderDetails`; no pide payment link ni reiniciar checkout

---

### Test Suite: `CatalogOrderHistoryIsPaidTests`

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/Orders/CatalogOrderHistoryIsPaidTests.cs`  
(o métodos en el mismo archivo si el estilo del repo agrupa)

#### Test: Historial marca IsPaid en Paid/Shipped
- **Given:** Pedidos `Paid` y `PendingPayment`
- **When:** Se proyecta `IsPaid` (propiedad DTO o helper de mapping)
- **Then:** Paid/Shipped → true; PendingPayment → false

#### Test: GetOrderDetails / proyección IsPaid regresión
- **Given:** Status `Paid`
- **When:** `CatalogOrderStatusProjection.IsPaid(status)` (o mapping de detalle)
- **Then:** true; label comercial Pagado ya cubierto por proyección existente

---

## Expected RED Outcome

```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CustomerCommerceSessionResolver|FullyQualifiedName~CatalogOrderHistoryIsPaid"
```

- Compilan los archivos de test
- Fallan por tipo/método/`IsPaid` ausente (razón correcta)
- **No** implementar producción en esta tarea

---

## Checklist

- [x] `CustomerCommerceSessionResolverTests.cs` creado con casos de precedencia y hint
- [x] Tests de `IsPaid` en historial/proyección creados
- [x] `dotnet test` ejecutado; fallos por ausencia de implementación
- [x] Ningún cambio GREEN de producción

### RED evidence
- `CS0103`: `CustomerCommerceSessionResolver` no existe
- `CS0117` / `CS1061`: `CatalogOrderHistoryEntryMcpDto.IsPaid` no existe

---

## Next

Arrastra: `@tasks/task-manual-payment-agent-status/task03-green-commerce-session-mcp.md`
