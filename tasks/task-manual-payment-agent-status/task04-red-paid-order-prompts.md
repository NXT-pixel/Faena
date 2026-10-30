---
phase: red
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 04: Prompts / guardrails - Tests

**Phase:** RED (Write Tests)  
**Module:** `StoreOrderStatusInstructions` / `StorePromptConstrains` / `CustomerFacingGuardrails`  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Escribir asserts de contenido que fallen hasta que las instrucciones Store prohíban tratar «sin checkout activo» como «sin pago», obliguen tools de detalle/historial en follow-ups de envío, y eviten pedir comprobante / HITL de pago cuando `IsPaid=true`.

---

## Module Responsibility

**Files (a actualizar en GREEN)**:
- `services/ai/PrototypeZero.AiService/ChatBot/StoreOrderStatusInstructions.cs`
- `services/ai/PrototypeZero.AiService/AiAppService.cs` (`StorePromptConstrains`)
- `services/ai/PrototypeZero.AiService/ChatBot/CustomerFacingGuardrails.cs`

**Purpose**: Reglas no negociables de follow-up de estado/envío y guardrails de comprobante.

---

## Test Specification

Fuente: `test-spec-manual-payment-agent-status.md` (módulos StoreOrderStatusInstructions + StorePromptConstrains/Guardrails)

---

## Testing Conventions

Seguir `StoreCatalogDiscoveryInstructionsTests.cs` / `CustomerFacingGuardrailsTests.cs`: asserts `Assert.Contains` / `DoesNotContain` sobre strings constantes.

```csharp
public class StoreOrderStatusInstructionsTests
{
    [Fact]
    public void Tool_rules_do_not_treat_missing_open_checkout_as_unpaid()
    {
        var rules = StoreOrderStatusInstructions.ToolRules;
        Assert.Contains(/* frase acordada en GREEN */, rules, StringComparison.Ordinal);
    }
}
```

En RED, elegir frases/keywords estables que el GREEN deberá introducir (documentarlas en el assert). Si el GREEN usará wording distinto, alinear en GREEN con pause-and-report si hace falta.

---

### Test Suite: `StoreOrderStatusInstructionsTests`

**Test File**: `services/ai/PrototypeZero.AiService.Tests/ChatBot/StoreOrderStatusInstructionsTests.cs`

#### Test: Null/checkout vacío no implica unpaid
- **Given:** `StoreOrderStatusInstructions.ToolRules`
- **When:** Se inspecciona el texto
- **Then:** Contiene regla explícita de que ausencia de checkout abierto **no** significa pago no verificado

#### Test: Follow-up de envío exige GetOrderDetails / GetUserOrderHistory
- **Given:** ToolRules
- **When:** Assert de contenido
- **Then:** Exige esas tools en el turno para estado/envío (regresión + refuerzo)

#### Test: IsPaid / Pagado prohíbe comprobante y re-captura de dirección
- **Given:** ToolRules
- **When:** Assert de contenido
- **Then:** Prohíbe solicitar comprobante o dirección ya capturada cuando el tool result muestra pagado; distingue envío por preparar de deuda

#### Test: Independencia order vs shipment se mantiene
- **Given:** ToolRules
- **When:** Assert de contenido
- **Then:** Conserva que shipment status no implica unpaid (regla ya existente)

---

### Test Suite: extender `CustomerFacingGuardrailsTests` / composition o suite nueva

**Test Files**:
- `services/ai/PrototypeZero.AiService.Tests/ChatBot/CustomerFacingGuardrailsTests.cs` (extender)
- Opcional: asserts sobre `AiAppService.StorePromptConstrains` en suite dedicada o `CommercialPromptCompositionTests`

#### Test: StorePromptConstrains aclara Paid en Active como fulfillment
- **Given:** `AiAppService.StorePromptConstrains`
- **When:** Assert de contenido
- **Then:** Paid/Shipped en Active no es cart; no CreateOrder/UpdateOrder por pregunta de estado; usar GetOrderDetails/history

#### Test: Guardrails no escalan comprobante si IsPaid
- **Given:** Texto de `CustomerFacingGuardrails.Build(...)` (Store feature)
- **When:** Assert de contenido
- **Then:** No tratar imagen de comprobante como pago pendiente / no HITL por «pago no verificado» cuando tools del turno muestran `IsPaid=true`

---

## Expected RED Outcome

```bash
dotnet test services/ai/PrototypeZero.AiService.Tests --filter "FullyQualifiedName~StoreOrderStatus|FullyQualifiedName~CustomerFacingGuardrails|FullyQualifiedName~StorePrompt|FullyQualifiedName~CommercialPrompt"
```

- Tests nuevos fallan por texto ausente
- Suites preexistentes no rotas (salvo asserts nuevos)
- **No** editar producción en esta tarea

---

## Checklist

- [x] `StoreOrderStatusInstructionsTests.cs` creado
- [x] Extensiones guardrails / StorePromptConstrains creadas (`StorePaidOrderPromptTests.cs`)
- [x] `dotnet test` RED confirmado (4 failed / 12 passed en filtro ampliado)
- [x] Sin cambios GREEN de prompts

### Frases RED que GREEN debe introducir
**StoreOrderStatusInstructions:**
- `A missing open checkout does not mean the payment is unverified`
- `does not mean there is no paid order`
- `When IsPaid is true` + `do not ask for payment proof` + `do not re-ask for the delivery address`

**StorePromptConstrains:**
- `Paid or Shipped` + `not the cart` + `fulfillment`
- `Do not call CreateOrder or UpdateOrder only because the customer asked about shipping or status`

**CustomerFacingGuardrails:**
- `When IsPaid is true`
- `do not call RequestHumanIntervention for payment verification`
- `do not treat a payment-proof image as an unpaid order`

---

## Next

Arrastra: `@tasks/task-manual-payment-agent-status/task05-green-paid-order-prompts.md`
