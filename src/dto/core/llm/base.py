from __future__ import annotations

from abc import ABC, abstractmethod
from dto.core.contracts import ChatMessage


class LlmClient(ABC):
    @abstractmethod
    async def chat(self, messages: list[ChatMessage]) -> str:
        raise NotImplementedError
