"""
Anthropic (Claude) provider implementation using standard library HTTP client.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional
from faena.providers.base import LLMProvider, Message, Role, ToolCall, ToolDefinition, ToolResult, LLMResponse


class AnthropicProvider(LLMProvider):
    """
    Provider for Anthropic models (Claude 3.5 Sonnet, Claude 3.7 Sonnet, Haiku, Opus).
    Uses direct HTTPS calls so no external SDK installation is required.
    """

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def default_model(self) -> str:
        return "claude-3-7-sonnet-latest"

    def _format_tools(self, tools: List[ToolDefinition]) -> List[Dict[str, Any]]:
        formatted = []
        for t in tools:
            formatted.append({
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters,
            })
        return formatted

    def _format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        formatted: List[Dict[str, Any]] = []

        for msg in messages:
            if msg.role == Role.SYSTEM:
                continue  # System prompt is passed at top level in Anthropic API

            content_blocks: List[Dict[str, Any]] = []

            # Add text content if present
            if msg.content:
                content_blocks.append({"type": "text", "text": msg.content})

            # Add tool calls (assistant message)
            for tc in msg.tool_calls:
                content_blocks.append({
                    "type": "tool_use",
                    "id": tc.id,
                    "name": tc.name,
                    "input": tc.arguments,
                })

            # Add tool results (user message replying to tool_use)
            for tr in msg.tool_results:
                content_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": tr.call_id,
                    "content": tr.content,
                    "is_error": tr.is_error,
                })

            role_str = "user" if msg.role in (Role.USER, Role.TOOL) else "assistant"

            # Merge consecutive messages of the same role if necessary
            if formatted and formatted[-1]["role"] == role_str:
                formatted[-1]["content"].extend(content_blocks)
            else:
                formatted.append({
                    "role": role_str,
                    "content": content_blocks if content_blocks else [{"type": "text", "text": ""}],
                })

        return formatted

    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable.")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        # Extract system prompt if in messages
        sys_text = system_prompt or ""
        for m in messages:
            if m.role == Role.SYSTEM and m.content:
                sys_text = f"{sys_text}\n{m.content}".strip()

        payload: Dict[str, Any] = {
            "model": self.get_model(),
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": self._format_messages(messages),
        }

        if sys_text:
            payload["system"] = sys_text

        if tools:
            payload["tools"] = self._format_tools(tools)

        req_body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Anthropic API error (HTTP {e.code}): {error_body}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with Anthropic API: {e}") from e

        content_parts = []
        tool_calls: List[ToolCall] = []

        for block in data.get("content", []):
            if block.get("type") == "text":
                content_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.get("id", ""),
                        name=block.get("name", ""),
                        arguments=block.get("input", {}),
                    )
                )

        usage = data.get("usage", {})

        return LLMResponse(
            content="\n".join(content_parts),
            tool_calls=tool_calls,
            raw_response=data,
            usage={
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
            },
        )
