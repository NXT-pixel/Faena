---
phase: red
agent: jest-tester
agent_path: /agents/coding/jest-tester.md
---

# Task 04: Angular HITL resolution - Tests

**Phase:** RED (Write Tests)  
**Module:** `hitl-register-payment.util` + `ConversationDetailComponent.registerPayment`  
**Dependencies:** Task 01  
**Location:** `Proyecto/growthhacking.PrototypeZero/apps/angular/`

---

## Overview

Escribir specs Jasmine que fallen definiendo helpers de teléfono/match/payable y el comportamiento de `registerPayment`: path teléfono, fallback `findByWhatsAppContactId`, toasts `NoMatchingCustomer` / `NoPayableOrder`, picker multi-pedido y guard de loading.

---

## Module Responsibility

**Files (a implementar en GREEN)**:
- `apps/angular/src/app/whatsapp/conversations/hitl-register-payment.util.ts`
- `apps/angular/src/app/whatsapp/conversations/conversation-detail/conversation-detail.component.ts`

**Purpose**: Helpers puros + orquestación HITL de resolución de cliente y apertura de pago.

**Key Functions**:
- `toPhoneDigits`, `hasUsablePhoneDigits`, `phonesMatch`, `matchCustomerByPhone`, `isPayableOrderStatus`
- `registerPayment(): void` — teléfono → contactId → getDetail → modal/picker/toasts

---

## Test Specification

Fuente: `test-spec-whatsapp-hitl-register-payment.md` → suites `hitl-register-payment.util` y `ConversationDetailComponent registerPayment`

---

## Testing Conventions

El repo Angular usa **Jasmine + Karma** (no Jest). Seguir:

1. Patrón de `apps/angular/src/app/whatsapp/conversations/whatsapp-contact-label.util.spec.ts` para utils.
2. Si no hay spec de componente cercano, preferir tests del util al 100% y tests de orquestación con TestBed/mocks mínimos de `CatalogCustomerService` / toaster — o extraer lógica pura adicional testeable sin TestBed si el componente es pesado.
3. Usar `describe` / `it` / `expect` Jasmine.

Do not invent a different runner.

```typescript
describe('hitl-register-payment.util', () => {
  describe('toPhoneDigits', () => {
    it('strips non digits', () => {
      // agent fills in
    });
  });
});
```

---

### Test Suite: `hitl-register-payment.util`

#### Test: toPhoneDigits_strips_non_digits
- **Given:** `'+57 300-111-2233'`
- **When:** `toPhoneDigits(...)`
- **Then:** `'573001112233'`

#### Test: toPhoneDigits_empty_for_null_or_blank
- **Given:** `null` / `''` / `'+'`
- **When:** `toPhoneDigits(...)`
- **Then:** `''`

#### Test: hasUsablePhoneDigits_true_when_length_gte_7
- **Given:** `'3001112233'`
- **When:** `hasUsablePhoneDigits(digits)`
- **Then:** `true`

#### Test: hasUsablePhoneDigits_false_when_too_short
- **Given:** `'123456'`
- **When:** `hasUsablePhoneDigits(digits)`
- **Then:** `false`

#### Test: phonesMatch_compares_trailing_up_to_10_digits
- **Given:** stored `'+573001112233'`, input `3001112233`
- **When:** `phonesMatch(...)`
- **Then:** `true`

#### Test: phonesMatch_false_when_either_side_too_short
- **Given:** stored o input demasiado corto
- **When:** `phonesMatch(...)`
- **Then:** `false`

#### Test: matchCustomerByPhone_prefers_same_WhatsAppContactId_among_phone_matches
- **Given:** Dos phone matches; uno con contactId G1
- **When:** `matchCustomerByPhone(list, G1, phoneDigits)`
- **Then:** El de G1

#### Test: matchCustomerByPhone_returns_single_phone_match_without_contact_id
- **Given:** Un solo phone match
- **When:** match
- **Then:** Ese candidato

#### Test: matchCustomerByPhone_returns_null_when_ambiguous_without_contact_match
- **Given:** Dos phone matches sin contactId pedido
- **When:** match
- **Then:** `null`

