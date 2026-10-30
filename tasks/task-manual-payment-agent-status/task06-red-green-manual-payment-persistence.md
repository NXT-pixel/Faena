---
phase: red-green
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 06: Regresión RegisterManualPayment - RED + GREEN

**Phase:** RED + GREEN (Write failing test, then fix only if needed) + VERIFY  
**Module:** `CatalogOrderPaymentAppService` (`RegisterManualPayment`)  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Confirmar en backend que el pago manual deja el pedido `Paid` y el `Payment` en `Approved`. Escribir el test de regresión primero (RED). Solo modificar `PaymentAppService.cs` si el test revela una regresión real de persistencia; si ya pasa en GREEN inmediato, documentarlo — el bug de producto sigue siendo el agente/MCP (Tasks 02–05).

---

## Module Responsibility

**File**: `services/core/PrototypeZero.CoreService/Store/Payments/PaymentAppService.cs`  
**Class**: `CatalogOrderPaymentAppService`

**Purpose**: Tras `RegisterManualPayment`, estado financiero persistido = pagado/aprobado.

**Key Function**:
- `RegisterManualPayment(CreatePaymentDto input)` — inserta Payment Approved, setea `CatalogOrder.Status = Paid`, publica notificación

---

## Test Specification

Fuente: `test-spec-manual-payment-agent-status.md` → `RegisterManualPaymentPersistenceTests`

---

## Testing Conventions

Preferir el harness más simple que el repo permita (unit con repos mock/fakes, o test integrado ABP si ya existe patrón para AppServices Store). Revisar tests cercanos (`CatalogOrderPaymentLinkEligibilityTests`, etc.) antes de inventar infraestructura pesada.

Si el harness completo de UoW/event bus es demasiado costoso para este ticket: extraer y testear la transición de estado (order+payment) en un helper de dominio **solo** si el Tech Lead/TRD lo permiten; default = test de AppService o documentación explícita de bloqueo + smoke manual para Laura.

---

## RED Phase

### Test Suite: `RegisterManualPaymentPersistenceTests`

**Test File**: `services/core/PrototypeZero.CoreService.Tests/Store/Payments/RegisterManualPaymentPersistenceTests.cs`

#### Test: RegisterManualPayment deja order Paid y payment Approved
- **Given:** Pedido `PendingPayment` con total positivo; precondiciones de shipping satisfechas o shipping deshabilitado según fixture viable
- **When:** `RegisterManualPayment(CreatePaymentDto)` con amount = total
- **Then:** `order.Status == Paid`; existe `Payment` con `Status == Approved` y `RelatedEntityId == order.Id`

#### Test: Tras pago manual el estado no vuelve a PendingPayment al releer
- **Given:** Pedido ya `Paid` tras registro
- **When:** Se relee desde repositorio
- **Then:** Sigue `Paid`

**RED success**: Test escrito; falla por setup/implementación incorrecta **o** se vuelve verde de inmediato (comportamiento ya correcto) — en ambos casos continuar a VERIFY.

---

## GREEN Phase (solo si falla)

**Files Modified** (condicional):
- `services/core/PrototypeZero.CoreService/Store/Payments/PaymentAppService.cs`

**Rules**:
- No rediseñar flujo Wompi / crédito salvo bug colateral demostrado
- No tocar notificaciones WhatsApp salvo que el test de persistencia lo exija
- Si el fallo es de test harness (categoría 9), pause-and-report

---

## File Operations

**Files Created**:
- `services/core/PrototypeZero.CoreService.Tests/Store/Payments/RegisterManualPaymentPersistenceTests.cs`

**Files Modified**:
- `PaymentAppService.cs` — **solo si** el test demuestra regresión de persistencia

**Files Deleted**:
- None

---

## Test Issue Handling

Pause-and-report para categorías 1–10 del protocolo. Si no es viable montar AppService test sin infra excesiva, reportar al usuario con alternativa (test de proyección de estado + checklist QA Laura) antes de abandonar cobertura.

---

## VERIFY

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~RegisterManualPayment|FullyQualifiedName~ManualPayment"
```

### Verification Checklist

- [x] Suite de persistencia creada (`RegisterManualPaymentPersistenceTests` + `ManualCatalogOrderPayment`)
- [x] Pedido Paid + Payment Approved demostrados por test (2 passed; sin bug de persistencia)
- [x] `PaymentAppService` refactor mínimo para usar helper testeable (comportamiento idéntico)
- [x] Checkbox Task 06 en `README.md`

---

## Handoff note

Tras Tasks 02–06: resumen para Laura (TRD §7) — flujo ManualVerification → RegisterManualPayment → WhatsApp «¿Cuándo lo envían?» sin pedir comprobante de nuevo.
