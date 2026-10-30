# 🧠 Skills: Catálogo de Conocimiento Técnico

Este directorio es la **única fuente de verdad** del conocimiento técnico especializado de Faena.

## Contrato

- Una skill = una carpeta `skills/<nombre>/` que contiene un archivo `SKILL.md`.
- **Nunca** se copian skills fuera de `skills/`. Un `SKILL.md` dentro de `agents/`, `commands/` o cualquier otra ruta es un bug.
- El front matter de cada `SKILL.md` es obligatorio y debe tener:
  - `name`: idéntico al nombre de la carpeta.
  - `description`: qué cubre la skill y, al final, **cuándo usarla**.
- Los archivos auxiliares (`references/`, `assets/`, `resources/`) viven dentro de la carpeta de su skill y se leen solo cuando `SKILL.md` los referencia para la tarea en curso.

## Cómo la usa el agente

1. Lee la regla [`rules/skills-routing.md`](../rules/skills-routing.md) (siempre activa).
2. Busca en este catálogo la skill que corresponde al dominio del ticket.
3. Abre `skills/<nombre>/SKILL.md` **antes** de escribir código, tests o una revisión de ese dominio.

## Agregar o editar una skill

1. Crea o edita `skills/<nombre>/SKILL.md` con su front matter.
2. Regenera el catálogo:

   ```powershell
   .\scripts\build-skills-index.ps1
   ```

3. Verifica el harness completo:

   ```powershell
   .\scripts\validate-faena.ps1
   ```

   La validación falla si el catálogo quedó viejo, si hay un `SKILL.md` fuera de `skills/` o si un `name` no coincide con su carpeta.

## Skills privadas de la empresa

Las skills internas de un cliente (SDKs propios, APIs privadas) van en [`skills/project/`](project/), no en `skills/` a secas. Ver ese README para el criterio de aislamiento.

---

_La sección siguiente es generada automáticamente. No la edites a mano: corre el script._

<!-- BEGIN:skills -->
_Generado por `scripts/build-skills-index.ps1`. No editar a mano._

**29 skills disponibles.**

