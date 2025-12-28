from __future__ import annotations

from typing import Literal

from orchestrator.core.llm.base import LlmClient
from orchestrator.core.llm.fake import FakeLlmClient
from orchestrator.core.llm.ollama import OllamaLlmClient
from orchestrator.core.llm.openaiCompat import OpenAiCompatLlmClient


LlmType = Literal["fake", "ollama", "openai"]


class LlmFactory:
    @staticmethod
    def create(llmType: LlmType) -> LlmClient:
        if llmType == "fake":
            return FakeLlmClient()

        if llmType == "ollama":
            return OllamaLlmClient()

        if llmType == "openai":
            return OpenAiCompatLlmClient()

        raise ValueError(f"Unsupported LLM type: {llmType}")
