"""
Universal Multi-Provider LLM abstraction package.
"""
from faena.providers.base import (
    LLMProvider,
    Message,
    Role,
    ToolCall,
    ToolDefinition,
    ToolResult,
    LLMResponse,
)
from faena.providers.anthropic import AnthropicProvider
from faena.providers.openai_provider import OpenAIProvider
from faena.providers.gemini import GeminiProvider
from faena.providers.generic import (
    GenericOpenAICompatibleProvider,
    OllamaProvider,
    OpenRouterProvider,
    DeepSeekProvider,
)
from faena.providers.factory import (
    create_provider,
    auto_detect_provider,
    list_providers_status,
    get_api_key_for_provider,
)

__all__ = [
    "LLMProvider",
    "Message",
    "Role",
    "ToolCall",
    "ToolDefinition",
    "ToolResult",
    "LLMResponse",
    "AnthropicProvider",
    "OpenAIProvider",
    "GeminiProvider",
    "GenericOpenAICompatibleProvider",
    "OllamaProvider",
    "OpenRouterProvider",
    "DeepSeekProvider",
    "create_provider",
    "auto_detect_provider",
    "list_providers_status",
    "get_api_key_for_provider",
]
