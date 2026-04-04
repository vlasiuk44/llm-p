import os
from pathlib import Path
from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    @staticmethod
    def _resolve_api_key() -> str:
        env_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if env_key:
            return env_key

        settings_key = settings.openrouter_api_key.strip()
        if settings_key:
            return settings_key

        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.split("=", 1)[1].strip()
        return ""

    async def chat_completion(
        self, *, messages: list[dict[str, str]], temperature: float = 0.7
    ) -> str:
        api_key = self._resolve_api_key()
        if not api_key:
            raise ExternalServiceError("OPENROUTER_API_KEY is not configured")

        url = f"{settings.openrouter_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 400:
            raise ExternalServiceError(f"OpenRouter error {response.status_code}: {response.text}")

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ExternalServiceError("OpenRouter returned unexpected response format") from exc
