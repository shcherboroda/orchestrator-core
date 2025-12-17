from __future__ import annotations

from dto.core.contracts import AgentResult, Artifact, ChatMessage, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import Agent


class QaAgent(Agent):
    roleName = "QA"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        implText = ""

        for r in previous:
            for a in r.artifacts:
                if a.type == "implementation":
                    implText = a.payload.get("text", "")

        system = ChatMessage(
            role="system",
            content="You are a QA engineer. Produce a test plan and edge cases.",
        )

        user = ChatMessage(
            role="user",
            content=(
                f"Goal: {task.goal}\n\n"
                f"Implementation:\n{implText}\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Test plan and edge cases",
            artifacts=[
                Artifact(
                    type="qaPlan",
                    description="QA plan (text)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
