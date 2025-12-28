from __future__ import annotations

import os
import asyncio
import httpx

from orchestrator.core.contracts import ChatMessage
from orchestrator.core.llm.base import LlmClient


class OllamaLlmClient(LlmClient):
    def __init__(self) -> None:
        self.baseUrl = os.getenv("DTOollamaBaseUrl", "http://127.0.0.1:11434").rstrip("/")
        self.model = os.getenv("DTOollamaModel", "qwen2.5:3b")

        self.numThreads = int(os.getenv("DTOollamaNumThreads", "4"))
        self.maxTokens = int(os.getenv("DTOollamaMaxTokens", "400"))
        self.temperature = float(os.getenv("DTOollamaTemperature", "0.2"))

        self.timeoutSec = float(os.getenv("DTOollamaTimeoutSec", "600"))
        self.retries = int(os.getenv("DTOollamaRetries", "2"))

    async def chat(self, messages: list[ChatMessage]) -> str:
        url = f"{self.baseUrl}/api/chat"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                }
                for m in messages
            ],
            "stream": False,
            "options": {
                "num_thread": self.numThreads,
                "num_predict": self.maxTokens,
                "temperature": self.temperature,
            },
        }

        timeout = httpx.Timeout(
            timeout=self.timeoutSec,
        )

        lastError: Exception | None = None

        for attempt in range(self.retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(
                        url,
                        json=payload,
                    )

                if response.status_code >= 400:
                    raise RuntimeError(
                        f"Ollama request failed: {response.status_code} {response.text}"
                    )

                data = response.json()
                content = data.get("message", {}).get("content", "")

                return content

            except (httpx.ReadTimeout, httpx.RemoteProtocolError) as e:
                lastError = e

                if attempt >= self.retries:
                    break

                await asyncio.sleep(1.0 * (attempt + 1))

        raise RuntimeError(
            "Ollama request timed out. "
            f"model={self.model} timeoutSec={self.timeoutSec} retries={self.retries}. "
            "Try reducing DTOollamaMaxTokens or increasing DTOollamaTimeoutSec."
        ) from lastError