#### Test: isPayableOrderStatus_true_for_PendingPayment_OnCredit_PaymentReminder
- **Given:** Cada enum pagable
- **When:** `isPayableOrderStatus`
- **Then:** `true`

#### Test: isPayableOrderStatus_false_for_Paid_Draft_Shipped
- **Given:** Estados no pagables
- **When:** `isPayableOrderStatus`
- **Then:** `false`

**Test File**: `apps/angular/src/app/whatsapp/conversations/hitl-register-payment.util.spec.ts`

---

### Test Suite: `ConversationDetailComponent registerPayment`

#### Test: With_usable_phone_and_one_payable_order_opens_payment_modal
- **Given:** Teléfono usable; getList match; getDetail un `PendingPayment`
- **When:** `registerPayment()`
- **Then:** `paymentModal.open(...)`; sin toast NoMatchingCustomer

#### Test: Without_usable_phone_uses_FindByWhatsAppContactId_and_opens_modal
- **Given:** Sin teléfono usable; contactId G1; find OK + pagable
- **When:** `registerPayment()`
- **Then:** `findByWhatsAppContactId(G1)`; modal abierto

#### Test: Phone_path_miss_falls_back_to_contact_id
- **Given:** Teléfono usable sin match; contactId find OK + pagable
- **When:** `registerPayment()`
- **Then:** Fallback find; modal abierto

#### Test: Shows_NoMatchingCustomer_when_no_phone_and_no_contact_id
- **Given:** Sin teléfono ni contactId
- **When:** `registerPayment()`
- **Then:** Toast NoMatchingCustomer; sin getDetail/modal

#### Test: Shows_NoMatchingCustomer_when_contact_id_find_returns_null
- **Given:** Find → null
- **When:** `registerPayment()`
- **Then:** Toast NoMatchingCustomer

#### Test: Shows_NoPayableOrder_when_customer_has_no_payable_orders
- **Given:** Cliente OK; orders solo Paid/Draft
- **When:** `registerPayment()`
- **Then:** Toast NoPayableOrder

#### Test: Opens_order_picker_when_multiple_payable_orders
- **Given:** 2+ pagables
- **When:** `registerPayment()`
- **Then:** Order picker abierto; modal aún no

#### Test: Does_not_start_second_request_while_isLoadingPayableOrders
- **Given:** `isLoadingPayableOrders === true`
- **When:** `registerPayment()`
- **Then:** Sin nuevas llamadas a customerService

**Test File**: Prefer `conversation-detail.component.spec.ts` junto al componente, o specs de un facade/helper de resolución si TestBed del componente resulta inviable — documentar la elección; cubrir todos los GWT anteriores.

---

## Test Data & Fixtures

- `conversation-no-phone`, `conversation-with-phone` (test-spec)
- `customer-with-pending-payment`, `customer-multi-payable`
- Mocks: `CatalogCustomerService` (`getList`, `getDetail`, `findByWhatsAppContactId`), `ToasterService`, `LocalizationService`

---

## File Operations

**Files Created**:
- `apps/angular/src/app/whatsapp/conversations/hitl-register-payment.util.spec.ts`
- Specs de orquestación `registerPayment` (path según patrón del repo; p. ej. `conversation-detail.component.spec.ts`)

**Files Modified**:
- None (stubs mínimos del util solo si el compilador de specs lo exige para importar símbolos — preferir fallar por módulo ausente)

**Files Deleted**:
- None

---

## Success Criteria

- [ ] All util + registerPayment GWT covered
- [ ] Specs run and FAIL (RED)
- [ ] No production implementation (util/component/proxy/localization)

---

## Notes

**For Coding Agent**: Tests define the contract. Fail first. Angular runner is Jasmine/Karma despite agent name `jest-tester`.

**TRD Reference**: `trd-whatsapp-hitl-register-payment.md`

**Verify RED** (ajustar al script real de Task 01):

```bash
cd apps/angular
yarn test --watch=false
# o filtro equivalente a hitl-register-payment / conversation-detail
```
