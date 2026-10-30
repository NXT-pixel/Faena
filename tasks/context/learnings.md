---
created: 2026-10-24T23:32:00Z
last_updated: 2026-10-29T21:05:00Z
version: 1.10
author: Faena Context System
---

# 🧠 Lecciones Aprendidas y Memoria Continua (Faena)

Este archivo almacena la memoria persistente de la factoría. Cada vez que se resuelva un ticket o se ejecute el Paso 5 (Review & Handoff), el asistente de IA registrará aquí convenciones, trucos, puertos, peculiaridades y errores resueltos en los repositorios de `Proyecto/`.

---

## 📌 Convenciones y Patrones de la Empresa
*Registra aquí decisiones acordadas con el Tech Lead o convenciones de código.*

- **Arquitectura de Repositorios**: Todo el código de producción vive en `Proyecto/<nombre-del-repo>/`.
- **Estrategia de Testing**: Todo desarrollo sigue TDD estricto (RED -> GREEN -> VERIFY).
- **Identidad Git Corporativa**: Configurar siempre `user.name "Santiago"` y `user.email "Santiago.guerrero@pevaar.com"` en el git local de `Proyecto/growthhacking.PrototypeZero`.

---

## 🛠️ Trucos de Entorno y Configuración
*Puertos locales, variables de entorno clave, peculiaridades de Docker o dependencias.*

- **Gestión de Secretos en `growthhacking.PrototypeZero`**:
  - Los archivos `appsettings.secrets.json` contienen la licencia comercial de ABP y la conexión a Azure ServiceBus (`Azure:ServiceBus:Connections:Default:ConnectionString`).
  - El certificado `openiddict.pfx` es indispensable para `apps/auth-server/PrototypeZero.AuthServer` y está en `.gitignore`.
  - Carpeta de respaldo de secretos: `C:\Users\santi\Downloads\PrototypeZero-Secrets\PrototypeZero-Secrets`.
  - Script automatizado de restauración disponible en: `scripts/restore-secrets.ps1`.
  - Para evitar que Git marque los `appsettings.secrets.json` como modificados o los sobreescriba en pulls/checkouts, usar: `git update-index --skip-worktree <archivo>`.

- **Azure Blob Storage (`Azure:BlobStorage:Connection`)**:
  - Requiere un connection string válido de Azure Storage (actual de desarrollo: storage account `ghstoragedev02`).
  - **Servicios que lo requieren obligatoriamente y su propósito**:
    1. **`PrototypeZero.CoreService`**:
       - *Propósito*: Almacena los archivos de catálogo (PDFs) subidos por los administradores y las imágenes asociadas a productos dentro del contenedor `store-catalog` (`StoreCatalogBlobService`). Gestiona la reserva y confirmación de cuotas de almacenamiento de catálogos (`ICatalogStorageQuotaIntegrationService`).
    2. **`PrototypeZero.AiService`**:
       - *Propósito*: En el pipeline de procesamiento inteligente de catálogos (`CatalogDocumentBlobReader`), descarga el PDF desde `store-catalog`, procesa páginas y fragmentos para OpenAI, y sube de vuelta al contenedor `store-catalog` las imágenes detectadas y recortadas de los productos.
    3. **`PrototypeZero.FileManagementService`**:
       - *Propósito*: Motor central de blobs del sistema (`AzureBlobIntegrationService`, `StandardStorageShareUrlService`). Administra el contenedor general `prototypezero-dev`, sincroniza metadatos de archivos subidos y valida la existencia de blobs multimedia para generar URLs públicas temporales de descarga consumidas por WhatsApp/Meta.
    4. **`PrototypeZero.SaasService`**:
       - *Propósito*: Gestión de personalización visual por tenant (`TenantBranding`). Almacena y sirve los logos corporativos (modo claro/oscuro) y los íconos de cada tenant en el contenedor `tenant-branding`.
  - **Estrategia de Fallback para Branding de Tenant**:
    - Si `brandingUrl` no está configurado o si el blob en Azure aún no ha sido subido (404), tanto el front-office (`BrandingProvider`) como el modal de inquilinos (`TenantBrandingComponent`) y el catálogo público (`storefront-catalog`) realizan fallback automático a los logos genéricos (`defaultBranding` / iconos estándar) sin romper el diseño de la interfaz ni mostrar imágenes rotas.
    - Tan pronto como se detecta y resuelve exitosamente la imagen en Azure (`200 OK`), la interfaz reemplaza dinámicamente el logo por el del inquilino.

