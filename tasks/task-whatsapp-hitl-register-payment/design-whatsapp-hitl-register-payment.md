# Requerimientos y Diseño: Registrar pago HITL desde Chats WhatsApp (match de cliente)

**Fecha:** 2026-11-12  
**Ticket Origen:** Bug — «Ningún cliente de la tienda coincide con este número» al usar **Registrar pago** en la alerta de revisión humana (Chats WhatsApp); el mismo pago sí se completa desde **Inicio**  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero`

---

## 1. Resumen Ejecutivo y Objetivos

Cuando una conversación WhatsApp escala a revisión humana por comprobante de pago (HITL), el operador usa el botón **Registrar pago** en la alerta. Hoy el flujo falla con `WhatsAppService::HITL:NoMatchingCustomer` («Ningún cliente de la tienda coincide con este número») y no abre el modal de pago.

En el caso reportado (Capilarte / PrototypeZero), el encabezado de la conversación muestra **Teléfono no disponible** (`Conversation:PhoneUnavailable`) y el estado del agente está **Pausado**. El registro del mismo pago desde el módulo **Inicio** (dashboard de tienda) sí funciona, porque allí se abre el modal con el **pedido** ya identificado, sin resolver cliente por teléfono.

**Objetivo de negocio:** Permitir registrar el comprobante/pago pendiente **sin salir de la conversación**, resolviendo de forma fiable al cliente (y sus pedidos pagables) asociados al chat activo, con el mismo resultado operativo que el flujo de Inicio.

**Hipótesis técnica (a confirmar en TRD):**

1. `conversation-detail.component.ts` → `registerPayment()` exige `detail.phoneNumber` con ≥7 dígitos; si no, muestra `HITL:NoMatchingCustomer` y aborta (coincide con UI «Teléfono no disponible»).
2. La búsqueda de cliente usa `CatalogCustomerService.getList({ filter: últimos 10 dígitos })` y `matchCustomer` solo desambigua por `whatsAppContactId` **entre matches por teléfono**; sin teléfono usable no hay match, aunque exista `WhatsAppContactId` en conversación y en `CatalogCustomer`.
3. El listado de clientes (`CatalogCustomerAppService.GetListAsync`) filtra por `FullName` / `WhatsappPhone` / `Email`, **no** por `WhatsAppContactId`.
4. Inicio (`store-dashboard.registerPaymentFor`) llama `paymentModal.open(orderId, …)` directamente sobre pedidos pendientes; no depende del teléfono del chat.

**Relación con ticket previo:** `task-manual-payment-agent-status` cubre consistencia de estado agente/portal **después** de `RegisterManualPayment`. Este ticket cubre el **acceso** al registro desde HITL en Chats WhatsApp.

---

## 2. Personas y Actores

- **Usuario Final / Rol**: Tenant Admin / operador de tienda que atiende HITL en **Chats WhatsApp** y registra pagos manuales (también desde **Inicio**).
- **Equipo Interno**:
  - Tech Lead: David / Santiago
  - QA Asignado: Laura
  - DevOps: Sofía

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

- **Escenario 1**: Registrar pago desde HITL con teléfono disponible y cliente vinculado
  - **Dado** una conversación con alerta HITL de comprobante, teléfono usable en el detalle y un cliente de tienda con pedido pagable (`PendingPayment` / `OnCredit` / `PaymentReminder`)
  - **Cuando** el operador hace clic en **Registrar pago**
  - **Entonces** se abre el flujo de registro (modal o selector de pedido si hay varios) sin el toast `HITL:NoMatchingCustomer`

- **Escenario 2**: Registrar pago desde HITL con teléfono no disponible / oculto
  - **Dado** una conversación HITL cuyo encabezado muestra «Teléfono no disponible» (o `IsPhoneNumberHidden`), pero con `WhatsAppContactId` y un `CatalogCustomer` vinculado por ese contact id (y/o pedido pagable del mismo cliente)
  - **Cuando** el operador hace clic en **Registrar pago**
  - **Entonces** el sistema identifica al cliente/pedidos pagables y permite registrar el pago, sin exigir número de teléfono en el chat

- **Escenario 3**: Paridad con Inicio
  - **Dado** un pedido pendiente que se puede registrar desde **Inicio**
  - **Cuando** el operador registra el pago desde la alerta HITL de la conversación asociada
  - **Entonces** el pago se completa con el mismo resultado de negocio (pedido/pago actualizados) que desde Inicio

- **Escenario 4**: Sin cliente ni pedido pagable (control negativo)
  - **Dado** una conversación HITL sin cliente de tienda resoluble y/o sin pedidos en estado pagable
  - **Cuando** el operador hace clic en **Registrar pago**
  - **Entonces** se muestra un mensaje claro (`NoMatchingCustomer` o `NoPayableOrder` según el caso) y no se abre un modal vacío

- **Escenario 5**: Varios pedidos pagables
  - **Dado** un cliente resuelto con más de un pedido pagable
  - **Cuando** el operador inicia **Registrar pago** desde HITL
  - **Entonces** se muestra el selector de pedidos y, al elegir uno, se abre el modal de pago

---

## 4. Alcance Técnico

- **En Alcance (In Scope)**:
  - Corregir la resolución de cliente/pedidos pagables desde `apps/angular/.../conversation-detail` al pulsar **Registrar pago** (HITL).
  - Usar identidad durable de WhatsApp (`WhatsAppContactId` / identificadores del contacto) cuando el teléfono falte, esté oculto o no alcance el umbral de dígitos — alineado con el modelo ya existente (`CatalogCustomer.WhatsAppContactId`, `WhatsAppCustomerResolver` en Core).
  - Extender API/consulta de clientes o pedidos en Core **solo si** el front no puede resolver de forma segura con endpoints actuales (p. ej. filtro/lookup por `WhatsAppContactId`, o listado de pedidos pagables por contact id).
  - Tests (TDD) del matching / resolución (unit Angular y/o unit/integration Core según el corte del TRD).
  - Mensajería de error coherente: distinguir «sin teléfono y sin vínculo por contact id» vs «cliente OK pero sin pedido pagable».

- **Fuera de Alcance (Out of Scope)**:
  - OCR / visión del comprobante enviado por el cliente.
  - Cambios al flujo Wompi o a la persistencia post-`RegisterManualPayment` (cubierto por `task-manual-payment-agent-status`).
  - Rediseño del dashboard **Inicio** más allá de usarlo como referencia de paridad.
  - Nuevos secretos, colas o infraestructura Azure (no se anticipan; confirmar en TRD).
  - Resolver todas las conversaciones históricas sin `WhatsAppContactId` (solo documentar limitación si aparece).

### Componentes clave (mapa preliminar)

| Área | Ubicación |
| :--- | :--- |
| Botón HITL + lookup actual | `apps/angular/.../conversation-detail/conversation-detail.component.ts` → `registerPayment()` / `matchCustomer()` |
| UI alerta HITL | `conversation-detail.component.html` |
| Teléfono / label | `whatsapp-contact-label.util.ts` (`PhoneUnavailable`, `IsPhoneNumberHidden`) |
| DTO conversación | `WhatsAppConversationDetailDto` (`PhoneNumber`, `WhatsAppContactId`, `IsPhoneNumberHidden`) |
| Listado clientes | `CatalogCustomerAppService.GetListAsync` (filtro actual sin contact id) |
| Vínculo cliente↔WhatsApp (backend) | `CatalogCustomer.WhatsAppContactId`, `WhatsAppCustomerResolver`, `WhatsAppCustomerContactLinker` |
| Paridad Inicio | `apps/angular/.../dashboard/store/store-dashboard.component.ts` → `registerPaymentFor` + `PaymentModalComponent` |
| Localización error | `Localizations/WhatsAppService/es.json` → `HITL:NoMatchingCustomer` |

### Skills a aplicar en fases posteriores

- Angular / ABP UI (front HITL)
- ABP / .NET CoreService (si hace falta endpoint de lookup por `WhatsAppContactId`)
- Ver catálogo en `skills/README.md` + `rules/skills-routing.md` antes de implementar

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Reproducir en tenant tipo Capilarte: conversación HITL con «Teléfono no disponible» + botón **Registrar pago** → debe abrir modal/selector, no el toast de número.
  - Caso con teléfono visible y match por últimos dígitos (regresión del happy path actual).
  - Validar paridad: mismo pedido registrable desde Inicio y desde Chats WhatsApp.
  - Negativos: sin cliente vinculado; cliente sin pedidos pagables; varios pedidos pagables.
  - Confirmar permisos `Store.Payments.Create` y que tras registrar, la intervención HITL / agente se comporten según reglas vigentes (sin ampliar alcance de estado agente salvo regresión).

- **Handoff a DevOps (Sofía)**:
  - Sin cambios de infraestructura previstos. Si el TRD introduce setting/secreto nuevo, documentarlo aquí; de lo contrario N/A.

- **Alineación Tech Lead (David / Santiago)**:
  - Confirmar estrategia preferida: lookup por `WhatsAppContactId` en Core vs enriquecer DTO de intervención con `orderId`/`customerId` desde el agente HITL. Priorizar la opción mínima que restaure el flujo del operador.

---

## 6. Próximo Paso

Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:  
Arrastra al chat:

`@commands/2-create-trd.md tasks/task-whatsapp-hitl-register-payment/design-whatsapp-hitl-register-payment.md`
