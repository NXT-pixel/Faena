# Requerimientos y Diseño: Consistencia de estado tras pago manual (Portal ↔ Agente WhatsApp)

**Fecha:** 2026-10-28  
**Ticket Origen:** Bug — estados contradictorios de pago/pedido tras verificación manual (Tenant Admin vs Agente WhatsApp)  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero`

---

## 1. Resumen Ejecutivo y Objetivos

Tras un pedido con método de pago **manual**, el administrador verifica/aprueba el pago en Tenant Admin (`RegisterManualPayment`). El backend marca el pedido como **Pagado** (`CatalogOrderStatus.Paid`), crea el registro `Payment` con `PaymentStatus.Approved` y envía por WhatsApp la confirmación (ej. «Tu pedido #CAT-… fue pagado exitosamente»).

Minutos después, si el cliente pregunta por el envío («¿Cuándo lo envían?»), el **Agente WhatsApp** puede responder que **no hay pedido activo ni pago verificado**, volver a pedir dirección/comprobante y reiniciar el flujo de checkout — contradiciendo el mensaje de confirmación y el estado persistido.

**Objetivo de negocio:** Cuando el pago está verificado, el estado financiero y la respuesta del agente deben reflejar **Pagado**. El pedido puede seguir pendiente de preparación/entrega **sin comunicar deuda**. La conversación debe conservar el pedido y los datos de entrega, **sin reiniciar checkout**.

**Hipótesis técnica (a confirmar en TRD/implementación):**
1. `GetCustomerActiveCommerceOrder` solo retorna `Draft` / `PendingPayment` / `OnCredit` / `PaymentReminder` — **excluye** pedidos `Paid`. Tras la verificación manual, la tool de “pedido activo” devuelve vacío (o un checkout distinto), y el modelo interpreta “sin pedido activo” como “sin pago”.
2. Las instrucciones de orquestación (`StorePromptConstrains`) obligan a llamar `GetCustomerActiveCommerceOrder` en mensajes relacionados con pedidos; las de estado (`StoreOrderStatusInstructions`) exigen `GetOrderDetails` / `GetUserOrderHistory` en follow-ups. Si el modelo se apoya solo en la tool de activo + memoria conversacional («aguardando pago»), contradice el mensaje de confirmación ya entregado.
3. Tras enviar comprobante, `CustomerFacingGuardrails` / `RequestHumanIntervention` puede reforzar el relato de “pago no verificado” aunque el backend ya esté en `Paid`.

**Prerrequisito del ticket:** Confirmar en backend (Core) que, tras `RegisterManualPayment`, el pedido queda `Paid` y el `Payment` queda `Approved` **antes** de clasificar la regresión como solo de agente/prompt.

---

## 2. Personas y Actores

- **Usuario Final / Rol**: Cliente de tienda (Store) por WhatsApp; Tenant Admin que registra pago manual.
- **Equipo Interno**:
  - Tech Lead: David / Santiago
  - QA Asignado: Laura
  - DevOps: Sofía

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

- **Escenario 1**: Confirmación de pago manual persistida en backend
  - **Dado** un pedido en `PendingPayment` con gateway en modo verificación manual
  - **Cuando** el Tenant Admin registra y aprueba el pago manual (`RegisterManualPayment`)
  - **Entonces** `CatalogOrder.Status = Paid`, existe `Payment` con `PaymentStatus.Approved`, y el detalle del pedido en portal refleja pago verificado (no “pendiente”)

- **Escenario 2**: Agente refleja pago verificado al preguntar por envío
  - **Dado** el escenario 1 y el mensaje proactivo de WhatsApp «pedido pagado exitosamente»
  - **Cuando** el cliente pregunta por estado de envío / «¿cuándo lo envían?»
  - **Entonces** el agente responde con pedido **Pagado** (o equivalente), no solicita de nuevo comprobante ni dirección ya capturada, y distingue envío «por preparar» de deuda pendiente

- **Escenario 3**: Sin reinicio de checkout
  - **Dado** un pedido `Paid` con datos de entrega ya registrados
  - **Cuando** el cliente retoma la conversación sobre ese pedido
  - **Entonces** el agente no inicia un nuevo checkout ni pide de nuevo la información de pago/entrega ya proporcionada

- **Escenario 4**: Pago aún no verificado (control negativo)
  - **Dado** un pedido `PendingPayment` sin registro manual aprobado
  - **Cuando** el cliente pregunta por el pedido
  - **Entonces** el agente puede indicar espera de verificación / instrucciones de pago manual, sin afirmar «pagado»

- **Escenario 5**: Pedido pagado + nuevo draft concurrente (borde)
  - **Dado** un pedido `Paid` y, si aplica, un nuevo `Draft`/`PendingPayment` del mismo cliente
  - **Cuando** el cliente pregunta por el pedido recién pagado (por número o contexto reciente)
  - **Entonces** el agente no atribuye el estado del checkout nuevo al pedido pagado; usa `GetOrderDetails` / historial para el pedido referido

---

## 4. Alcance Técnico

- **En Alcance (In Scope)**:
  - Verificar persistencia post-`RegisterManualPayment` en Core (`CatalogOrderPaymentAppService`, proyección de detalle de pedido / portal).
  - Alinear tools MCP y/o prompts del agente Store para follow-ups de estado tras pago:
    - `OrderTools.GetCustomerActiveCommerceOrder`, `GetOrderDetails`, `GetUserOrderHistory`
    - `StoreOrderStatusInstructions`, `StorePromptConstrains` / `CommercialRulesetProvider` en AiService
    - Posible señal explícita en DTOs MCP (`IsPaid`, último pedido pagado reciente, o tool de “último pedido comercial”) para que el modelo no confunda «sin checkout activo» con «sin pago».
  - Evitar que, con pedido `Paid`, el agente vuelva a pedir comprobante o reinicie captura de dirección.
  - Tests unitarios/integración sobre proyección de estado y reglas de tools/prompts según TDD.

- **Fuera de Alcance (Out of Scope)**:
  - Cambios al flujo Wompi / webhooks (`StorePaymentHandler`) salvo impacto colateral documentado.
  - Rediseño del catálogo de métodos manuales Colombia (`ColombiaManualPaymentMethodStore`).
  - Visión OCR de comprobantes (hoy el agente no “ve” la imagen y escala a HITL).
  - Cambios de infraestructura Azure / nuevos secretos (salvo que el TRD descubra alguno).

### Componentes clave (mapa preliminar)

| Área | Ubicación |
| :--- | :--- |
| Registro pago manual | `services/core/.../Store/Payments/PaymentAppService.cs` → `RegisterManualPayment` |
| Notificación WhatsApp | `StorePaymentNotificationEto` + `StorePaymentNotificationHandler` |
| Tools pedido | `services/core/.../Store/Tools/OrderTools.cs` |
| Instrucciones estado | `services/ai/.../ChatBot/StoreOrderStatusInstructions.cs` |
| Orquestación tools | `services/ai/.../AiAppService.cs` (`StorePromptConstrains`) |
| UI admin | `apps/angular/.../catalog-payments/payment-modal.component.ts` |

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Reproducir con gateway `ManualVerification`: crear pedido → aprobar pago en Tenant Admin → consultar detalle → preguntar por WhatsApp «¿cuándo lo envían?» y contrastar respuesta vs estados en portal/DB.
  - Verificar que no se pide de nuevo comprobante/dirección tras pago verificado.
  - Caso borde: cliente con pedido pagado y otro draft abierto.
  - Control negativo: sin aprobación manual, el agente no dice «pagado».

- **Handoff a DevOps (Sofía)**:
  - Sin nuevos secretos previstos. Confirmar en entorno de prueba que Service Bus / outbox entrega `StorePaymentNotificationEto` (mensaje «pagado exitosamente») para no confundir fallo de notificación con bug de estado del agente.

- **Alineación Tech Lead (David / Santiago)**:
  - Decidir si la corrección es solo de prompts/orquestación o también ampliar el contrato MCP (p. ej. exponer último pedido `Paid` / tool de estado reciente) cuando `GetCustomerActiveCommerceOrder` retorna null.

---

## 6. Evidencia del bug (conversación observada)

1. **11:54** — Agente: «Tu pedido #CAT-… fue pagado exitosamente…»
2. **12:05** — Cliente: «¿Cuándo lo envían?»
3. **12:05–12:06** — Agente: no puede confirmar fecha porque «no tengo un pedido activo con envío validado»; luego «no me aparece un pedido activo ni un pago verificado» y pide comprobante.
4. **12:33** — Cliente reenvía comprobante; agente escala a revisión humana (no ve la imagen).

Esto encaja con pérdida de contexto operativo respecto al pedido ya `Paid`, no necesariamente con rollback del pago en base de datos.

---

## 7. Próximo Paso

Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:  
Arrastra al chat:  
`@commands/2-create-trd.md tasks/task-manual-payment-agent-status/design-manual-payment-agent-status.md`
