---
name: azure-function
description: Design and build Azure Functions using the .NET 8 isolated worker model. Covers project structure, Program.cs DI setup, environment variable validation, single functions (Timer, HTTP, Service Bus, Cosmos DB triggers), Durable Functions (orchestrator, activity, client patterns), MassTransit with Azure Service Bus, CosmosDB integration, Application Insights, and error handling. Use when creating, extending, or reviewing Azure Function projects in the FlyGuys solution.
---

# Azure Functions — .NET 8 Isolated Worker Model

FlyGuys Azure Functions use the **isolated worker model** (`Microsoft.Azure.Functions.Worker`), not the legacy in-process model. All functions target **net8.0**.

## Project Structure

```
MyFunction/
├── Program.cs                  # DI host setup, env var validation
├── MyFunction.csproj
├── local.settings.json
├── Functions/
│   ├── MyTimerFunction.cs      # Single function triggers
│   └── Orchestrator/           # Durable function orchestrators & activities
│       ├── MyOrchestrator.cs
│       └── MyActivity.cs
├── Services/
│   ├── IMyService.cs
│   └── MyService.cs
├── Repositories/
│   ├── IMyRepository.cs
│   └── MyRepository.cs
├── Models/
│   └── MyModel.cs
├── Data/
│   └── MyDbContext.cs          # EF Core DbContexts
└── CosmosDb/
    └── MyCosmosDbContext.cs
```

## Required NuGet Packages

```xml
<PackageReference Include="Microsoft.Azure.Functions.Worker" Version="2.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http" Version="3.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Timer" Version="4.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.DurableTask" Version="1.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.ApplicationInsights" Version="1.*" />
<PackageReference Include="Microsoft.DurableTask.Client" Version="1.*" />
<PackageReference Include="Microsoft.DurableTask.Worker" Version="1.*" />
```

## Program.cs — Host Setup

Use `HostBuilder` with `ConfigureFunctionsWebApplication()`. Always validate required environment variables at startup — fail fast with a descriptive message.

```csharp
// Program.cs — top-level statements
ValidateEnvironmentVariables();

string dbConnection = Environment.GetEnvironmentVariable("DbConnection")!;
string serviceBusConnection = Environment.GetEnvironmentVariable("AzureServiceBusConnectionString")!;

var services = new ServiceCollection();

services.AddApplicationInsightsTelemetryWorkerService();
services.ConfigureFunctionsApplicationInsights();

// MassTransit — Azure Service Bus
services.AddMassTransit(x =>
{
    x.UsingAzureServiceBus((context, cfg) =>
    {
        cfg.Host(serviceBusConnection);
        cfg.ConfigureEndpoints(context);
    });
});

// HTTP clients with Polly retry
services.AddHttpClient().AddPolicyHandler(GetRetryPolicy());

// EF Core
services.AddDbContext<MyDbContext>(options =>
    options.UseSqlServer(dbConnection));

// CosmosDB (FlyGuys shared extension)
await services.AddCosmosDbContext<MyCosmosDbContext>(
    Environment.GetEnvironmentVariable("CosmosDbConnectionString")
        ?? throw new Exception("Missing CosmosDbConnectionString"),
    Environment.GetEnvironmentVariable("CosmosDbDatabaseId")
        ?? throw new Exception("Missing CosmosDbDatabaseId")
);

// Repositories & services
services.AddScoped<IMyRepository, MyRepository>();
services.AddScoped<IMyService, MyService>();

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication()
    .ConfigureServices(serviceCollection =>
    {
        foreach (var service in services)
            serviceCollection.Add(service);
    })
    .Build();

host.Run();

// ── Environment variable validation ──────────────────────────────────────────
static void ValidateEnvironmentVariables()
{
    var required = new Dictionary<string, string>
    {
        { "DbConnection",                    "SQL Server connection string" },
        { "CosmosDbConnectionString",        "Cosmos DB connection string" },
        { "CosmosDbDatabaseId",              "Cosmos DB database ID" },
        { "AzureServiceBusConnectionString", "Azure Service Bus connection string" },
        { "MyTimerExpression",               "CRON expression for the timer trigger" },
    };

    var missing = required
        .Where(kv => string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable(kv.Key)))
        .Select(kv => $"  {kv.Key}: {kv.Value}")
        .ToList();

    if (missing.Count > 0)
        throw new Exception($"Missing required environment variables:\n{string.Join("\n", missing)}");
}

static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy() =>
    HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3,
            retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
            (outcome, timespan, retryAttempt, _) =>
                Console.WriteLine($"Retry {retryAttempt} after {timespan}: " +
                    $"{outcome.Exception?.Message ?? outcome.Result.StatusCode.ToString()}"));
```

