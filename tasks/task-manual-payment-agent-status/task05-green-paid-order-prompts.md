---
phase: green
agent: aspnet-webapi-backend
agent_path: /agents/coding/aspnet-webapi-backend.md
---

# Task 05: Prompts / guardrails - Implementation

**Phase:** GREEN (Implement Code) + VERIFY  
**Module:** `StoreOrderStatusInstructions` / `StorePromptConstrains` / `CustomerFacingGuardrails`  
**Dependencies:** Task 04 (RED phase must be complete)  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Actualizar textos de orquestación Store y guardrails para alinear el agente con la sesión MCP Paid: follow-ups de envío usan tools autoritativas, no comunican deuda ni reinician checkout, y no escalan comprobante cuando `IsPaid=true`.

---

## Module Responsibility

**Files**:
- `services/ai/PrototypeZero.AiService/ChatBot/StoreOrderStatusInstructions.cs`
- `services/ai/PrototypeZero.AiService/AiAppService.cs` (`StorePromptConstrains`)
- `services/ai/PrototypeZero.AiService/ChatBot/CustomerFacingGuardrails.cs`

**Purpose**: Reglas no negociables de estado/envío y comprobante post-pago manual.

---

## Test Reference

**Test Files** (Task 04):
- `.../AiService.Tests/ChatBot/StoreOrderStatusInstructionsTests.cs`
- Extensiones en `CustomerFacingGuardrailsTests` / composition / StorePrompt tests

Leer los asserts RED: el wording de producción debe satisfacer `Assert.Contains` exactos.

---

## Architecture Patterns

TRD §4 Modules 4–5:

- Ausencia de checkout abierto ≠ unpaid
- Preguntas de estado/envío: `GetOrderDetails` / `GetUserOrderHistory` en el turno
- `IsPaid` / Pagado: no comprobante, no re-pedir dirección, no CreateOrder por esa pregunta
- Active con Status Paid/Shipped = fulfillment, no cart
- Imagen de comprobante + IsPaid: no HITL como «pago no verificado»

Conservar reglas existentes de independencia order vs shipment.

---

## Coding Conventions

- Solo strings de prompt/instrucciones; sin lógica de runtime nueva
- Mantener español/inglés según el archivo existente (hoy ToolRules en inglés)
- No tocar Wompi ni OCR
- Si `CommercialRulesetProvider` compone estas secciones, verificar que composition tests sigan verdes

---

## File Operations

**Files Created**:
- None

**Files Modified**:
- `services/ai/PrototypeZero.AiService/ChatBot/StoreOrderStatusInstructions.cs`
- `services/ai/PrototypeZero.AiService/AiAppService.cs`
- `services/ai/PrototypeZero.AiService/ChatBot/CustomerFacingGuardrails.cs`

**Files Deleted**:
- None

---

## Test Issue Handling

Pause and report (categorías 1–10 del protocolo create-tasks) si los asserts RED contradicen arquitectura o wording imposible. Minor: typos/imports/formato.

---

## VERIFY

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet build services/ai/PrototypeZero.AiService
dotnet test services/ai/PrototypeZero.AiService.Tests --filter "FullyQualifiedName~StoreOrderStatus|FullyQualifiedName~CustomerFacingGuardrails|FullyQualifiedName~CommercialRuleset|FullyQualifiedName~StorePrompt|FullyQualifiedName~CommercialPrompt"
```

**Expected**: Build OK; tests RED de Task 04 verdes; suites composition/guardrails existentes verdes.

### Verification Checklist

- [x] StoreOrderStatusInstructions actualizado
- [x] StorePromptConstrains aclara Paid fulfillment
- [x] Guardrails IsPaid / comprobante actualizados
- [x] Quality gates AiService verdes (18 passed)
- [x] Checkbox Task 05 en `README.md`

---

## Next

Completar Task 06 si falta; luego handoff QA (Laura) según TRD §7.