- **Puertos locales relevantes**:
  - WebGateway (YARP): `http://localhost:44368` — expone `/api/360dialog/{**}` → WhatsAppService y `/api/file-management/{**}` → FileManagementService.
  - WhatsAppService: `http://localhost:44364`.
  - FileManagementService: `http://localhost:44346`.
  - AuthServer: `http://localhost:44333`. Angular: `http://localhost:4200`.

- **Túnel local y DevTunnels (Regla de Exposición Pública)**:
  - **DevTunnels**: Al exponer `44368` (WebGateway) con VS Code DevTunnels (`https://<id>-44368.use2.devtunnels.ms`), es **estrictamente obligatorio** configurar la visibilidad como **`Public` (Anonymous)**.
  - Si la visibilidad está en `Private`, DevTunnels responde con `HTTP 302 Found` solicitando inicio de sesión con GitHub, bloqueando totalmente los webhooks entrantes de 360Dialog y las descargas de adjuntos de Meta.

- **Envío de Adjuntos / Multimedia en WhatsApp (Meta / 360Dialog / FileManagement)**:
  - Al enviar imágenes, audios o documentos por WhatsApp (ej. fotos de productos del catálogo o respuestas del chatbot), Meta no recibe los bytes directamente: Meta hace un `HTTP GET` a la URL pública generada por el backend.
  - La URL generada tiene el formato:
    `{Storage:PublicShareBaseUrl}/api/file-management/standard-storage/share/{token}`.
  - **Configuración obligatoria**: En `services/file-management/PrototypeZero.FileManagementService/appsettings.json`, la clave `Storage:PublicShareBaseUrl` **DEBE** actualizarse con el mismo DevTunnel público del WebGateway (ej. `https://<id>-44368.use2.devtunnels.ms`).
  - **Importante**: Tras actualizar `Storage:PublicShareBaseUrl`, se debe **reiniciar `PrototypeZero.FileManagementService`** para que recargue el valor en memoria.
  - Si esta clave apunta a una URL caducada o localhost, Meta no puede descargar los archivos y el mensaje con adjuntos falla silenciosamente sin entregarse al usuario.

- **Webhooks 360dialog (mensajes entrantes)**:
  - Endpoint: `POST /api/360dialog/events` (`D360Controller.OnEventAsync`).
  - Config base en `services/whatsapp/.../appsettings.json` → `360Dialog:WebhookUrl` y `HostWebhookUrl` (solo base HTTPS, sin path; el código añade `/api/360dialog/events`).
  - `HeaderSecret` debe coincidir con el header `Secret` que 360dialog reenvía.
  - Al **Guardar** la Clave API en Angular (`Configuración → Whatsapp`), `D360SettingsService.SetApiKeyForCurrentTenantAsync` llama `SetWebhookUrl` y registra en 360dialog la URL + headers `Secret` y `TenantId` (GUID del tenant actual).
  - **Obligatorio**: guardar la API key como admin del **tenant hijo** (no host). Si `TenantId` queda vacío, el webhook siempre responde 400.
  - Tras cambiar `WebhookUrl` en appsettings: **reiniciar WhatsAppService** y **volver a Guardar** la API key para re-registrar en 360dialog.
  - Local Development: MassTransit usa **Azure Service Bus** (`UsingAzureServiceBus`), no RabbitMQ del docker compose. Cola: `save-whatsapp-messages-dev{HOSTNAME}`.
  - `ApplicationUrl`: sandbox `https://waba-sandbox.360dialog.io` vs prod `https://waba-v2.360dialog.io`.

---

## 🐞 Errores Comunes Resueltos y Soluciones
*Gotchas y problemas típicos encontrados durante la compilación o tests.*

