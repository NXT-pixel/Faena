---
description: Python Microsoft Agent Framework + Azure Functions conventions
globs: "**/function_app.py"
alwaysApply: false
---

# Python MAF + Azure Functions

When editing the Azure Functions app entrypoint for Microsoft Agent Framework (Python):

- Use `agent_framework.azure`: `AgentFunctionApp`, `AzureOpenAIChatClient`. Create the client with `endpoint`, `deployment_name`, and `credential` (e.g. `DefaultAzureCredential()` or `AzureCliCredential()`).
- Create agents with `.as_agent(name="...", instructions="...")`. Register them with `AgentFunctionApp(agents=[...])`.
- Read endpoint and deployment from environment variables (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` or `AZURE_OPENAI_DEPLOYMENT_NAME`). Use `load_dotenv()` if you rely on a `.env` file.
- Optionally set `enable_health_check=True` and `max_poll_retries=50` on `AgentFunctionApp` when needed.
- Prefer a small factory (e.g. `_create_agent()`) that returns the agent, then `app = AgentFunctionApp(agents=[_create_agent()])`.

For full patterns, tools, durable state, and multi-agent/workflow samples, use the **python-maf-azurefunctions** coding agent (documentation and best-practices in `agents/coding/python-maf-azurefunctions/`).

