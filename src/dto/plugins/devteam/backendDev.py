from __future__ import annotations

from dto.core.contracts import AgentResult, Artifact, ChatMessage, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import Agent


class BackendDevAgent(Agent):
    roleName = "BackendDev"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        architectureText = ""

        for r in previous:
            for a in r.artifacts:
                if a.type == "architecture":
                    architectureText = a.payload.get("text", "")

        system = ChatMessage(
            role="system",
            content="You are a Senior Backend Developer. Produce implementation guidance.",
        )

        user = ChatMessage(
            role="user",
            content=(
                f"Goal: {task.goal}\n\n"
                f"Architecture:\n{architectureText}\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Implementation guidance",
            artifacts=[
                Artifact(
                    type="implementation",
                    description="Implementation proposal (text)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
