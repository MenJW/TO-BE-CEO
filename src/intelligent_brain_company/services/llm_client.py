from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from intelligent_brain_company.config import AppConfig


def _strip_code_fences(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return text


@dataclass(slots=True)
class LLMClient:
    api_key: str
    base_url: str
    model: str
    timeout_seconds: int = 45

    @classmethod
    def from_config(cls, config: AppConfig) -> "LLMClient | None":
        if not config.llm_enabled:
            return None
        return cls(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url,
            model=config.llm_model,
            timeout_seconds=config.llm_timeout_seconds,
        )

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
    ) -> dict[str, Any] | None:
        payload = {
            "model": self.model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        endpoint = self.base_url.rstrip("/") + "/chat/completions"
        req = request.Request(
            endpoint,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except (TimeoutError, error.URLError, error.HTTPError, json.JSONDecodeError):
            return None

        try:
            data = json.loads(raw)
            content = data["choices"][0]["message"]["content"]
            return json.loads(_strip_code_fences(content))
        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            return None