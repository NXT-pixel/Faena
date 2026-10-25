"""
OpenAI (ChatGPT) provider implementation using standard library HTTP client.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional
from faena.providers.base import LLMProvider, Message, Role, ToolCall, ToolDefinition, ToolResult, LLMResponse


class OpenAIProvider(LLMProvider):
    """
    Provider for OpenAI models (GPT-4o, GPT-4o-mini, o3-mini, etc.).
    Uses direct HTTPS calls so no external SDK installation is required.
    """

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return "gpt-4o"

    def _get_api_url(self) -> str:
        base = (self.base_url or "https://api.openai.com/v1").rstrip("/")
        return f"{base}/chat/completions"

    def _format_tools(self, tools: List[ToolDefinition]) -> List[Dict[str, Any]]:
        formatted = []
        for t in tools:
            formatted.append({
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            })
        return formatted

    def _format_messages(self, messages: List[Message], system_prompt: Optional[str] = None) -> List[Dict[str, Any]]:
        formatted: List[Dict[str, Any]] = []

        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})

        for msg in messages:
            if msg.role == Role.SYSTEM:
                formatted.append({"role": "system", "content": msg.content})
            elif msg.role == Role.USER:
                formatted.append({"role": "user", "content": msg.content})
            elif msg.role == Role.ASSISTANT:
                item: Dict[str, Any] = {"role": "assistant"}
                if msg.content:
                    item["content"] = msg.content
                if msg.tool_calls:
                    item["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments),
                            },
                        }
                        for tc in msg.tool_calls
                    ]
                formatted.append(item)
            elif msg.role == Role.TOOL:
                for tr in msg.tool_results:
                    formatted.append({
                        "role": "tool",
                        "tool_call_id": tr.call_id,
                        "content": tr.content,
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
        if not self.api_key and not self.base_url:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        url = self._get_api_url()
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: Dict[str, Any] = {
            "model": self.get_model(),
            "messages": self._format_messages(messages, system_prompt),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            payload["tools"] = self._format_tools(tools)
            payload["tool_choice"] = "auto"

        req_body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API error (HTTP {e.code}): {error_body}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with OpenAI API: {e}") from e

        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content") or ""

        tool_calls: List[ToolCall] = []
        raw_tool_calls = message.get("tool_calls", [])
        for tc in raw_tool_calls:
            func = tc.get("function", {})
            raw_args = func.get("arguments", "{}")
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args)
                except Exception:
                    args = {"raw": raw_args}
            else:
                args = raw_args or {}

            tool_calls.append(
                ToolCall(
                    id=tc.get("id", ""),
                    name=func.get("name", ""),
                    arguments=args,
                )
            )

        usage = data.get("usage", {})

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            raw_response=data,
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )
