import json
from abc import ABC, abstractmethod
from typing import Any

import httpx

from app.core.config import get_settings


class LLMProvider(ABC):
    @abstractmethod
    async def generate_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    async def generate_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        return {}


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                    "options": {"temperature": 0.25},
                },
            )
            response.raise_for_status()
        text = response.json().get("response", "{}")
        return _loads_json(text)


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def generate_json(self, prompt: str, schema_hint: str | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.25,
                },
            )
            response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]
        return _loads_json(text)


def _loads_json(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider == "ollama":
        return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
    if provider == "openai_compatible":
        if not (
            settings.openai_compatible_base_url
            and settings.openai_compatible_api_key
            and settings.openai_compatible_model
        ):
            return MockLLMProvider()
        return OpenAICompatibleProvider(
            settings.openai_compatible_base_url,
            settings.openai_compatible_api_key,
            settings.openai_compatible_model,
        )
    return MockLLMProvider()
