"""
Factory and discovery mechanism for LLM Providers.
"""
from __future__ import annotations
import os
from typing import Dict, List, Optional, Tuple, Type
from faena.providers.base import LLMProvider
from faena.providers.anthropic import AnthropicProvider
from faena.providers.openai_provider import OpenAIProvider
from faena.providers.gemini import GeminiProvider
from faena.providers.generic import (
    GenericOpenAICompatibleProvider,
    OllamaProvider,
    OpenRouterProvider,
    DeepSeekProvider,
)


PROVIDER_REGISTRY: Dict[str, Type[LLMProvider]] = {
    "anthropic": AnthropicProvider,
    "claude": AnthropicProvider,
    "openai": OpenAIProvider,
    "chatgpt": OpenAIProvider,
    "gemini": GeminiProvider,
    "google": GeminiProvider,
    "ollama": OllamaProvider,
    "openrouter": OpenRouterProvider,
    "deepseek": DeepSeekProvider,
    "custom": GenericOpenAICompatibleProvider,
}


def get_api_key_for_provider(provider_name: str) -> Optional[str]:
    name = provider_name.lower()
    if name in ("anthropic", "claude"):
        return os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
    elif name in ("openai", "chatgpt"):
        return os.environ.get("OPENAI_API_KEY")
    elif name in ("gemini", "google"):
        return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    elif name == "openrouter":
        return os.environ.get("OPENROUTER_API_KEY")
    elif name == "deepseek":
        return os.environ.get("DEEPSEEK_API_KEY")
    elif name == "ollama":
        return "ollama"
    return os.environ.get("FAENA_API_KEY")


def create_provider(
    name: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMProvider:
    provider_name = (name or os.environ.get("FAENA_PROVIDER") or "").strip().lower()

    if not provider_name:
        # Auto-detect based on available keys
        detected = auto_detect_provider()
        if not detected:
            raise ValueError(
                "No LLM provider configured or detected. "
                "Please set one of ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, "
                "or specify --provider and provide the API key."
            )
        provider_name = detected

    provider_cls = PROVIDER_REGISTRY.get(provider_name)
    if not provider_cls:
        available = ", ".join(sorted(set(PROVIDER_REGISTRY.keys())))
        raise ValueError(f"Unknown provider '{provider_name}'. Supported providers: {available}")

    key = api_key or get_api_key_for_provider(provider_name)
    selected_model = model or os.environ.get("FAENA_MODEL")

    if provider_name == "ollama":
        return OllamaProvider(model=selected_model, base_url=base_url)
    elif provider_name == "openrouter":
        return OpenRouterProvider(api_key=key, model=selected_model)
    elif provider_name == "deepseek":
        return DeepSeekProvider(api_key=key, model=selected_model)
    elif provider_name == "custom":
        return GenericOpenAICompatibleProvider(
            api_key=key, model=selected_model, base_url=base_url or os.environ.get("FAENA_BASE_URL")
        )
    else:
        return provider_cls(api_key=key, model=selected_model, base_url=base_url)


def auto_detect_provider() -> Optional[str]:
    """Auto-detect the first available provider with credentials set."""
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY"):
        return "claude"
    if os.environ.get("OPENAI_API_KEY"):
        return "chatgpt"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("DEEPSEEK_API_KEY"):
        return "deepseek"
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    return None


def list_providers_status() -> List[Tuple[str, str, bool]]:
    """Returns a list of (display_name, internal_name, is_available)."""
    checks = [
        ("Anthropic Claude", "claude", bool(get_api_key_for_provider("claude"))),
        ("OpenAI ChatGPT", "chatgpt", bool(get_api_key_for_provider("chatgpt"))),
        ("Google Gemini", "gemini", bool(get_api_key_for_provider("gemini"))),
        ("DeepSeek", "deepseek", bool(get_api_key_for_provider("deepseek"))),
        ("OpenRouter", "openrouter", bool(get_api_key_for_provider("openrouter"))),
        ("Ollama (Local)", "ollama", True),
    ]
    return checks
