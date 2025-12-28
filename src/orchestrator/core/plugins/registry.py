from __future__ import annotations

from typing import Callable
from orchestrator.core.contracts import AgentResult, Task
from orchestrator.core.llm.base import LlmClient


class Agent:
    roleName: str

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        raise NotImplementedError


AgentFactory = Callable[[], Agent]


class PluginRegistry:
    def __init__(self) -> None:
        self.factories: dict[str, AgentFactory] = {}

    def register(self, roleName: str, factory: AgentFactory) -> None:
        self.factories[roleName] = factory

    def create(self, roleName: str) -> Agent:
        if roleName not in self.factories:
            raise KeyError(f"Role not registered: {roleName}")

        return self.factories[roleName]()
