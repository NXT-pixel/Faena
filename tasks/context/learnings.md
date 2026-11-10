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

- **El panel del carrito no respetaba el modo claro/oscuro** (2026-10-30):
  - **Causa raíz**: `StorefrontCatalogComponent` gestiona el tema en `themeMode()` y lo expone en el host (`[attr.data-storefront-theme]`), pero el drawer del carrito quedó fuera de ese patrón: ~25 colores hardcodeados en modo oscuro dentro de `.cart-drawer` y su backdrop sin `[attr.data-storefront-theme]`, por lo que heredaba el scrim oscuro del modal (`rgba(6, 11, 24, 0.85)`).
  - **Regla del storefront para futuros elementos flotantes**: si el elemento debe cambiar de paleta en bloque (drawers/paneles), definir tokens propios en `:host` y `:host[data-storefront-theme='dark']` y consumirlos; ya hereda el atributo del host, no hace falta bindear por nodo. Si el elemento es un overlay que reutiliza `detail-modal-backdrop`, sí hay que añadirle `[attr.data-storefront-theme]="themeMode()"` porque su regla de modo claro es por atributo.
  - **Pitfall**: `.cart-close-btn` comparte `.modal-dismiss-btn`, cuyos tokens (`--sf-modal-dismiss-*`) son solo oscuros; al aclarar el panel hay que sobreescribir `background`/`color` con los tokens del contenedor.
  - **Verificación sin backend**: el SCSS del componente se puede compilar aislado con `sass` y renderizar el markup en una página estática (mapeando `:host` a una clase) para capturar los dos temas con Chrome headless; el build (`npm run build`) valida templates y estilos.