- **Fallo al enviar adjuntos o imágenes en respuestas de WhatsApp**:
  - Causa: `Storage:PublicShareBaseUrl` en `FileManagementService` apuntaba a una URL obsoleta o inaccesible por Meta.
  - Solución: Actualizar `Storage:PublicShareBaseUrl` en `services/file-management/PrototypeZero.FileManagementService/appsettings.json` con la URL del DevTunnel público y reiniciar el servicio.

- **Mensajes de WhatsApp no llegan / DevTunnel responde 302**:
  - Causa: El túnel de VS Code / devtunnel estaba en modo Privado (`Private`).
  - Solución: En la pestaña *Ports* de VS Code, clic derecho en `44368` → *Port Visibility* → *Public*.

- **Error de compilación TypeScript en Angular (`Cannot find module ../../../../environments/environment`)**:
  - Causa: En `storefront-catalog.component.ts` (ubicado en `src/app/public/storefront/`), se usaban 4 niveles relativos en vez de 3.
  - Solución: Cambiar a `import { environment } from '../../../environments/environment';` (comiteado en `f3da469`).

- **AuthServer falla al arrancar con Error 4060 (Cannot open database PrototypeZero_Administration)**:
  - Causa: Race condition al arrancar los microservicios. AuthServer necesita que `AdministrationService`, `IdentityService` y `SaasService` arranquen primero para auto-migrar sus bases de datos en SQL Server.

- **Webhook 360dialog llega pero responde 400**:
  - Se inyectó `ILogger<D360Controller>` en `D360Controller.cs` para auditar en los logs la causa exacta (mismatch de `Secret`, falta de header `TenantId`, tenant inactivo o payload no semánticamente válido).

- **Prevención de Categorías Duplicadas por Normalización Canónica (Bug 79082)**:
  - **Causa raíz**: El motor de categorías comparaba igualdad ordinal simple sin colapso de espacios ni descarte de diacríticos, permitiendo que variaciones como `"Anillos"` y `"  anÍllos  "` se persistieran como registros duplicados en el mismo tenant, tanto en CRUD manual como al publicar borradores con IA.
  - **Solución integral**:
    1. **`CatalogCategoryNormalizer`**: Utiliza descomposición Unicode (`NormalizationForm.FormD`) descartando marcas de acento (`NonSpacingMark`), convirtiendo a minúsculas (`ToLowerInvariant`) y colapsando espacios repetidos mediante regex `\s+`. Es agnóstico al idioma y funciona idénticamente para inglés, español y otros alfabetos latinos.
    2. **`CatalogCategoryAppService` & `CatalogCategoryDuplicateValidator`**: Intercepta `CreateAsync` y `UpdateAsync` para validar que no exista una categoría equivalente en el tenant (`c.TenantId == tenantId`), excluyendo la propia entidad en actualización (`c.Id != expectedId`). Ante colisión lanza `UserFriendlyException(L["Category:AlreadyExists"])`.
    3. **`CatalogImportAppService` & `CatalogDraftCategoryResolver`**: Durante la publicación de borradores extraídos por IA, reutiliza automáticamente la categoría existente si el nombre sugerido coincide fonético-ortográficamente con una previa, evitando inserciones redundantes.
    4. **Localización**: Añadidas claves `"Category:AlreadyExists"` en español e inglés en `Localizations/CoreService/es.json` y `en.json`.

- **Estados contradictorios tras pago manual (Portal Pagado vs Agente “sin pago”)**:
  - **Causa raíz**: `GetCustomerActiveCommerceOrder` solo devolvía Draft/PendingPayment/OnCredit/PaymentReminder. Tras `RegisterManualPayment` el pedido queda `Paid` y la tool retornaba `null`; el modelo interpretaba “sin checkout activo” como “sin pago verificado” y pedía comprobante/dirección de nuevo, pese al mensaje WhatsApp de pago exitoso. La persistencia backend (`Paid` + `Payment.Approved`) ya era correcta.
  - **Solución**:
    1. **`CustomerCommerceSessionResolver`**: Precedencia checkout/crédito; fallback al último `Paid`/`Shipped` con `BuildPaidFulfillmentReminderHint` (no reiniciar checkout; usar `GetOrderDetails`).
    2. **`OrderTools.GetCustomerActiveCommerceOrder`**: Incluye Paid/Shipped en candidatos; historial MCP expone `IsPaid`.
    3. **Prompts AiService**: `StoreOrderStatusInstructions`, `StorePromptConstrains`, `CustomerFacingGuardrails` — null/checkout vacío ≠ unpaid; IsPaid → no proof/HITL.
    4. **`ManualCatalogOrderPayment`**: Helper testeable de la transición Paid/Approved usado por `RegisterManualPayment`.

