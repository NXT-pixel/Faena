"""
Generic OpenAI-Compatible provider for Ollama, OpenRouter, DeepSeek, LocalAI, vLLM.
"""
from __future__ import annotations
from typing import Optional
from faena.providers.openai_provider import OpenAIProvider


class GenericOpenAICompatibleProvider(OpenAIProvider):
    """
    Provider for any OpenAI-compatible API endpoint.
    Supports Ollama, OpenRouter, DeepSeek, Groq, LiteLLM, vLLM, etc.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        name: str = "generic_openai",
        default_model: str = "default",
    ):
        super().__init__(api_key=api_key or "sk-no-key-required", model=model, base_url=base_url)
        self._custom_name = name
        self._default_model = default_model

    @property
    def provider_name(self) -> str:
        return self._custom_name

    @property
    def default_model(self) -> str:
        return self._default_model


class OllamaProvider(GenericOpenAICompatibleProvider):
    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None, **kwargs):
        super().__init__(
            api_key="ollama",
            model=model,
            base_url=base_url or "http://localhost:11434/v1",
            name="ollama",
            default_model="llama3.1",
        )


class OpenRouterProvider(GenericOpenAICompatibleProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url="https://openrouter.ai/api/v1",
            name="openrouter",
            default_model="anthropic/claude-3.7-sonnet",
        )


class DeepSeekProvider(GenericOpenAICompatibleProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url="https://api.deepseek.com/v1",
            name="deepseek",
            default_model="deepseek-chat",
        )
