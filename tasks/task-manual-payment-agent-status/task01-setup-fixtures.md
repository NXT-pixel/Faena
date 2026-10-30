---
phase: setup
agent: xunit-tester
agent_path: /agents/coding/xunit-tester.md
---

# Task 01: Setup / fixtures

**Phase:** Setup  
**Dependencies:** None  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Confirmar proyectos de test Core y AiService, namespaces existentes, y si hace falta un builder/fixture mínima de `CatalogOrder` para las pruebas del resolver de sesión comercial. Dejar baseline listo para fases RED.

---

## File Operations

**Files Created**:
- None (opcional: helper/fixture mínima solo si no existe patrón reutilizable)

**Files Modified**:
- None (verificación de build y baseline)

**Files Deleted**:
- None

---

## Tasks

### 1. Confirmar proyectos de tests

**Actions**:
- Ubicar `services/core/PrototypeZero.CoreService.Tests` y `services/ai/PrototypeZero.AiService.Tests`
- Revisar suites de referencia:
  - Core: `Store/Orders/CatalogOrderStatusProjectionTests.cs`, `Store/Tools/StoreMcpOrderHelper*.cs`
  - Ai: `ChatBot/StoreCatalogDiscoveryInstructionsTests.cs`, `ChatBot/CustomerFacingGuardrailsTests.cs`
- Confirmar xUnit en ambos `.csproj`

**Success Criteria**:
- Ambos proyectos de test existen y son referenciables por `dotnet test`

### 2. Baseline de compilación

**Actions**:
- Compilar `PrototypeZero.CoreService`, `PrototypeZero.CoreService.Tests`, `PrototypeZero.AiService`, `PrototypeZero.AiService.Tests`
- Documentar fallos de baseline previos (no corregir fuera de alcance)

**Success Criteria**:
- Build exitoso o fallos preexistentes claramente identificados

### 3. Inspectores de entidad / fixtures

**Actions**:
- Revisar cómo se construye `CatalogOrder` en tests existentes (constructors, status setters)
- Anotar namespace destino para `CustomerCommerceSessionResolver` (`Store/Orders` o `Store/Tools`)
- Confirmar ubicación de `CatalogOrderHistoryEntryMcpDto` y `CatalogOrderPaymentAppService`

**Success Criteria**:
- Rutas y convenciones documentadas mentalmente para Task 02/04/06; entorno listo para RED

---

## Verification

```bash
# Desde Proyecto/growthhacking.PrototypeZero/
dotnet build services/core/PrototypeZero.CoreService
dotnet build services/ai/PrototypeZero.AiService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogOrderStatus"
dotnet test services/ai/PrototypeZero.AiService.Tests --filter "FullyQualifiedName~CustomerFacingGuardrails|FullyQualifiedName~StoreCatalogDiscovery"
```

---

## Checklist

- [x] Proyectos Core/AiService Tests localizados y compilables
- [x] Baseline de build ejecutado
- [x] Suites de referencia y patrón de fixtures de `CatalogOrder` identificados
- [x] Entorno listo para Task 02 / 04 / 06

---

## Setup Notes (para RED)

| Item | Ruta / convención |
| :--- | :--- |
| Core tests | `services/core/PrototypeZero.CoreService.Tests` (xUnit 2.9.3) |
| AiService tests | `services/ai/PrototypeZero.AiService.Tests` (xUnit 2.9.3) |
| Namespace resolver | `PrototypeZero.CoreService.Store.Orders` → helper junto a `CatalogOrderStatusProjection`; tests en `...Tests/Store/Orders/` |
| Fixture `CatalogOrder` | `new CatalogOrder { Status = ..., OrderNumber = ..., Items = [...] }`; Id vía reflection si hace falta (`CatalogOrderPaymentLinkEligibilityTests.CreatePayableOrder`) |
| History DTO | `...Contracts/Store/Orders/Mcp/CatalogOrderHistoryEntryMcpDto.cs` — **sin** `IsPaid` aún |
| Payment AppService | `Store/Payments/PaymentAppService.cs` → `CatalogOrderPaymentAppService` |
| Prompt test style | `StoreCatalogDiscoveryInstructionsTests` / `CustomerFacingGuardrailsTests` (`Assert.Contains`) |
| Baseline | Core `CatalogOrderStatus*` OK; Ai `CustomerFacingGuardrails` + `StoreCatalogDiscovery` → 14 passed |
| Warnings preexistentes | NU190x MessagePack/OpenApi/ImageSharp/Pkcs; MSB3277 EF Relational 10.0.7 vs 10.0.9 en AiTests — fuera de alcance |

No se creó fixture compartida nueva: el patrón object-initializer es suficiente para Task 02.

---

## Next

Arrastra: `@tasks/task-manual-payment-agent-status/task02-red-commerce-session-mcp.md`  
(en paralelo tras setup: `@tasks/task-manual-payment-agent-status/task04-red-paid-order-prompts.md` o `task06-...`)
