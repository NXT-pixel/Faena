# Technical Context
**Created**: 2026-10-25T04:00:37.405234+00:00
**Last Updated**: 2026-10-26T22:30:00Z

## Repositorios Activos en `Proyecto/`

### 1. `Proyecto/growthhacking.PrototypeZero`
- **Plataforma / Runtime**: **.NET 10.0** SDK `10.0.402` (`net10.0`)
- **Framework Principal**: **ABP Framework 10.5.0** (ABP Commercial / Studio Microservices)
- **Frontend**: **Angular 21** (`@angular/core: ~21.2.0`) en `apps/angular`
  - Gestor de paquetes: **Yarn 1.22.22** (Node.js `v24.20.0`)
  - Puerto de desarrollo: `http://localhost:4200`
- **Arquitectura**: Microservicios distribuidos con API Gateway y AuthServer OpenIddict
- **Buses & Mensajería**: Azure Service Bus (`Volo.Abp.EventBus.Azure` 10.5.0), RabbitMQ
- **Almacenamiento & Caching**: SQL Server (EF Core), Redis, PostgreSQL, Azure Blob Storage (cuenta `ghstoragedev02`)
- **Orquestación Local**: Docker Compose (`etc/docker/containers/`)

---

## 🌐 Mapa de Puertos y Servicios Locales

| Servicio / Proyecto | Puerto / URL Local | Descripción |
| :--- | :--- | :--- |
| **Angular UI** | `http://localhost:4200` | Frontend principal SPA Angular 21 |
| **PrototypeZero.WebGateway** | `http://localhost:44368` | API Gateway principal (YARP reverse proxy) |
| **PrototypeZero.AuthServer** | `http://localhost:44333` | Servidor de Autenticación OpenIddict |
| **AdministrationService** | `http://localhost:44388` | Servicio de administración y permisos |
| **AiService** | `http://localhost:44366` | Agente IA, OpenAI, MCP y extracción de catálogos |
| **CoreService** | `http://localhost:44314` | Lógica de negocio core (catálogos, borradores, órdenes) |
| **FileManagementService** | `http://localhost:44346` | Gestión de blobs y URLs públicas temporales |
| **IdentityService** | `http://localhost:44305` | Gestión de usuarios, roles e identidades |
| **PaymentService** | `http://localhost:44367` | Procesamiento y reglas de pagos Wompi |
| **SaasService** | `http://localhost:44374` | Gestión de Tenants y personalización de marca |
| **WhatsAppService** | `http://localhost:44364` | Integración y webhooks de WhatsApp (360Dialog / WABA) |
| **SQL Server (Docker)** | `localhost:1434` | Instancia local Azure SQL Edge |
| **Redis (Docker)** | `localhost:6379` | Cache distribuido |
| **RabbitMQ (Docker)** | `localhost:5672` (Admin: `15672`) | Bus de eventos / mensajería local |