- **Preservación de Precio Exacto en Importación de Catálogos con IA y Variantes (Bug 59.999 vs 60.000 COP)**:
  - **Causa raíz**: Al procesar documentos o imágenes con IA/OCR, textos en viñetas o burbujas pueden ser extraídos con discrepancias menores (ej. OCR leyendo `59999` en vez de `60000`) y almacenados dentro de `draft.VariantsJson`. Si el operador corrige o aprueba el precio del borrador en la cabecera (`PriceAmount = 60000`), pero las variantes hijas retienen el JSON stale desalineado, `TryExpandVariants` al publicar creaba los productos usando el `PriceAmount` de la variante (`59999`), desestimando el precio revisado y aprobado por el usuario.
  - **Solución integral**:
    1. **Backend (`CatalogDraftVariantResolver`)**:
       - `SyncVariantPrices(draft, approvedPrice)`: Sincroniza `VariantsJson` con el precio aprobado en `UpdateDraftAsync`, `MarkDraftReviewedAsync` y `PublishDraftAsync`. Si las variantes comparten el precio base o carecen de precio individual, adoptan el valor aprobado.
       - `ExpandVariants(draft)`: Valida que las variantes tomen como valor efectivo el precio aprobado del borrador, impidiendo que variantes con precios desactualizados generen productos con discrepancias.
    2. **Frontend Angular (`create-update-catalog-draft`)**:
       - Escucha el evento `(change)` en `priceAmount` para actualizar en tiempo real los controles de variantes en el formulario.
       - Al guardar (`buildUpdateDto()`) se ejecuta `syncVariantPrices()` para garantizar consistencia antes de enviar el payload HTTP.
       - Nuevas variantes añadidas toman por defecto el precio principal actual del borrador.
    3. **Precisión Numérica**: En todo el flujo de catálogo se debe preservar el tipo `decimal` (C#) con serialización JSON precisa y sin redondeos implícitos que alteren los valores aprobados por el operador.

- **Refactorización de Colores Hardcoded en Modales del Storefront** (2026-10-29):
  - **Problema**: El SCSS de `storefront-catalog.component.scss` tenía ~24 colores hexadecimales hardcoded en las clases `.detail-modal-*` y `.modal-*`.
  - **Solución (Task Modal Theme Fix)**:
    1. **Tarea 01 SETUP**: Identificados 24 colores hardcoded y registrados.
    2. **Tarea 02 RED**: Se crearon ~22 nuevas variables CSS específicas para modales en la sección root del SCSS. Todos los 21 colores hardcoded reemplazados con variables CSS temáticas manteniendo el esquema "dark glassmorphism".
  - **Compatibilidad Dark Mode**: Las variables usan valores RGBA basados en tonos oscuros (azul marino, gris oscuro) para mantener legibilidad consistente.
  - **Nota para Light Mode**: El modal está diseñado para dark glassmorphism. Para light mode se necesitaría crear variantes separadas con backgrounds más claros y ajustes de contraste.

- **Banner del catálogo parpadea al abrir/cerrar modal de producto**:
  - **Causa raíz**: Tres rutas hermanas (`catalog`, `catalog/product/:id`, `catalog/:category`) cada una con `loadComponent` del mismo `StorefrontCatalogComponent`. Angular destruía y recreaba el componente en cada navegación del modal, recargando info/banner y saltando el scroll.
  - **Solución**: Un único `storefrontCatalogMatcher` en `app.routes.ts`; el `paramMap` ya no llama `loadProducts()` al abrir/cerrar producto; se restaura la categoría al cerrar; body scroll lock con compensación del scrollbar.