## Single Functions

### Timer Trigger

Use `[TimerTrigger("%EnvVarName%")]` so the schedule is externally configurable.  
Always use `try/catch/finally` with structured logging.

```csharp
public class MyTimerFunction
{
    private readonly IMyService _service;
    private readonly ILogger<MyTimerFunction> _logger;

    public MyTimerFunction(IMyService service, ILogger<MyTimerFunction> logger)
    {
        _service = service;
        _logger = logger;
    }

    [Function(nameof(MyTimerFunction))]
    public async Task Run([TimerTrigger("%MyTimerExpression%")] TimerInfo timer)
    {
        _logger.LogInformation("{Function}: Starting at {Time}", nameof(MyTimerFunction), DateTime.UtcNow);

        try
        {
            await _service.ProcessAsync();
            _logger.LogInformation("{Function}: Completed at {Time}", nameof(MyTimerFunction), DateTime.UtcNow);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "{Function}: Error — {Message}", nameof(MyTimerFunction), ex.Message);
            throw; // re-throw so the Functions runtime marks the execution as failed
        }
    }
}
```

### HTTP Trigger

```csharp
public class MyHttpFunction
{
    private readonly IMyService _service;
    private readonly ILogger<MyHttpFunction> _logger;

    public MyHttpFunction(IMyService service, ILogger<MyHttpFunction> logger)
    {
        _service = service;
        _logger = logger;
    }

    [Function(nameof(MyHttpFunction))]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "my-route")] HttpRequestData req)
    {
        _logger.LogInformation("Processing HTTP request");

        try
        {
            var input = await req.ReadFromJsonAsync<MyInputDto>();
            var result = await _service.ProcessAsync(input!);

            var response = req.CreateResponse(HttpStatusCode.OK);
            await response.WriteAsJsonAsync(result);
            return response;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing request: {Message}", ex.Message);
            var errorResponse = req.CreateResponse(HttpStatusCode.InternalServerError);
            await errorResponse.WriteStringAsync(ex.Message);
            return errorResponse;
        }
    }
}
```

### Service Bus Trigger

```csharp
public class MyServiceBusFunction
{
    private readonly IMyService _service;
    private readonly ILogger<MyServiceBusFunction> _logger;

    public MyServiceBusFunction(IMyService service, ILogger<MyServiceBusFunction> logger)
    {
        _service = service;
        _logger = logger;
    }

    [Function(nameof(MyServiceBusFunction))]
    public async Task Run(
        [ServiceBusTrigger("%QueueName%", Connection = "AzureServiceBusConnectionString")] MyMessage message)
    {
        _logger.LogInformation("Received message for {Id}", message.Id);

        try
        {
            await _service.HandleAsync(message);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process message {Id}: {Message}", message.Id, ex.Message);
            throw;
        }
    }
}
```

### Cosmos DB Change Feed Trigger

```csharp
public class MyCosmosChangeFeedFunction
{
    private readonly IMyService _service;
    private readonly ILogger<MyCosmosChangeFeedFunction> _logger;

    public MyCosmosChangeFeedFunction(IMyService service, ILogger<MyCosmosChangeFeedFunction> logger)
    {
        _service = service;
        _logger = logger;
    }

    [Function(nameof(MyCosmosChangeFeedFunction))]
    public async Task Run(
        [CosmosDBTrigger(
            databaseName: "%CosmosDbDatabaseId%",
            containerName: "my-container",
            Connection = "CosmosDbConnectionString",
            LeaseContainerName = "leases",
            CreateLeaseContainerIfNotExists = true)]
        IReadOnlyList<MyDocument> documents)
    {
        if (documents == null || documents.Count == 0) return;

        _logger.LogInformation("Processing {Count} changed documents", documents.Count);

        foreach (var doc in documents)
        {
            try
            {
                await _service.ProcessDocumentAsync(doc);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing document {Id}: {Message}", doc.Id, ex.Message);
            }
        }
    }
}
```

## Durable Functions

Use Durable Functions for **long-running, stateful, multi-step workflows**. Three roles:
- **Client** — schedules new orchestration instances (`DurableTaskClient`)
- **Orchestrator** — defines the workflow; calls activities in sequence or in parallel (`TaskOrchestrationContext`)
- **Activity** — executes a single unit of work; has full access to DI services (`ActivityTrigger`)

### Client — Scheduling an Orchestration

Clients are typically Timer or HTTP triggered functions that start orchestrations.

