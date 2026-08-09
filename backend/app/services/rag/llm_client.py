"""Thin wrapper around the OpenRouter chat completions API (OpenAI-compatible).

Kept as the single place that knows about OpenRouter, so switching provider
or model later only touches this file.
"""

import json
from collections.abc import AsyncGenerator

import httpx

from app.core.config import get_settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMError(Exception):
    """Raised when the LLM call fails or returns something unexpected."""


async def call_llm(messages: list[dict[str, str]]) -> str:
    settings = get_settings()

    if not settings.openrouter_api_key:
        raise LLMError(
            "OPENROUTER_API_KEY is not set in .env — get a free key at "
            "openrouter.ai/keys."
        )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.llm_model_name,
                "temperature": settings.llm_temperature,
                "messages": messages,
            },
        )

    if response.status_code != 200:
        raise LLMError(
            f"OpenRouter request failed ({response.status_code}): "
            f"{response.text[:300]}"
        )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise LLMError(f"Unexpected OpenRouter response shape: {data}") from exc


async def stream_llm(messages: list[dict[str, str]]) -> AsyncGenerator[str, None]:
    """Same call as call_llm, but yields text chunks as they arrive instead
    of waiting for the full response — used to power the typing effect in
    the chat widget."""
    settings = get_settings()

    if not settings.openrouter_api_key:
        raise LLMError(
            "OPENROUTER_API_KEY is not set in .env — get a free key at "
            "openrouter.ai/keys."
        )

    async with httpx.AsyncClient(timeout=60) as client, client.stream(
        "POST",
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.llm_model_name,
            "temperature": settings.llm_temperature,
            "messages": messages,
            "stream": True,
        },
    ) as response:
        if response.status_code != 200:
            body = await response.aread()
            raise LLMError(
                f"OpenRouter request failed ({response.status_code}): "
                f"{body[:300]!r}"
            )

        async for line in response.aiter_lines():
            if not line or not line.startswith("data: "):
                continue

            payload = line[len("data: ") :].strip()
            if payload == "[DONE]":
                break

            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue

            delta = chunk.get("choices", [{}])[0].get("delta", {})
            content = delta.get("content")
            if content:
                yield content
