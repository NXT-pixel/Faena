# Project Structure
**Created**: 2026-10-25T04:00:37.405234+00:00
**Last Updated**: 2026-10-26T22:30:00Z

## 🏢 Arquitectura y Disposición del Repositorio

- **`Proyecto/`**: Repositorios de código fuente reales del cliente (ignorado en `.gitignore` del harness).
- **`tasks/`**: Tareas activas, especificaciones técnicas y contexto del equipo.
- **`rules/`**: Reglas globales, de seguridad y estándares del proyecto.
- **`skills/`**: Conocimiento técnico específico (ABP, .NET, Angular, Azure).
- **`agents/`**: Personas y roles especializados para diseño y codificación.
- **`commands/`**: Flujo de comandos arrastrables en el chat de Faena.

---

## 📦 Repositorios Clonados en `Proyecto/`

### `Proyecto/growthhacking.PrototypeZero`
- **Rama Actual**: `bug/preserve-price`
- **Últimos Commits**:
  - `5e1ff37`: Merged PR 14564: Update angular.json
  - `afdf4e3`: Update angular.json
  - `f664a6a`: Merged PR 14563: Catalog Storefront
- **Estructura Interna**:
  - `apps/`:
    - `angular/`: Frontend SPA Angular 21 (ABP Framework UI)
    - `auth-server/`: Servidor de Autenticación OpenIddict (`PrototypeZero.AuthServer`)
    - `web-gateway/`: API Gateway YARP (`PrototypeZero.WebGateway`)
  - `services/`:
    - `administration/`: `PrototypeZero.AdministrationService` (Permisos, auditoría)
    - `ai/`: `PrototypeZero.AiService` (Agente IA, OpenAI, MCP, extracción documental)
    - `core/`: `PrototypeZero.CoreService` (Catálogo, borradores, productos, pedidos, logística)
    - `file-management/`: `PrototypeZero.FileManagementService` (Blobs Azure, enlaces públicos de descarga)
    - `identity/`: `PrototypeZero.IdentityService` (Usuarios, roles, claims)
    - `payment/`: `PrototypeZero.PaymentService` (Pasarela Wompi, enlaces de pago)
    - `saas/`: `PrototypeZero.SaasService` (Tenants, ediciones, branding por tenant)
    - `whatsapp/`: `PrototypeZero.WhatsAppService` (Integración con 360Dialog / Meta WABA)
  - `shared/`: Contratos compartidos, localizaciones y paquetes comunes de ABP
  - `etc/`: Configuraciones de Docker Compose, scripts y plantillas
