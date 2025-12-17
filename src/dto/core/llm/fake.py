from __future__ import annotations

import hashlib
from dto.core.contracts import ChatMessage
from dto.core.llm.base import LlmClient


class FakeLlmClient(LlmClient):
    def __init__(self) -> None:
        self.counter = 0

    async def chat(self, messages: list[ChatMessage]) -> str:
        self.counter += 1

        joined = "\n".join([f"{m.role}:{m.content}" for m in messages])
        digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]

        return (
            "FAKE_LLM_OUTPUT\n"
            f"call={self.counter}\n"
            f"digest={digest}\n"
            "notes=This is a deterministic stub. Replace with a real LLM adapter.\n"
        )