| Skill | Descripcion |
| :--- | :--- |
| [`abp-angular`](abp-angular/SKILL.md) | ABP Angular UI patterns - generate-proxy, ListService, PermissionGuard, abpLocalization pipe, ConfirmationService, ToasterService, ConfigStateService. Use when building or reviewing Angular UI components, routing, or service integration in ABP Angular projects. |
| [`abp-authorization`](abp-authorization/SKILL.md) | ABP permission system - PermissionDefinitionProvider, [Authorize] attribute, CheckPolicyAsync, IsGrantedAsync, ICurrentUser, IPermissionManager, multi-tenancy side. Use when working with permissions, authorization, role-based access, or security in ABP projects. |
| [`abp-cli`](abp-cli/SKILL.md) | ABP CLI commands - generate-proxy, install-libs, add-package-ref, new-module, install-module, abp update, abp clean, abp suite generate. Use when the user asks how to run ABP CLI commands, generate proxies, install libraries, or use ABP Suite. |
| [`abp-core`](abp-core/SKILL.md) | Core ABP Framework conventions - module system, DI registration, base classes (ApplicationService, DomainService), IClock, BusinessException, localization, async patterns. Use when working on any ABP project, asking about ABP fundamentals, or unsure which skill applies. |
| [`abp-ef-core`](abp-ef-core/SKILL.md) | ABP Entity Framework Core - DbContext, entity configuration, EfCoreRepository implementation, migrations (dotnet ef migrations add), data seeding. Use when working in EntityFrameworkCore projects, adding migrations, or implementing EF Core repositories. |
| [`abp-infrastructure`](abp-infrastructure/SKILL.md) | ABP infrastructure services - ISettingProvider, IFeatureChecker, IDistributedCache, ILocalEventBus, IDistributedEventBus, IBackgroundJobManager, localization resource. Use when working with settings, feature flags, caching, event bus, or background jobs in ABP. |
| [`abp-microservices`](abp-microservices/SKILL.md) | ABP Microservice solution template - service structure, Integration Services ([IntegrationService]), inter-service HTTP proxies, distributed events with Outbox/Inbox, Entity Cache, RabbitMQ/Redis/YARP setup. Use when working with the ABP microservice solution template or inter-service communication patterns. |
| [`abp-multitenancy`](abp-multitenancy/SKILL.md) | ABP Multi-Tenancy - IMultiTenant interface, CurrentTenant, CurrentTenant.Change(), DataFilter.Disable(IMultiTenant), tenant resolution order, database-per-tenant. Use when working with multi-tenant features, tenant-specific data isolation, or switching tenant context. |
| [`abp-no-layers`](abp-no-layers/SKILL.md) | ABP Single-Layer (No-Layers / nolayers) application template - single project structure, feature-based file organization, no separate Domain/Application.Contracts projects. Use when working with the single-layer web application template or when the project has no layered separation. |
| [`angular-developer`](angular-developer/SKILL.md) | Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (signals, linkedSignal, resource), forms, dependency injection, routing, SSR, accessibility (ARIA), animations, styling (component styles, Tailwind CSS), testing, or CLI tooling. |
| [`api-design-principles`](api-design-principles/SKILL.md) | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewing API specifications, or establishing API design standards. |
| [`architecture-patterns`](architecture-patterns/SKILL.md) | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use when architecting complex backend systems or refactoring existing applications for better maintainability. |
| [`azure-function`](azure-function/SKILL.md) | Design and build Azure Functions using the .NET 8 isolated worker model. Covers project structure, Program.cs DI setup, environment variable validation, single functions (Timer, HTTP, Service Bus, Cosmos DB triggers), Durable Functions (orchestrator, activity, client patterns), MassTransit with Azure Service Bus, CosmosDB integration, Application Insights, and error handling. Use when creating, extending, or reviewing Azure Function projects in the FlyGuys solution. |
| [`cqrs-implementation`](cqrs-implementation/SKILL.md) | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems. |
| [`csharp-testing`](csharp-testing/SKILL.md) | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when writing or reviewing xUnit tests, mocks, or integration tests in a C# / .NET project. |
| [`docker-patterns`](docker-patterns/SKILL.md) | Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orchestration. Use when creating or reviewing Dockerfiles and Compose services, testing installers across Linux distributions, or planning accurate native macOS and Windows validation. |
| [`dotnet-patterns`](dotnet-patterns/SKILL.md) | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. Use when writing or reviewing C# / .NET code — DI, async, or general conventions. |
| [`event-store-design`](event-store-design/SKILL.md) | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| [`frontend-a11y`](frontend-a11y/SKILL.md) | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader support. Use when building or reviewing forms, modals, dropdowns, tooltips, or tabs, fixing a11y lint or code-review findings, or wiring up keyboard navigation and focus management. |
| [`frontend-patterns`](frontend-patterns/SKILL.md) | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or reviewing React or Next.js components, state, or render performance. |
| [`masstransit`](masstransit/SKILL.md) | Implement MassTransit message bus in .NET microservices. Covers consumers, producers, transport configuration (RabbitMQ, Azure Service Bus), saga state machines, middleware (retry, outbox), health checks, testing with the test harness, and ABP Framework integration. Use when building cross-service messaging, event-driven workflows, or request/response patterns in the FlyGuys platform. |
| [`microservices-patterns`](microservices-patterns/SKILL.md) | Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices. |
| [`projection-patterns`](projection-patterns/SKILL.md) | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| [`python-backend-development`](python-backend-development/SKILL.md) | Build production-ready Python backend services using FastAPI, SQLAlchemy, async patterns, testing, and API design best practices. Use when creating or refactoring Python APIs, designing service architecture, or improving backend reliability and performance. |
| [`saga-orchestration`](saga-orchestration/SKILL.md) | Implement saga patterns for distributed transactions and cross-aggregate workflows. Use when coordinating multi-step business processes, handling compensating transactions, or managing long-running workflows. |
| [`security-review`](security-review/SKILL.md) | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns. |
| [`security-scan`](security-scan/SKILL.md) | Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Checks CLAUDE.md, settings.json, MCP servers, hooks, and agent definitions. Use when auditing a .claude/ directory — CLAUDE.md, settings.json, MCP servers, hooks, or agent definitions. |
| [`temporal-python-testing`](temporal-python-testing/SKILL.md) | Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integration testing, replay testing, and local development setup. Use when implementing Temporal workflow tests or debugging test failures. |
| [`workflow-orchestration-patterns`](workflow-orchestration-patterns/SKILL.md) | Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determinism constraints. Use when building long-running processes, distributed transactions, or microservice orchestration. |
<!-- END:skills -->
