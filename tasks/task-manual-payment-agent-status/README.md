# Manual Payment Agent Status - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/`  
**Total Tasks**: 6 (1 setup + 2 RED + 2 GREEN+VERIFY + 1 RED+GREEN)  
**Estimated Effort**: 1.5–2.5 days (~11h)

---

## Quick Start

### Prerequisites
1. Read `trd-manual-payment-agent-status.md` for technical context
2. Review `test-spec-manual-payment-agent-status.md` for test requirements
3. Confirm repo at `Proyecto/growthhacking.PrototypeZero/`

### Execution Order
Tasks 02–03 (sesión MCP) y 04–05 (prompts) pueden avanzar en paralelo tras Task 01. Task 06 solo depende de Task 01.

**TDD Discipline**:
- RED: Write tests that fail
- GREEN: Implement code to pass tests + run quality gates

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
|------|------|-------|------|------------|--------------|-------|
| 01 | Setup / fixtures | setup | XS | 0.5h | None | xunit-tester |
| 02 | Sesión MCP + historial IsPaid | red | M | 2h | 01 | xunit-tester |
| 03 | Resolver + OrderTools + DTOs | green+verify | M | 3h | 02 | aspnet-webapi-backend |
| 04 | Prompts / guardrails | red | S | 1.5h | 01 | xunit-tester |
| 05 | Prompts / guardrails | green+verify | S | 2h | 04 | aspnet-webapi-backend |
| 06 | Regresión RegisterManualPayment | red+green | M | 2h | 01 | xunit-tester |

**Legend**:
- **Size**: S (Small), M (Medium), L (Large)
- **Phase**: Setup, RED, GREEN (GREEN includes VERIFY), RED+GREEN
- **Agent**: Recommended coding agent from `/agents/coding/`

---

## Task Details

### Phase 1: Setup (Task 01)
- **Setup** (`task01-setup-fixtures.md`): Baseline Core + AiService tests; namespaces/fixtures

### Phase 2: Sesión MCP (Tasks 02–03)
- **RED** (`task02-red-commerce-session-mcp.md`): Resolver Paid fallback + `IsPaid` historial
- **GREEN** (`task03-green-commerce-session-mcp.md`): Implementar resolver, `OrderTools`, DTOs + VERIFY

### Phase 3: Prompts (Tasks 04–05)
- **RED** (`task04-red-paid-order-prompts.md`): Asserts de contenido en instrucciones/guardrails
- **GREEN** (`task05-green-paid-order-prompts.md`): Actualizar prompts + VERIFY

### Phase 4: Regresión pago manual (Task 06)
- **RED+GREEN** (`task06-red-green-manual-payment-persistence.md`): Persistencia `Paid`+`Approved`

---

## Quality Gates

### verify:quick (Core)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CustomerCommerce|FullyQualifiedName~CatalogOrderStatus|FullyQualifiedName~ManualPayment|FullyQualifiedName~OrderHistory"
```

### verify:quick (AiService)
```bash
dotnet test services/ai/PrototypeZero.AiService.Tests --filter "FullyQualifiedName~StoreOrderStatus|FullyQualifiedName~CustomerFacingGuardrails|FullyQualifiedName~CommercialRuleset|FullyQualifiedName~StorePrompt"
```

### verify:full
```bash
dotnet build services/core/PrototypeZero.CoreService
dotnet build services/ai/PrototypeZero.AiService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CustomerCommerce|FullyQualifiedName~CatalogOrderStatus|FullyQualifiedName~ManualPayment|FullyQualifiedName~OrderHistory"
dotnet test services/ai/PrototypeZero.AiService.Tests --filter "FullyQualifiedName~StoreOrderStatus|FullyQualifiedName~CustomerFacingGuardrails|FullyQualifiedName~CommercialRuleset|FullyQualifiedName~StorePrompt"
```

(Ejecutar desde `Proyecto/growthhacking.PrototypeZero`.)

---

## Progress Tracking

- [x] Task 01: Setup / fixtures (setup)
- [x] Task 02: Sesión MCP + historial IsPaid (RED)
- [x] Task 03: Resolver + OrderTools + DTOs (GREEN+VERIFY)
- [x] Task 04: Prompts / guardrails (RED)
- [x] Task 05: Prompts / guardrails (GREEN+VERIFY)
- [x] Task 06: Regresión RegisterManualPayment (RED+GREEN)

---

## References

- **TRD**: `trd-manual-payment-agent-status.md`
- **Test Spec**: `test-spec-manual-payment-agent-status.md`
- **Design**: `design-manual-payment-agent-status.md`
- **Coding Agents**: `/agents/coding/`
- **QA Handoff**: Laura (TRD §7)
- **DevOps Handoff**: Sofía (sin infra nueva)

---

## Next Step

Arrastra al chat una tarea para ejecutarla, por ejemplo:  
`@tasks/task-manual-payment-agent-status/task01-setup-fixtures.md`
