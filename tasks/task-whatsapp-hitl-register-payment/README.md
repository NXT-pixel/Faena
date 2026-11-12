# WhatsApp HITL Register Payment - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/`  
**Total Tasks**: 5 (1 setup + 2 RED + 2 GREEN+VERIFY)  
**Estimated Effort**: 1–1.5 days (~8h)

---

## Quick Start

### Prerequisites
1. Read `trd-whatsapp-hitl-register-payment.md` for technical context
2. Review `test-spec-whatsapp-hitl-register-payment.md` for test requirements
3. Confirm repo at `Proyecto/growthhacking.PrototypeZero/`

### Execution Order
Task 01 first. Tasks 02–03 (Core) y 04 (Angular RED) pueden avanzar en paralelo tras 01. Task 05 depende de 03 y 04.

**TDD Discipline**:
- RED: Write tests that fail
- GREEN: Implement code to pass tests + run quality gates

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
|------|------|-------|------|------------|--------------|-------|
| 01 | Setup paths / baseline | setup | XS | 0.5h | None | xunit-tester |
| 02 | Core FindByWhatsAppContactId tests | red | S | 1.5h | 01 | xunit-tester |
| 03 | Core FindByWhatsAppContactId impl | green+verify | S | 1.5h | 02 | aspnet-webapi-backend |
| 04 | Angular HITL resolution tests | red | M | 2h | 01 | jest-tester |
| 05 | Angular HITL resolution + proxy | green+verify | M | 2.5h | 03, 04 | angular-developer |

**Legend**:
- **Size**: S (Small), M (Medium), L (Large)
- **Phase**: Setup, RED, GREEN (GREEN includes VERIFY)
- **Agent**: Recommended coding agent from `/agents/coding/`

---

## Task Details

### Phase 1: Setup (Task 01)
- **Setup** (`task01-setup-paths-baseline.md`): Confirmar rutas Core/Angular, permisos, comandos de test

### Phase 2: Core lookup (Tasks 02–03)
- **RED** (`task02-red-core-find-by-whatsapp-contact.md`): Tests `FindByWhatsAppContactIdAsync`
- **GREEN** (`task03-green-core-find-by-whatsapp-contact.md`): Contrato + AppService + VERIFY

### Phase 3: Angular HITL (Tasks 04–05)
- **RED** (`task04-red-angular-hitl-resolution.md`): Specs util + `registerPayment`
- **GREEN** (`task05-green-angular-hitl-resolution.md`): Util + componente + proxy + localización + VERIFY

---

## Quality Gates

### verify:quick (Core)
```bash
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"
```

### verify:quick (Angular)
```bash
# package.json no tiene script "test"; usar target angular.json (Task 01)
cd apps/angular
npx ng test --watch=false --browsers=ChromeHeadless --include=**/hitl-register-payment*.spec.ts
npx ng test --watch=false --browsers=ChromeHeadless --include=**/conversation-detail*.spec.ts
```

### verify:full
```bash
dotnet build services/core/PrototypeZero.CoreService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"
cd apps/angular
npx ng test --watch=false --browsers=ChromeHeadless --include=**/hitl-register-payment*.spec.ts
npx ng test --watch=false --browsers=ChromeHeadless --include=**/conversation-detail*.spec.ts
```

(Ejecutar desde `Proyecto/growthhacking.PrototypeZero` salvo `cd apps/angular`. Requiere .NET SDK + `node_modules` en Angular — ver notas Task 01.)

---

## Progress Tracking

- [x] Task 01: Setup paths / baseline (setup)
- [x] Task 02: Core FindByWhatsAppContactId tests (RED)
- [ ] Task 03: Core FindByWhatsAppContactId impl (GREEN+VERIFY)
- [ ] Task 04: Angular HITL resolution tests (RED)
- [ ] Task 05: Angular HITL resolution + proxy (GREEN+VERIFY)

---

## References

- **TRD**: `trd-whatsapp-hitl-register-payment.md`
- **Test Spec**: `test-spec-whatsapp-hitl-register-payment.md`
- **Design**: `design-whatsapp-hitl-register-payment.md`
- **Coding Agents**: `/agents/coding/`
- **QA Handoff**: Laura (TRD §7)
- **DevOps Handoff**: Sofía (N/A infra)

---

## Next Step

Arrastra al chat la primera tarea:  
`@tasks/task-whatsapp-hitl-register-payment/task01-setup-paths-baseline.md`
