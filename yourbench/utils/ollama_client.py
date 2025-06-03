from __future__ import annotations
from types import SimpleNamespace
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import httpx


@dataclass
class AsyncOllamaClient:
    """Minimal async client for Ollama's OpenAI-compatible API."""

    base_url: str = "http://localhost:11434/v1"
    api_key: str | None = None
    timeout: float = 300
    headers: Dict[str, str] | None = None

    async def chat_completion(
        self,
        *,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload: Dict[str, Any] = {"model": model, "messages": messages}
        if temperature is not None:
            payload["temperature"] = temperature
        if seed is not None:
            payload["seed"] = seed

        req_headers = {"Content-Type": "application/json"}
        if self.headers:
            req_headers.update(self.headers)
        if self.api_key:
            req_headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload, headers=req_headers)
            response.raise_for_status()
            data = response.json()

        return SimpleNamespace(**data)
