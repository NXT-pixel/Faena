---
phase: green
agent: angular-developer
agent_path: /agents/coding/angular-developer.md
---

# Task 05: Angular HITL resolution + proxy - Implementation

**Phase:** GREEN (Implement Code)  
**Module:** `hitl-register-payment.util` + `ConversationDetailComponent` + proxy + localizations  
**Dependencies:** Task 03, Task 04  
**Location:** `Proyecto/growthhacking.PrototypeZero/`

---

## Overview

Implementar util HITL, reescribir `registerPayment()` (teléfono → fallback `findByWhatsAppContactId` → getDetail → modal/picker/toasts), añadir método al proxy `CatalogCustomerService`, y ajustar copy de `HITL:NoMatchingCustomer`. Hacer pasar specs de Task 04.

---

## Module Responsibility

**Files**:
- `apps/angular/src/app/whatsapp/conversations/hitl-register-payment.util.ts` (create)
- `apps/angular/src/app/whatsapp/conversations/conversation-detail/conversation-detail.component.ts` (modify)
- `apps/angular/src/app/proxy/core-service/store/customers/catalog-customer.service.ts` (modify)
- `Localizations/WhatsAppService/es.json`, `en.json` (modify)

**Purpose**: Resolver cliente desde HITL sin depender solo del teléfono; abrir el mismo flujo de pago que Inicio.

**Key Functions**:
- Util: `toPhoneDigits`, `hasUsablePhoneDigits`, `phonesMatch`, `matchCustomerByPhone`, `isPayableOrderStatus`
- `registerPayment(): void` — algoritmo TRD §2/§4
- Proxy: `findByWhatsAppContactId(whatsAppContactId: string, config?)`

---

## Test Reference

**Test Files** (from Task 04):
- `hitl-register-payment.util.spec.ts`
- Specs de `registerPayment` / orquestación

Read Task 04 tests; all must pass after implementation. Task 03 Core API must exist for the real HTTP path (proxy URL alineada al AppService).

---

## Architecture Patterns

- Extraer helpers puros (patrón `whatsapp-contact-label.util`).
- Orquestación en el componente; sin lógica de negocio en templates.
- Proxy ABP `RestService` alineado a la ruta de Task 03 (`generate-proxy` o edición manual coherente con `catalog-customer.service.ts`).
- Algoritmo: (1) teléfono usable → getList + match; (2) sin match + contactId → findByWhatsAppContactId; (3) sin cliente → NoMatchingCustomer; (4) getDetail → pagables → modal / picker / NoPayableOrder.

Skills: `abp-angular`, `angular-developer`.

---

## Coding Conventions

Follow `rules/project/company-standards.md` and domain skills. No inventar estilos; mirror surrounding WhatsApp Angular code (signals, inject, toaster keys `WhatsAppService::HITL:*`).

---

## Dependencies

**Uses**:
- `CatalogCustomerService` (getList, getDetail, findByWhatsAppContactId)
- `ToasterService`, `LocalizationService`
- `PaymentModalComponent`
- Enums `CatalogOrderStatus`

---

## File Operations

**Files Created**:
- `apps/angular/src/app/whatsapp/conversations/hitl-register-payment.util.ts`

**Files Modified**:
- `apps/angular/src/app/whatsapp/conversations/conversation-detail/conversation-detail.component.ts`
- `apps/angular/src/app/proxy/core-service/store/customers/catalog-customer.service.ts`
- `Localizations/WhatsAppService/es.json`
- `Localizations/WhatsAppService/en.json`

**Files Deleted**:
- None

---

## Test Issue Handling

If you encounter issues with the tests from Task 04, **pause and report** rather than silently fixing tests. Categories: logic inconsistencies, schema/type mismatches, architectural violations, missing coverage, mock inconsistencies, impossible expectations, validation conflicts, integration mismatches, brittle setup, ambiguous requirements.

**You may fix without asking**: Typos, imports, test helper usage, formatting.

---

## Implementation Checklist

- [ ] Create `hitl-register-payment.util.ts`
- [ ] Refactor `registerPayment` to use util + contactId fallback
- [ ] Add `findByWhatsAppContactId` to proxy (URL matches Core)
- [ ] Update `HITL:NoMatchingCustomer` ES/EN (contacto, no solo número)
- [ ] All Task 04 tests pass
- [ ] No test modifications without approval

---

## VERIFY: Quality Gates

### verify:quick

```bash
# Desde Proyecto/growthhacking.PrototypeZero/apps/angular
yarn test --watch=false
# filtrar a hitl-register-payment / conversation-detail según script real (Task 01)
```

**Expected**: Specs HITL green

### verify:full

```bash
# Core regression of Task 03
dotnet build services/core/PrototypeZero.CoreService
dotnet test services/core/PrototypeZero.CoreService.Tests --filter "FullyQualifiedName~CatalogCustomerFindByWhatsAppContact"

# Angular
cd apps/angular && yarn test --watch=false
```

**Expected**: Core + Angular HITL suites green

### Coverage Requirements

- Paths: phone OK, no-phone+contactId, no match, no payable, N payable — covered
- Error handling: empty contact / null find — covered

### Verification Checklist

- [ ] Task 04 tests pass
- [ ] `verify:quick` passes
- [ ] `verify:full` passes
- [ ] Proxy method present and aligned with Core
- [ ] Localization updated ES + EN

---

## Notes

**For Coding Agent**: Minimal change to restore HITL parity with Inicio. Do not redesign dashboard or HITL DTO.

**TRD Reference**: `trd-whatsapp-hitl-register-payment.md`
