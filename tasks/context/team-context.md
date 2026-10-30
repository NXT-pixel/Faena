# Contexto del Equipo, Organización y Responsabilidades (`team-context.md`)

Este archivo define el organigrama, roles y fronteras de responsabilidad del proyecto/empresa.
Los agentes de Faena leen este documento para interpretar correctamente las menciones a personas en los tickets y saber qué tareas corresponden a desarrollo vs. qué debe delegarse o prepararse para QA, DevOps u otros compañeros.

---

## 🏢 Información de la Empresa / Proyecto

- **Empresa / Cliente**: Pevaar / Growth Hacking
- **Nombre del Proyecto**: PrototypeZero (Plataforma E-Commerce Multitenant con IA y Agente de WhatsApp)
- **Mi Rol en el Proyecto**: Desarrollador Full-Stack / Integrador IA
- **Objetivo Principal**: Mantener y evolucionar la arquitectura de microservicios (.NET 10 + ABP + Angular 21) para la gestión inteligente de catálogos, pedidos y atención comercial automatizada.

---

## 🛡️ Identidad Git Corporativa (Obligatorio para Commits en Proyecto/)

Para evitar que se filtren cuentas personales de GitHub o correos personales (ej. la cuenta personal con la que se creó Faena), **todo commit o push dentro de cualquier repositorio en `Proyecto/` DEBE atribuirse a la identidad corporativa de la empresa/cliente**:

- **Nombre Git Corporativo (`user.name`)**: Santiago
- **Email Git Corporativo (`user.email`)**: Santiago.guerrero@pevaar.com
- **Dominio Corporativo Permitido**: @pevaar.com

> ⚠️ **Regla de Oro**: Antes de ejecutar cualquier `git commit` o `git push` en cualquier repositorio en `Proyecto/`, el agente DEBE verificar con `git -C Proyecto/<repo> config --local user.email` que la identidad local corresponda a la corporativa aquí indicada. Si no está configurada, debe configurarse a nivel `--local` antes de commitear. NUNCA depender de la configuración `--global`.

---

## 👥 Roster del Equipo y Contactos Clave

| Nombre | Rol / Cargo | Responsabilidades Principales | Cuándo Consultar o Escalar |
| :--- | :--- | :--- | :--- |
| **David / Santiago** | Tech Lead / Engineering Lead | Aprobación de arquitectura, decisiones técnicas de alto nivel, contratos de microservicios y directrices core. | Dudas de diseño mayor, dependencias del sistema o acuerdos arquitectónicos. |
| **Product Owner** | Product Owner / PM | Criterios de aceptación del negocio, priorización de backlog y reglas de negocio para tenants. | Ambigüedades en requerimientos de negocio o cambios de alcance del ticket. |
| **Laura** | QA Engineer / Tester | Pruebas funcionales, pruebas de regresión, certificación de releases y validación de endpoints/UI. | Entrega de features terminados para certificación QA; proveer datos de prueba y casos de borde. |
| **Sofía** | DevOps / Cloud Engineer | Infraestructura en Azure (Azure Service Bus, Blob Storage, Key Vault), túneles y pipelines de CI/CD. | Creación de recursos de nube, secretos de infraestructura o problemas de despliegue. |
| **Compañero Frontend** | Desarrollador Frontend Angular | Componentes UI en Angular 21, proxies ABP, formularios reactivos y estilos corporativos. | Coordinación de contratos DTO/JSON y componentes compartidos de UI. |
| **Compañero Backend/DBA** | Desarrollador Backend .NET | Microservicios ABP, EF Core, optimización de queries y eventos distribuidos. | Dudas sobre modelos de datos existentes o migraciones de base de datos complejas. |

---

## 🎯 Límites de Responsabilidad y Protocolo de Handoff (Delegación)

Los agentes de IA deben seguir estas directrices al interpretar los tickets:

1. **Lo que SÍ es nuestra responsabilidad de desarrollo**:
   - Escribir código limpio y probado siguiendo TDD estricto (unit tests, integration tests).
   - Crear migraciones de base de datos y DTOs requeridos para el feature.
   - Generar proxies de API (ej. `abp generate-proxy`) y componentes front asignados en Angular.
   - Documentar endpoints (Swagger / OpenAPI) y criterios técnicos.

2. **Handoff a QA (Control de Calidad - Laura)**:
   - **NO** intentar simular la aprobación humana de QA en el ticket.
   - Al finalizar el desarrollo, generar una sección clara de *"Pasos para verificación de QA"* (endpoints, payloads de prueba, casos de borde y credenciales de prueba) dirigida a Laura.

3. **Handoff a DevOps / Infraestructura (Sofía)**:
   - **NO** modificar configuraciones de infraestructura críticas o secretos en producción.
   - Si el ticket requiere un nuevo secreto, variable de entorno o cola de mensajería (ej. Azure Service Bus), documentar la solicitud para Sofía en el TRD.

4. **Toma de Decisiones y Menciones en Tickets**:
   - Si el ticket dice *"según lo acordado con [Tech Lead]"*, asumir que esa decisión técnica ya fue aprobada y tiene máxima prioridad.
   - Si el ticket menciona a un compañero para coordinación (*"revisar con [Compañero]"*), detallar en el TRD el punto de integración exacto.
