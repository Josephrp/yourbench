"""Simple async client for vLLM's OpenAI-compatible API."""

from __future__ import annotations
import json
import asyncio
import urllib.request
from typing import Any, Dict, List, Optional


async def chat_completion(
    base_url: str,
    api_key: Optional[str],
    model: str,
    messages: List[Dict[str, Any]],
    temperature: Optional[float] = None,
    timeout: int = 300,
    request_id: Optional[str] = None,
) -> str:
    """Query a vLLM server's `/chat/completions` endpoint."""

    url = base_url.rstrip("/") + "/chat/completions"

    payload: Dict[str, Any] = {"model": model, "messages": messages}
    if temperature is not None:
        payload["temperature"] = temperature

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if request_id:
        headers["X-Request-ID"] = request_id

    data = json.dumps(payload).encode("utf-8")

    def _post() -> str:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
        choices = resp_data.get("choices")
        if not choices:
            raise RuntimeError("Empty response from vLLM server")
        return choices[0]["message"]["content"]

    return await asyncio.to_thread(_post)
