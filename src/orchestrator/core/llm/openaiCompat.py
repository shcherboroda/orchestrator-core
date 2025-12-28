from __future__ import annotations

import os
import httpx

from orchestrator.core.contracts import ChatMessage
from orchestrator.core.llm.base import LlmClient


class OpenAiCompatLlmClient(LlmClient):
    def __init__(self) -> None:
        self.baseUrl = os.getenv("DTOllmBaseUrl", "https://api.openai.com").rstrip("/")
        self.apiKey = os.getenv("DTOllmApiKey", "")
        self.model = os.getenv("DTOllmModel", "gpt-4.1-mini")

        if self.apiKey.strip() == "":
            raise RuntimeError(
                "DTOllmApiKey is not set. "
                "Put it into .env to use --llm openai"
            )

    async def chat(self, messages: list[ChatMessage]) -> str:
        url = f"{self.baseUrl}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                }
                for m in messages
            ],
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.apiKey}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
            )

            if response.status_code >= 400:
                raise RuntimeError(
                    f"LLM request failed: {response.status_code} {response.text}"
                )

            data = response.json()

        return data["choices"][0]["message"]["content"]