```csharp
public class MyWorkflowStarter
{
    private readonly ILogger<MyWorkflowStarter> _logger;

    public MyWorkflowStarter(ILogger<MyWorkflowStarter> logger)
    {
        _logger = logger;
    }

    [Function(nameof(MyWorkflowStarter))]
    public async Task Run(
        [TimerTrigger("%WorkflowTimerExpression%")] TimerInfo timer,
        [DurableClient] DurableTaskClient client)
    {
        var input = new MyOrchestratorInput { BatchSize = 100 };
        string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
            nameof(MyOrchestrator), input);

        _logger.LogInformation("Scheduled orchestration {InstanceId}", instanceId);
    }
}
```

### Orchestrator

Orchestrators **must be deterministic** — no I/O, no random values, no `DateTime.Now` directly.  
Use `context.CallActivityAsync` for all side effects.

```csharp
public class MyOrchestrator
{
    // Orchestrators should NOT use injected services for I/O — delegate all work to activities.
    // Constructor injection is allowed only for ILogger (safe for replays).
    private readonly ILogger<MyOrchestrator> _logger;

    public MyOrchestrator(ILogger<MyOrchestrator> logger)
    {
        _logger = logger;
    }

    [Function(nameof(MyOrchestrator))]
    public async Task Run(
        [OrchestrationTrigger] TaskOrchestrationContext context,
        MyOrchestratorInput input)
    {
        _logger.LogInformation("Orchestrator started, batch size: {BatchSize}", input.BatchSize);

        // Sequential activity calls
        var preprocessResult = await context.CallActivityAsync<PreprocessResult>(
            nameof(PreprocessActivity), new PreprocessInput { BatchSize = input.BatchSize });

        // Fan-out / fan-in — parallel activity calls
        var tasks = new List<Task<ProcessResult>>();
        foreach (var chunk in preprocessResult.Chunks)
        {
            tasks.Add(context.CallActivityAsync<ProcessResult>(
                nameof(ProcessChunkActivity), new ProcessChunkInput { Chunk = chunk }));
        }

        var results = await Task.WhenAll(tasks);

        // Summarize
        await context.CallActivityAsync(
            nameof(SummarizeActivity), new SummarizeInput { Results = results });

        _logger.LogInformation("Orchestrator completed");
    }
}

public class MyOrchestratorInput
{
    public int BatchSize { get; set; }
}
```

### Activity

Activities have full DI access and can perform I/O freely.

```csharp
public class ProcessChunkActivity
{
    private readonly IMyRepository _repository;
    private readonly ILogger<ProcessChunkActivity> _logger;

    public ProcessChunkActivity(IMyRepository repository, ILogger<ProcessChunkActivity> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    [Function(nameof(ProcessChunkActivity))]
    public async Task<ProcessResult> Run([ActivityTrigger] ProcessChunkInput input)
    {
        _logger.LogInformation("Processing chunk of {Count} items", input.Chunk.Count);

        try
        {
            var processed = await _repository.ProcessChunkAsync(input.Chunk);
            return new ProcessResult { ProcessedCount = processed };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed processing chunk: {Message}", ex.Message);
            throw;
        }
    }
}

public class ProcessChunkInput
{
    public required List<MyItem> Chunk { get; set; }
}

public class ProcessResult
{
    public int ProcessedCount { get; set; }
}
```

### Chunked Batch Processing Pattern

Used when processing a large number of records in parallel batches (see `CsvDataOrchestrator`):

```csharp
[Function(nameof(BatchOrchestrator))]
public async Task Run(
    [OrchestrationTrigger] TaskOrchestrationContext context,
    BatchOrchestratorInput input)
{
    const int batchSize = 1000;
    var allItems = input.Items;

    for (int i = 0; i < allItems.Count; i += batchSize)
    {
        var chunk = allItems.Skip(i).Take(batchSize).ToList();
        try
        {
            await context.CallActivityAsync(nameof(ProcessBatchActivity),
                new ProcessBatchInput { Items = chunk });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Batch {Start}-{End} failed: {Message}", i, i + batchSize, ex.Message);
            // Continue with next batch — don't fail the whole orchestration
        }
    }
}
```

## MassTransit — Sending Commands via Queue

Inject `ISendEndpointProvider` to send to a named queue. Read queue name from env vars.

```csharp
private async Task SendCommandAsync(ISendEndpointProvider sendEndpointProvider, int id)
{
    var queueName = Environment.GetEnvironmentVariable("MyCommandQueueName")
        ?? throw new InvalidOperationException("MyCommandQueueName is not configured");

    var endpoint = await sendEndpointProvider.GetSendEndpoint(new Uri($"queue:{queueName}"));
    await endpoint.Send(new MyCommand { Id = id });

    _logger.LogInformation("Sent MyCommand for Id {Id} to queue {Queue}", id, queueName);
}
```

