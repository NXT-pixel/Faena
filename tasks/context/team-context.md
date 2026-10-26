# Contexto del Equipo, Organización y Responsabilidades (`team-context.md`)

Este archivo define el organigrama, roles y fronteras de responsabilidad del proyecto/empresa.
Los agentes de Faena leen este documento para interpretar correctamente las menciones a personas en los tickets y saber qué tareas corresponden a desarrollo vs. qué debe delegarse o prepararse para QA, DevOps u otros compañeros.

---

## 🏢 Información de la Empresa / Proyecto

- **Empresa / Cliente**: [Nombre de la Empresa o Cliente, ej. Acme Corp]
- **Nombre del Proyecto**: [Nombre del Proyecto, ej. Portal de Clientes v2]
- **Mi Rol en el Proyecto**: [ej. Desarrollador Full-Stack / Backend Lead]
- **Objetivo Principal**: [ej. Modernizar la API de pagos y migrar el frontend a Angular con ABP]

---

## 🛡️ Identidad Git Corporativa (Obligatorio para Commits en Proyecto/)

Para evitar que se filtren cuentas personales de GitHub o correos personales (ej. la cuenta personal con la que se creó Faena), **todo commit o push dentro de cualquier repositorio en `Proyecto/` DEBE atribuirse a la identidad corporativa de la empresa/cliente**:

- **Nombre Git Corporativo (`user.name`)**: [ej. Santiago Guerrero]
- **Email Git Corporativo (`user.email`)**: [ej. santiago.guerrero@pevaar.com]
- **Dominio Corporativo Permitido**: [ej. @pevaar.com]

> ⚠️ **Regla de Oro**: Antes de ejecutar cualquier `git commit` o `git push` en cualquier repositorio en `Proyecto/`, el agente DEBE verificar con `git -C Proyecto/<repo> config --local user.email` que la identidad local corresponda a la corporativa aquí indicada. Si no está configurada, debe configurarse a nivel `--local` antes de commitear. NUNCA depender de la configuración `--global`.

---

## 👥 Roster del Equipo y Contactos Clave

| Nombre | Rol / Cargo | Responsabilidades Principales | Cuándo Consultar o Escalar |
| :--- | :--- | :--- | :--- |
| **[Nombre Jefe/Tech Lead]** | Tech Lead / Engineering Manager | Aprobación de arquitectura, decisiones técnicas de alto nivel, cambios en contratos públicos de API. | Dudas de diseño mayor, cambios en dependencias core o bloqueos con otras áreas. |
| **[Nombre Product Owner]** | Product Owner / PM | Criterios de aceptación del negocio, priorización de historias y alcance de features. | Ambigüedades en requerimientos de negocio o cambios de alcance del ticket. |
| **[Nombre QA Lead/Tester]** | QA Engineer / Tester | Pruebas funcionales, pruebas de regresión, certificación de releases y planes de prueba manuales. | Entrega de features terminados para certificación QA; proveer datos de prueba y pasos de reproducción. |
| **[Nombre DevOps/SRE]** | DevOps / Cloud Engineer | Infraestructura en Azure/AWS, pipelines de CI/CD, configuración de Kubernetes, permisos de base de datos. | Creación de recursos de nube, secretos en Key Vault o fallos en agentes de build/deploy. |
| **[Nombre Compañero Frontend]** | Desarrollador Frontend | Componentes UI en Angular, consumo de endpoints, maquetación y diseño de pantallas. | Coordinación de contratos DTO/JSON y eventos de WebSocket/SignalR. |
| **[Nombre Compañero Backend/DBA]** | Desarrollador Backend / DBA | Base de datos relacional, procedimientos almacenados, optimización de queries y servicios legacy. | Dudas sobre modelos de datos existentes o migraciones de base de datos complejas. |

---

## 🎯 Límites de Responsabilidad y Protocolo de Handoff (Delegación)

Los agentes de IA deben seguir estas directrices al interpretar los tickets:

1. **Lo que SÍ es nuestra responsabilidad de desarrollo**:
   - Escribir código limpio y probado (unit tests, integration tests).
   - Crear migraciones de base de datos y DTOs requeridos para el feature.
   - Generar proxies de API (ej. `abp generate-proxy`) y componentes front asignados.
   - Documentar endpoints (Swagger / OpenAPI) y criterios técnicos.

2. **Handoff a QA (Control de Calidad)**:
   - **NO** intentar simular la aprobación humana de QA en el ticket.
   - Al finalizar el desarrollo, generar una sección clara de *"Pasos para verificación de QA"* (endpoints, payloads de prueba, casos de borde y credenciales de prueba) dirigida a la persona de QA asignada.

3. **Handoff a DevOps / Infraestructura**:
   - **NO** modificar configuraciones de infraestructura críticas o secretos en producción.
   - Si el ticket requiere un nuevo secreto, variable de entorno o cola de mensajería (ej. Azure Service Bus), documentar la solicitud para el ingeniero de DevOps en el TRD.

4. **Toma de Decisiones y Menciones en Tickets**:
   - Si el ticket dice *"según lo acordado con [Tech Lead]"*, asumir que esa decisión técnica ya fue aprobada y tiene máxima prioridad.
   - Si el ticket menciona a un compañero para coordinación (*"revisar con [Compañero]"*), detallar en el TRD el punto de integración exacto.
