from __future__ import annotations

from dto.core.contracts import AgentResult, Artifact, ChatMessage, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import Agent


class ArchitectAgent(Agent):
    roleName = "Architect"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        system = ChatMessage(
            role="system",
            content=(
                "You are a Staff Software Architect. Produce architecture and decomposition."
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"ProjectId: {task.projectId}\n"
                f"Goal: {task.goal}\n"
                f"Context: {task.context}\n"
                f"Constraints: {task.constraints}\n"
                f"AcceptanceCriteria: {task.acceptanceCriteria}\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Architecture + decomposition",
            artifacts=[
                Artifact(
                    type="architecture",
                    description="Architecture proposal (text)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
