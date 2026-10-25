"""
Google Gemini provider implementation using standard library HTTP client.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
import uuid
from typing import Any, Dict, List, Optional
from faena.providers.base import LLMProvider, Message, Role, ToolCall, ToolDefinition, ToolResult, LLMResponse


class GeminiProvider(LLMProvider):
    """
    Provider for Google Gemini models (gemini-2.5-flash, gemini-2.5-pro, gemini-3.8-flash, etc.).
    Uses direct HTTPS REST calls so no external SDK installation is required.
    """

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return "gemini-2.5-flash"

    def _format_tools(self, tools: List[ToolDefinition]) -> List[Dict[str, Any]]:
        declarations = []
        for t in tools:
            declarations.append({
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            })
        return [{"functionDeclarations": declarations}]

    def _format_contents(self, messages: List[Message]) -> List[Dict[str, Any]]:
        contents: List[Dict[str, Any]] = []

        for msg in messages:
            if msg.role == Role.SYSTEM:
                continue

            parts: List[Dict[str, Any]] = []

            if msg.content:
                parts.append({"text": msg.content})

            for tc in msg.tool_calls:
                parts.append({
                    "functionCall": {
                        "name": tc.name,
                        "args": tc.arguments,
                    }
                })

            for tr in msg.tool_results:
                parts.append({
                    "functionResponse": {
                        "name": tr.name,
                        "response": {
                            "output": tr.content,
                            "is_error": tr.is_error,
                        },
                    }
                })

            role_str = "model" if msg.role == Role.ASSISTANT else "user"

            if parts:
                contents.append({
                    "role": role_str,
                    "parts": parts,
                })

        return contents

    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[ToolDefinition]] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")

        model = self.get_model()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json",
        }

        # Collect system prompt
        sys_text = system_prompt or ""
        for m in messages:
            if m.role == Role.SYSTEM and m.content:
                sys_text = f"{sys_text}\n{m.content}".strip()

        payload: Dict[str, Any] = {
            "contents": self._format_contents(messages),
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        if sys_text:
            payload["systemInstruction"] = {
                "parts": [{"text": sys_text}]
            }

        if tools:
            payload["tools"] = self._format_tools(tools)

        req_body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Gemini API error (HTTP {e.code}): {error_body}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with Gemini API: {e}") from e

        content_parts = []
        tool_calls: List[ToolCall] = []

        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for p in parts:
                if "text" in p:
                    content_parts.append(p["text"])
                elif "functionCall" in p:
                    fc = p["functionCall"]
                    tool_calls.append(
                        ToolCall(
                            id=str(uuid.uuid4())[:8],
                            name=fc.get("name", ""),
                            arguments=fc.get("args", {}),
                        )
                    )

        usage_meta = data.get("usageMetadata", {})

        return LLMResponse(
            content="\n".join(content_parts),
            tool_calls=tool_calls,
            raw_response=data,
            usage={
                "prompt_tokens": usage_meta.get("promptTokenCount", 0),
                "completion_tokens": usage_meta.get("candidatesTokenCount", 0),
            },
        )
