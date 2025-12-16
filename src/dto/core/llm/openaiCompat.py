from __future__ import annotations

import os
import httpx
from dto.core.contracts import ChatMessage
from dto.core.llm.base import LlmClient


class OpenAiCompatLlmClient(LlmClient):
    def __init__(self) -> None:
        self.baseUrl = os.getenv("DTOllmBaseUrl", "https://api.openai.com").rstrip("/")
        self.apiKey = os.getenv("DTOllmApiKey", "")
        self.model = os.getenv("DTOllmModel", "gpt-4.1-mini")

        if self.apiKey.strip() == "":
            raise RuntimeError("DTOllmApiKey is empty. Put it into .env")

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
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