Inject `IPublishEndpoint` to publish events (fanout, no specific destination):

```csharp
await _publishEndpoint.PublishAsync(new MyEvent { Id = id });
```

## Cosmos DB — Query Patterns

FlyGuys uses a custom `CosmosDbContext` with repository-style accessors:

```csharp
// Get single item with SQL query
var item = (await _cosmosDbContext.Items
    .GetAllAsync("SELECT TOP 1 * FROM c WHERE c.IsActive = false ORDER BY c.CreatedAt ASC"))
    .FirstOrDefault();

// Upsert
await _cosmosDbContext.Items.UpsertAsync(item, new PartitionKey(item.Id));

// Patch individual fields (atomic, avoids full document replace)
var patches = new List<PatchOperation>
{
    PatchOperation.Set("/IsProcessing", true),
    PatchOperation.Set("/LastUpdated", DateTime.UtcNow),
    PatchOperation.Increment("/ProcessedCount", 1),
};
await _cosmosDbContext.Items.PatchAsync(item.Id, new PartitionKey(item.Id), patches);

// Delete
await _cosmosDbContext.Items.DeleteAsync(item.Id, new PartitionKey(item.Id));

// Count
var count = await _cosmosDbContext.Items
    .CountAsync("SELECT VALUE COUNT(1) FROM c WHERE c.fileName = 'foo.csv'");
```

## Error Handling Patterns

### Single Function — Try/Catch/Finally

```csharp
MyDocument? doc = null;
try
{
    doc = await FetchNextPendingDocument();
    if (doc == null) return;

    // Mark as in-flight before processing
    await MarkAsProcessing(doc.Id);
    await _service.ProcessAsync(doc);
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error processing document {Id}: {Message}", doc?.Id, ex.Message);

    // Persist error to Cosmos for observability
    await _cosmosDbContext.Errors.CreateAsync(
        new ErrorDocument { SourceId = doc?.Id, Message = ex.Message },
        new PartitionKey(doc?.Id ?? "unknown"));
}
finally
{
    // Always clean up — delete the in-flight marker even on failure
    if (doc != null)
        await _cosmosDbContext.Items.DeleteAsync(doc.Id, new PartitionKey(doc.Id));
}
```

### Orchestration — Continue on Partial Failure

Wrap individual activity calls in `try/catch` inside the orchestrator when one failure should not abort the entire batch:

```csharp
foreach (var item in items)
{
    try
    {
        await context.CallActivityAsync(nameof(ProcessItemActivity), item);
    }
    catch (Exception ex)
    {
        _logger.LogError("Item {Id} failed: {Message}", item.Id, ex.Message);
        // log and continue — don't re-throw
    }
}
```

## local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "AzureServiceBusConnectionString": "<your-service-bus-connection-string>",
    "CosmosDbConnectionString": "<your-cosmos-connection-string>",
    "CosmosDbDatabaseId": "my-database",
    "DbConnection": "<your-sql-connection-string>",
    "MyTimerExpression": "0 */5 * * * *"
  }
}
```

## Checklist — New Azure Function

- [ ] Uses isolated worker model (`Microsoft.Azure.Functions.Worker`)
- [ ] `Program.cs` validates all required env vars at startup
- [ ] Timer schedules are env-var-driven (`%EnvVarName%`), not hardcoded CRON strings
- [ ] Function name matches class name via `nameof()` or explicit string constant
- [ ] Constructor injection for all dependencies — no service locator
- [ ] Structured logging using `{PropertyName}` placeholders, not string interpolation
- [ ] `try/catch` in every `Run` method; durable activities re-throw on unexpected errors
- [ ] Durable orchestrators contain no I/O — all side effects delegated to activities
- [ ] `finally` block cleans up in-flight state markers (Cosmos, DB rows)
- [ ] `local.settings.json` populated for local dev, never committed with real secrets

## Additional Resources

- [Isolated Worker Process Guide](https://learn.microsoft.com/en-us/azure/azure-functions/dotnet-isolated-process-guide)
- [Durable Functions Overview](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)
- [Durable Functions Fan-out / Fan-in](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-cloud-backup)
- [Azure Functions C# Samples](https://learn.microsoft.com/en-us/samples/browse/?products=azure-functions&languages=csharp)
- [MassTransit Azure Service Bus](https://masstransit.io/documentation/transports/azure-service-bus)
