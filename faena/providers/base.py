"""
Base classes and interfaces for Faena Multi-Provider LLM abstraction.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema dictionary

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    call_id: str
    name: str
    content: str
    is_error: bool = False


@dataclass
class Message:
    role: Role
    content: str = ""
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)


@dataclass
class LLMResponse:
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, int]] = None

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


class LLMProvider(ABC):
    """Abstract base class for all LLM providers (Claude, OpenAI, Gemini, Ollama, etc.)."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider, e.g. 'anthropic', 'openai', 'gemini'."""
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model used when none is provided."""
        pass

    def get_model(self) -> str:
        return self.model or self.default_model

    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """
        Generates a response from the LLM, optionally handling tool calling.
        """
        pass
