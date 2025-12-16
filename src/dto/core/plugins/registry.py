from __future__ import annotations

from typing import Callable
from dto.core.contracts import Task, AgentResult
from dto.core.llm.base import LlmClient


AgentFactory = Callable[[], "Agent"]


class Agent:
    roleName: str

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        raise NotImplementedError


class PluginRegistry:
    def __init__(self) -> None:
        self.factories: dict[str, AgentFactory] = {}

    def register(self, roleName: str, factory: AgentFactory) -> None:
        self.factories[roleName] = factory

    def create(self, roleName: str) -> Agent:
        if roleName not in self.factories:
            raise KeyError(f"Role not registered: {roleName}")

        return self.factories[roleName]()
