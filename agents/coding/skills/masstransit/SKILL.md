---
name: masstransit
description: Implement MassTransit message bus in .NET microservices. Covers consumers, producers, transport configuration (RabbitMQ, Azure Service Bus), saga state machines, middleware (retry, outbox), health checks, testing with the test harness, and ABP Framework integration. Use when building cross-service messaging, event-driven workflows, or request/response patterns in the FlyGuys platform.
---

# MassTransit

MassTransit is a transport-agnostic .NET message bus abstraction. It decouples services through messages, consumers, and configurable transports (RabbitMQ, Azure Service Bus, Amazon SQS, etc.).

FlyGuys uses MassTransit as the event bus layer across all microservices under `NVC.FlyGuys/services/`.

Reference: [masstransit.io/documentation](https://masstransit.io/documentation/concepts)

---

## Core Concepts

| Concept | Role |
|---|---|
| **Message** | Plain C# record/class — the data contract between services |
| **Consumer** | Handles a message type; implements `IConsumer<T>` |
| **Producer** | Publishes or sends messages via `IPublishEndpoint` / `ISendEndpointProvider` |
| **Transport** | The broker underneath (RabbitMQ, Azure Service Bus, etc.) |
| **Receive Endpoint** | A queue wired to one or more consumers |
| **Saga** | Stateful, long-running process tied to a correlation ID |

---

## Messages

Messages are plain C# types — use interfaces or records. Never use base classes.

```csharp
// Preferred: interface contract (supports multiple implementations)
public interface MissionStatusChanged
{
    Guid MissionId { get; }
    string NewStatus { get; }
    Guid? TenantId { get; }
}

// Also valid: record
public record OrderPlaced(Guid OrderId, Guid CustomerId, DateTime PlacedAt);
```

Message types are routed by **full type name**. Namespace and class name form the topic/exchange name — keep them stable. Renaming a message type is a breaking change.

---

## Configuration

### Basic Setup (NuGet packages)

```
MassTransit
MassTransit.RabbitMQ          // for RabbitMQ transport
MassTransit.Azure.ServiceBus.Core  // for Azure Service Bus transport
```

### Register MassTransit in ASP.NET Core / ABP Module

```csharp
services.AddMassTransit(x =>
{
    // Register all consumers in the assembly automatically
    x.AddConsumers(typeof(MyServiceModule).Assembly);

    // Use kebab-case queue names: "mission-status-changed"
    x.SetKebabCaseEndpointNameFormatter();

    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host(configuration["MassTransit:RabbitMq:Host"], h =>
        {
            h.Username(configuration["MassTransit:RabbitMq:Username"]);
            h.Password(configuration["MassTransit:RabbitMq:Password"]);
        });

        // Auto-configure receive endpoints for all registered consumers
        cfg.ConfigureEndpoints(context);
    });
});
```

> Always call `ConfigureEndpoints` **last** — after all middleware and consumer definitions are applied.

### appsettings.json (RabbitMQ transport)

```json
"MassTransit": {
  "RabbitMq": {
    "Host": "amqp://localhost",
    "Username": "guest",
    "Password": "guest"
  }
}
```

### Azure Service Bus transport (alternative)

```csharp
x.UsingAzureServiceBus((context, cfg) =>
{
    cfg.Host(configuration["MassTransit:AzureServiceBus:ConnectionString"]);
    cfg.ConfigureEndpoints(context);
});
```

### In-Memory transport (testing / local development)

```csharp
x.UsingInMemory((context, cfg) =>
{
    cfg.ConfigureEndpoints(context);
});
```

---

## Consumers

A consumer handles a specific message type. Each consumer gets its own queue by default.

```csharp
public class MissionStatusChangedConsumer : IConsumer<MissionStatusChanged>
{
    private readonly INotificationService _notifications;

    public MissionStatusChangedConsumer(INotificationService notifications)
    {
        _notifications = notifications;
    }

    public async Task Consume(ConsumeContext<MissionStatusChanged> context)
    {
        await _notifications.SendStatusAlertAsync(
            context.Message.MissionId,
            context.Message.NewStatus,
            context.CancellationToken);
    }
}
```

### Consumer Definition (retry, concurrency, endpoint name)

```csharp
public class MissionStatusChangedConsumerDefinition
    : ConsumerDefinition<MissionStatusChangedConsumer>
{
    public MissionStatusChangedConsumerDefinition()
    {
        EndpointName = "notifications-mission-status";
        ConcurrentMessageLimit = 10;
    }

    protected override void ConfigureConsumer(
        IReceiveEndpointConfigurator endpointConfigurator,
        IConsumerConfigurator<MissionStatusChangedConsumer> consumerConfigurator,
        IRegistrationContext context)
    {
        // Exponential retry: 5 attempts at 1s, 2s, 5s, 10s, 30s intervals
        endpointConfigurator.UseMessageRetry(r =>
            r.Intervals(1000, 2000, 5000, 10000, 30000));

        // Use in-memory outbox to prevent duplicate publishes on retry
        endpointConfigurator.UseInMemoryOutbox(context);
    }
}
```

### Consuming Multiple Message Types in One Consumer

```csharp
public class MissionEventConsumer :
    IConsumer<MissionCreated>,
    IConsumer<MissionCancelled>
{
    public async Task Consume(ConsumeContext<MissionCreated> context) { ... }
    public async Task Consume(ConsumeContext<MissionCancelled> context) { ... }
}
```

---

## Producers

### Publish (fan-out to all subscribers)

```csharp
public class MissionAppService : ApplicationService
{
    private readonly IPublishEndpoint _publishEndpoint;

    public MissionAppService(IPublishEndpoint publishEndpoint)
    {
        _publishEndpoint = publishEndpoint;
    }

    public async Task CompleteMissionAsync(Guid missionId)
    {
        // ... domain logic ...

        await _publishEndpoint.PublishAsync<MissionCompleted>(new
        {
            MissionId = missionId,
            CompletedAt = DateTime.UtcNow
        });
    }
}
```

### Send (point-to-point to a specific queue)

```csharp
public class InvoicingService
{
    private readonly ISendEndpointProvider _sendEndpointProvider;

    public async Task RequestInvoiceAsync(Guid orderId)
    {
        var endpoint = await _sendEndpointProvider.GetSendEndpoint(
            new Uri("queue:invoicing-generate-invoice"));

        await endpoint.Send(new GenerateInvoice { OrderId = orderId });
    }
}
```

> **Publish** = message goes to all consumers subscribed to the type (use for events).
> **Send** = message goes to one specific queue (use for commands).

---

## Endpoint Naming

MassTransit generates queue names from consumer class names. Configure a formatter to use consistent casing:

| Formatter | Consumer class | Queue name |
|---|---|---|
| Default (PascalCase) | `MissionStatusChangedConsumer` | `MissionStatusChanged` |
| Kebab-case | `MissionStatusChangedConsumer` | `mission-status-changed` |
| Snake-case | `MissionStatusChangedConsumer` | `mission_status_changed` |

FlyGuys convention: **kebab-case** (`x.SetKebabCaseEndpointNameFormatter()`).

Add a prefix per service to avoid queue name collisions across services:

```csharp
x.SetEndpointNameFormatter(
    new KebabCaseEndpointNameFormatter(prefix: "missions", includeNamespace: false));
// → "missions-mission-status-changed"
```

---

## Middleware — Retry

Apply retry at the endpoint level in the consumer definition:

```csharp
// Fixed intervals
endpointConfigurator.UseMessageRetry(r => r.Interval(5, TimeSpan.FromSeconds(5)));

// Exponential back-off
endpointConfigurator.UseMessageRetry(r => r.Exponential(5, TimeSpan.FromSeconds(1), TimeSpan.FromSeconds(30), TimeSpan.FromSeconds(2)));

// Ignore specific exceptions (do not retry)
endpointConfigurator.UseMessageRetry(r =>
{
    r.Interval(3, 1000);
    r.Ignore<ValidationException>();
    r.Ignore<ArgumentNullException>();
});
```

---

## Middleware — Outbox (prevent duplicate publishes on retry)

Use the **in-memory outbox** within a consumer to batch outgoing messages and publish only after the consumer completes successfully:

```csharp
endpointConfigurator.UseInMemoryOutbox(context);
```

Use the **transactional outbox** when you need durability across DB transactions (requires EF Core persistence):

```csharp
// In AddMassTransit registration
x.AddEntityFrameworkOutbox<MyDbContext>(o =>
{
    o.UseSqlServer();
    o.UseBusOutbox(); // deliver outbox messages via the bus
});

// In consumer definition
endpointConfigurator.UseEntityFrameworkOutbox<MyDbContext>(context);
```

---

## Request / Response

MassTransit provides typed request/response over the bus — no HTTP call needed between services.

```csharp
// Client side (e.g., missions service requesting pilot info)
public class MissionAssignmentService
{
    private readonly IRequestClient<GetPilotDetails> _pilotClient;

    public MissionAssignmentService(IRequestClient<GetPilotDetails> pilotClient)
    {
        _pilotClient = pilotClient;
    }

    public async Task<PilotDetailsResult> GetPilotAsync(Guid pilotId)
    {
        var response = await _pilotClient.GetResponse<PilotDetailsResult>(
            new GetPilotDetails { PilotId = pilotId });

        return response.Message;
    }
}

// Server side (pilots service)
public class GetPilotDetailsConsumer : IConsumer<GetPilotDetails>
{
    public async Task Consume(ConsumeContext<GetPilotDetails> context)
    {
        var pilot = await LoadPilotAsync(context.Message.PilotId);

        await context.RespondAsync(new PilotDetailsResult
        {
            PilotId = pilot.Id,
            Name = pilot.FullName,
            IsAvailable = pilot.IsAvailable
        });
    }
}
```

Register the request client:

```csharp
services.AddMassTransit(x =>
{
    x.AddRequestClient<GetPilotDetails>();
    // ...
});
```

---

## Saga State Machines

Sagas track long-running processes correlated by an ID. Prefer MassTransit Saga State Machines over consumer sagas for complex flows.

```csharp
public class MissionSagaState : SagaStateMachineInstance
{
    public Guid CorrelationId { get; set; }
    public string CurrentState { get; set; }
    public Guid? AssignedPilotId { get; set; }
}

public class MissionStateMachine : MassTransitStateMachine<MissionSagaState>
{
    public State Pending { get; private set; }
    public State Assigned { get; private set; }
    public State Completed { get; private set; }

    public Event<MissionCreated> MissionCreatedEvent { get; private set; }
    public Event<PilotAssigned> PilotAssignedEvent { get; private set; }
    public Event<MissionCompleted> MissionCompletedEvent { get; private set; }

    public MissionStateMachine()
    {
        InstanceState(x => x.CurrentState);

        Event(() => MissionCreatedEvent, x => x.CorrelateById(m => m.Message.MissionId));
        Event(() => PilotAssignedEvent, x => x.CorrelateById(m => m.Message.MissionId));
        Event(() => MissionCompletedEvent, x => x.CorrelateById(m => m.Message.MissionId));

        Initially(
            When(MissionCreatedEvent)
                .TransitionTo(Pending));

        During(Pending,
            When(PilotAssignedEvent)
                .Then(ctx => ctx.Saga.AssignedPilotId = ctx.Message.PilotId)
                .TransitionTo(Assigned));

        During(Assigned,
            When(MissionCompletedEvent)
                .TransitionTo(Completed)
                .Finalize());
    }
}
```

Register the saga with EF Core persistence:

```csharp
x.AddSagaStateMachine<MissionStateMachine, MissionSagaState>()
    .EntityFrameworkRepository(r =>
    {
        r.ConcurrencyMode = ConcurrencyMode.Pessimistic;
        r.AddDbContext<DbContext, MissionSagaDbContext>((provider, builder) =>
        {
            builder.UseSqlServer(connectionString);
        });
    });
```

---

## Health Checks

MassTransit registers health checks automatically. Wire them in `Program.cs`:

```csharp
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.MapHealthChecks("/health/live", new HealthCheckOptions());
```

Status values:
- `Healthy` — connected and processing
- `Degraded` — connected but broker issues detected
- `Unhealthy` — not connected (may trigger orchestrator restart)

---

## Testing with the Test Harness

Use `MassTransit.Testing` to test consumers without a real broker:

```csharp
[Fact]
public async Task MissionStatusChangedConsumer_SendsNotification()
{
    await using var harness = new InMemoryTestHarness();
    var consumerHarness = harness.Consumer<MissionStatusChangedConsumer>();

    await harness.Start();

    await harness.InputQueueSendEndpoint.Send(new MissionStatusChanged
    {
        MissionId = Guid.NewGuid(),
        NewStatus = "Completed"
    });

    Assert.True(await consumerHarness.Consumed.Any<MissionStatusChanged>());
}
```

With `IServiceCollection` and the test harness (v8+):

```csharp
await using var provider = new ServiceCollection()
    .AddMassTransitTestHarness(x =>
    {
        x.AddConsumer<MissionStatusChangedConsumer>();
    })
    .BuildServiceProvider(true);

var harness = provider.GetRequiredService<ITestHarness>();
await harness.Start();

var client = harness.GetRequestClient<MissionStatusChanged>();
// ... assert consumed, published, sent
```

---

## Integration with ABP Framework (FlyGuys pattern)

ABP's `IDistributedEventBus` can be layered over MassTransit. Alternatively, inject MassTransit interfaces directly for non-ABP publish/subscribe flows.

### When to use `IDistributedEventBus` (ABP)
- Events already defined as ABP ETOs
- You want ABP's outbox, tenant context propagation, and correlation handled automatically

### When to use MassTransit directly (`IPublishEndpoint`)
- New cross-service messages not bound to ABP ETOs
- Saga state machines (MassTransit-native)
- Request/response patterns
- Advanced middleware (transactional outbox, retry definitions)

### Both patterns in the same service

```csharp
public class MissionAppService : ApplicationService
{
    // ABP event bus — for ABP ETO events
    private readonly IDistributedEventBus _abpEventBus;

    // MassTransit — for new message contracts and sagas
    private readonly IPublishEndpoint _publishEndpoint;

    public async Task CompleteMissionAsync(Guid missionId)
    {
        // ABP-style
        await _abpEventBus.PublishAsync(new MissionCompletedEto { MissionId = missionId });

        // MassTransit-style (saga trigger)
        await _publishEndpoint.PublishAsync<MissionCompleted>(new { MissionId = missionId });
    }
}
```

---

## Checklist for New Consumers

- [ ] Message type defined as interface or record in `*.Application.Contracts`
- [ ] Consumer class implements `IConsumer<T>` and registered via `AddConsumers(assembly)`
- [ ] Consumer definition created with retry policy and concurrency limit
- [ ] Queue name prefix matches service name (kebab-case formatter with prefix)
- [ ] In-memory outbox applied if consumer publishes additional events
- [ ] Consumer tested with `ITestHarness` (no real broker required)
- [ ] Health check endpoints configured in `HttpApi.Host`
- [ ] `appsettings.json` transport config set per environment

---

## Anti-Patterns to Avoid

- Publishing messages inside a consumer **without** the outbox — risks duplicate events on retry
- Using `IBus` directly instead of `IPublishEndpoint` or `ISendEndpointProvider` — `IBus` is for non-request-scoped publishes only
- Sharing a single queue across unrelated consumers — prefer one queue per consumer
- Putting domain logic inside `Consume()` — delegate to an Application Service or Domain Service
- Catching all exceptions in `Consume()` and swallowing them — let MassTransit retry handle transient failures
- Hardcoding queue URIs in `Send()` calls — use endpoint name formatters or definitions

---

## References

- [MassTransit Concepts](https://masstransit.io/documentation/concepts)
- [MassTransit Configuration](https://masstransit.io/documentation/configuration)
- [MassTransit Patterns](https://masstransit.io/documentation/patterns)
- [MassTransit Transports](https://masstransit.io/documentation/transports)