- **Visor Lightbox / Zoom de Imagen en Catálogo Storefront (2026-11-04)**:
  - **Requerimiento**: Permitir a los clientes inspeccionar las imágenes de productos en gran detalle desde el modal de detalle del catálogo público.
  - **Solución**:
    1. **Señal reactiva `isImageZoomOpen`**: Controla el ciclo de vida del visor sin remounting del componente ni pérdida de contexto en la navegación.
    2. **Jerarquía de Teclado**: `@HostListener('document:keydown.escape')` cierra prioritariamente el zoom si está abierto; solo si el zoom está cerrado delega el cierre al modal principal del producto (`closeProductDetail()`), evitando cierres accidentales.
    3. **Bloqueo de scroll**: `bodyScrollLockEffect` incorpora `isImageZoomOpen()` para impedir desplazamiento indeseado de fondo.
    4. **Soporte de Temas**: Estilizado con variables temáticas para `:host` y `[data-storefront-theme='light']`, manteniendo contraste y nitidez en modo claro y oscuro.
  - **Stacking Context y z-index de Overlays en Storefront**:
    - El modal de detalle del producto (`.detail-modal-backdrop`) usa `z-index: 99999`. Cualquier overlay, modal secundario o lightbox hijo/hermano (como `.image-zoom-backdrop`) DEBE tener un `z-index` superior (ej. `100005`) para evitar quedar oculto detrás del modal principal e inaccesible a la interacción del usuario.
  - **Mecánica Interactiva de Zoom (Mouse Wheel + Pan Dragging + Zoom-to-Cursor)**:
    - **Fórmula de anclaje al cursor**: Para que el zoom se efectúe exactamente sobre el punto donde apunta el cursor en vez del centro geométrico, se calcula el offset del mouse relativo al centro del viewport `(cx, cy)`. La nueva traslación tras variar de `scaleOld` a `scaleNew` sigue la relación:
      `nextPan = C - (C - panOld) * (scaleNew / scaleOld)`. De esta forma, el píxel de la imagen ubicado bajo el puntero no se desplaza durante la ampliación o reducción.
    - **Transición suave vs reactividad**: En el movimiento de rueda y zoom-to-cursor, una transición corta de `0.08s ease-out` elimina retrasos visuales y hace que la imagen siga fielmente al puntero. Al arrastrar (`isPanning`), la transición se desactiva (`none`) para lograr seguimiento 1:1 en tiempo real.
    - Para permitir un zoom profundo con la rueda del ratón (`(wheel)="onZoomWheel($event)"`), se debe capturar el evento en el contenedor del viewport y llamar `event.preventDefault()` y `event.stopPropagation()` para evitar que la rueda desplace la página detrás del lightbox.
    - El rango de escala se acota entre `1.0x` (ajuste exacto a pantalla) y `4.0x` (inspección de detalles al 400%).
    - Al estar en `scale > 1.0`, se habilita arrastre (`mousedown/mousemove/mouseup` y `touchstart/touchmove/touchend`) cambiando el cursor dinámicamente (`grab` / `grabbing`). La imagen debe llevar `draggable="false"` y `pointer-events: none` en la etiqueta `<img>` para impedir que el drag nativo del navegador interfiera con el arrastre del viewport.
    - Se añade acotamiento (`clampAndSetPan`) para evitar que la imagen se pierda fuera de los bordes visibles al arrastrarla en escalas altas.
  - **Configuración Karma en Angular 21 (`karma.conf.js`)**:
    - Con `@angular/build:karma` ya no se debe requerir `@angular-devkit/build-angular/plugins/karma` (provoca `MODULE_NOT_FOUND`). Se configuró `frameworks: ['jasmine']` y los plugins estándar de karma, habilitando pruebas headless con `ng test --watch=false --browsers=ChromeHeadless`.
  - **Optimización de Borrado de Blobs y Cuota de Almacenamiento en ABP / Azure**:
    - Evitar invocar servicios de cuota (`ICatalogStorageQuotaIntegrationService.RemoveUsedAsync`) dentro de bucles `foreach` cuando se borran múltiples archivos o imágenes de un catálogo. Al ser un cliente proxy HTTP cross-service, ejecutar 1 llamada por imagen para ~180 imágenes genera más de 700 llamadas remotas (existencia, propiedades, borrado y cuota), superando los 100 segundos y provocando Gateway Timeout 504.
  - **Patrón Responsive Móvil para Catálogos Storefront (Estilo Kyte - 2026-11-04)**:
    - **Problema de acumulación vertical**: En móviles, apilar la barra lateral de categorías, opciones de ordenamiento y datos de contacto antes de los productos fuerza al usuario a desplazarse más de dos pantallas antes de ver artículos.
    - **Solución arquitectónica**:
      1. **Header compacto con Menú Hamburguesa (`☰`)**: Traslada el bloque de contacto, redes sociales, alternador de tema y selector de idioma a un drawer lateral deslizable (`.mobile-drawer-backdrop`), liberando el flujo principal.
      2. **Carrusel horizontal de categorías (`.mobile-category-bar`)**: Despliega pestañas en mayúsculas (`TODO`, categorías) con `overflow-x: auto; scrollbar-width: none;` y subrayado activo, acompañadas de un botón de búsqueda rápida `🔍`.
      3. **Barra de acción compacta (`.mobile-action-bar`)**: Contiene un badge con la categoría activa y un botón `ORDENAR POR` que abre un selector inferior modal (`.sort-sheet-backdrop`) en lugar de botones dispersos.
      4. **Tarjetas de producto horizontales**: En `viewport <= 768px`, las tarjetas `.store-card` se estructuran en `flex-direction: row`: imagen cuadrada a la izquierda (`aspect-ratio: 1; min-width: 115px; border-radius: 14px;`) y a la derecha una columna con título en negrita (`line-clamp: 2`), subtítulo tenue en gris y precio destacado en color corporativo grande, replicando la experiencia de compra de catálogos modernos como Kyte.
      5. **Preservación Desktop**: La vista de escritorio (`> 768px`) conserva intacta la barra lateral y la cuadrícula multi-columna sin regresiones.
    - La consolidación usando `Parallel.ForEachAsync` con `MaxDegreeOfParallelism` controlado (10–12) y acumulación atómica (`Interlocked.Add`) permite borrar los blobs en paralelo y reducir las llamadas remotas de cuota a 1 sola invocación consolidada (`totalReleasedBytes`).
    - En tests de xUnit (.NET 10) con `Microsoft.NET.Test.Sdk 18.7.0`, la presencia de un ejecutable nativo `testhost.exe` puede fallar con `0xC0000142` en Windows; agregar un target MSBuild `RemoveTestHostExe` fuerza a VSTest a utilizar `dotnet exec testhost.dll`.
  - **Desbloqueo de Acciones de Lote en Grillas Angular**:
    - Si un elemento no cumple los criterios de una acción secundaria (ej. `canPublish`), el checkbox selector de la fila jamás debe tener `[disabled]`, ya que esto secuestra otras operaciones de lote válidas como el borrado (`DeleteSelected`).
    - La validación restrictiva debe residir exclusivamente en el botón específico de la acción (`[disabled]="... || !canPublishSelected()"`) mediante una señal `computed` reactiva.
  - **Storefront Móvil: Vistas Duales (Cuadrícula / Lista), Modo Claro por Defecto y Drawer de Contacto (2026-11-04)**:
    - **Incompatibilidad de la etiqueta `<header>` con ABP LeptonX en Móvil**: En el paquete de estilos de LeptonX (`layout-bundle.css`), existe una regla global activa en pantallas móviles que oculta etiquetas de cabecera: `.lpx-sidebar-container, header, .lpx-toolbar-container { display: none; }`. Debido a esto, cualquier barra con la etiqueta `<header class="storefront-navbar">` era ocultada inmediatamente en celulares. Se reemplazó por la etiqueta semántica `<nav class="storefront-navbar" aria-label="Navegación superior">` junto con `display: block !important;` y `.mobile-menu-btn { display: inline-flex !important; }`, garantizando la visualización permanente del botón hamburguesa `☰` y el logo en la parte superior.
    - **Alternador de Vista en Barra de Acciones**: Se implementó una pastilla de control segmentada a la derecha de "ORDENAR POR" (`.mobile-action-pill-group`). A la izquierda abre el menú inferior de ordenamiento y a la derecha conmuta instantáneamente entre la vista de cuadrícula (`instaview`, 2-3 columnas de tarjetas verticales con foto cuadrada superior) y la vista de lista (`list`, 1 columna horizontal compacta).
    - **Garantía de Modo Claro por Defecto**: La señal `themeMode` se inicializa y garantiza como `'light'` por defecto ante ausencia o reseteo de almacenamiento. El botón de cambio de tema (`.theme-toggle-btn`) se mantuvo accesible en el header móvil (`.navbar-actions`) y se añadió un selector visual de tema segmentado dentro del drawer lateral.
    - **Drawer de Contacto Integral**: Al pulsar el botón hamburguesa (`☰`), el panel lateral despliega la información completa de la tienda: acceso directo por WhatsApp, teléfono con enlace `tel:`, dirección física con búsqueda en Google Maps, horario de atención, redes sociales corporativas y selector de apariencia/idioma.
    - **Integración de Categorías y Filtros en el Menú Hamburguesa Móvil (2026-11-04)**:
      - Para ofrecer una experiencia de navegación omnicanal en pantallas táctiles, el drawer lateral desplegado por el botón hamburguesa (`☰`) ahora incluye:
        1. **Sección de Categorías**: Acceso a "Todas las categorías" con contador total y cada categoría con su respectivo badge numérico e ícono. Al seleccionar una categoría, se navega y filtra el catálogo cerrando automáticamente el drawer (`selectCategoryAndClose`).
        2. **Opciones de Filtrado / Ordenamiento**: Lista de criterios de ordenamiento (categoría, precio ascendente/descendente, nombre A-Z/Z-A) con indicador activo de checkmark (`selectSortAndCloseDrawer`).
        3. **Selector de Modo de Visualización**: Conmutador rápido entre cuadrícula (instaview) y lista (`setDisplayModeAndCloseDrawer`).
        4. **Información de Contacto y Redes**: Mantiene las tarjetas de teléfono, WhatsApp, ubicación Maps, horarios y redes sociales debajo de los filtros.
      - **Resiliencia en Rutas Base**: Al llamar `selectCategory` dentro de entornos de test o rutas iniciales donde `this.router.url` aún es undefined, la propiedad getter `baseRoute` ahora evalúa `(this.router.url || '').includes(...)`, previniendo `TypeError: Cannot read properties of undefined (reading 'includes')`.
    - **Formato del Mensaje Autogenerado de WhatsApp en Storefront (2026-11-05)**:
      - Los mensajes autogenerados hacia WhatsApp (`buildWhatsAppLink` y `buildCartWhatsAppLink`) prescinden del saludo inicial ("¡Hola!" / "Hi!") e inician directamente con el contenido de la solicitud ("Vi en su catálogo...", "Quiero pedir estos productos...").
      - Cada producto (tanto en consulta individual como en cada línea del pedido del carrito) incluye de forma obligatoria su URL directa resuelta mediante `buildProductUrl` (`https://.../product/{id}?tenant=...`), permitiendo al comerciante identificar inmediatamente el artículo exacto en su panel de administración.
      - La suite unitaria [`public-storefront.service.spec.ts`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/services/public-storefront.service.spec.ts) asegura contractualmente este comportamiento (`expect(text).not.toContain('Hola')` y `expect(text).toContain(url)`).
    - **Storefront `wa.me` debe respetar el transporte activo (OpenWa vs 360Dialog) (2026-11-05)**:
      - El catálogo publicaba `WhatsAppPhoneNumber` leyendo primero `360Dialog.PhoneNumber`. Tras migrar a OpenWa, un sandbox D360 residual (`5511…`) seguía ganando sobre `WhatsApp.OpenWa.PhoneNumber`.
      - `GetBusinessPhoneNumberAsync` debe preferir `OpenWa.PhoneNumber` cuando `OpenWA:Enabled=true`; el storefront debe preguntar primero al integration service de WhatsApp y solo luego caer a settings locales (`OpenWa` → `D360`).
    - **SEO Fase 1 del catálogo público (2026-11-05)**:
      - Producto: `Slug` / `MetaTitle` / `MetaDescription` (+ `Tags` existentes). Tienda: `SeoTitle` / `SeoDescription` en el blob de branding (mismo patrón que contacto).
      - Cliente: `StorefrontSeoService` actualiza `Title`/`Meta`/OG/Twitter, canonical y JSON-LD (`Organization` + `Product`/`Offer`) sin SSR.
      - URLs: `…/product/{slug|id}` — `GetProductDetailAsync` resuelve GUID o slug; `buildProductUrl` / WhatsApp emiten slug cuando existe.
      - Tags: chips en tarjeta/detalle; click filtra vía `search` (API ya busca en `Tags`); tags también van a meta `keywords`.
      - SEO 1.5: `buildProductImageAlt` (nombre + tag/categoría/desc, máx. 125); H1 único en ficha (brand pasa a `span` con modal abierto); meta description ideal 140–155 (maxLength duro + aviso suave en back-office).
      - SEO Fase 2 (sin SSR Angular): HTML OG en Core `GET /api/core/store/public-storefront-seo/{product|catalog|sitemap.xml|robots.txt}`. Soft-redirect a SPA solo con `location.replace` (sin `meta refresh`: WhatsApp/Facebook lo siguen y pierden OG). `og:url`/canonical = URL SPA. Ruta canónica única: `/store/products/catalog` (ya no `/catalogo`). `App:AngularUrl` / `App:GatewayUrl`.
      - Share/WhatsApp usan la URL pública SPA. El host Angular (`seo-bot-proxy.server.js` / nginx) detecta UA de crawlers y proxea producto/catálogo al SEO de Core con tenant de subdominio o `?tenant=`.
    - **Productos sin categoría en catálogo público (2026-11-06)**:
      - `StoreProductCatalogHelper.WhereSellable` / `IsSellable` ya no exigen `CategoryId`; basta producto activo, precio > 0 y (sin categoría **o** categoría activa). Aplica también a pedidos WhatsApp.
      - El badge "Todos" del storefront no puede sumar solo `categories.productCount` (ignora uncategorized); se usa `sellableTotalCount` desde `getProducts` sin filtro de categoría.
      - `GetCategoriesAsync` ya no filtra `ProductCount > 0`: las categorías activas vacías siguen listadas en el catálogo (badge 0 / sin badge).
    - **Infinite scroll del catálogo (2026-11-09)**:
      - Primera página `PAGE_SIZE=24`; al acercarse al final del viewport un `#infiniteScrollSentinel` con `IntersectionObserver` (`rootMargin` 320px) llama `loadMoreProducts` y appendea.
      - Se reemplazó el botón "Cargar más"; el sentinel muestra spinner + `Storefront:LoadingMore` mientras `isLoadingMore`.
    - **SEO keywords principal vs relacionadas (2026-11-09)**:
      - `CatalogProduct.PrimaryKeyword` (80) + `RelatedKeywords` (500, CSV). Migración `AddCatalogProductSeoKeywords`.
      - Meta/ALT/JSON-LD: `CatalogProductSeoKeywords.Build` / `buildProductKeywords` = primary → related → tags (dedupe).
      - Búsqueda pública incluye ambos campos y hace boost (primary > related > name) cuando hay `search`.
      - Back-office: inputs en sección SEO + aviso si la principal no aparece en meta title/desc.

