from __future__ import annotations

from dto.core.contracts import AgentResult, Artifact, ChatMessage, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import Agent


class ConsolidatorAgent(Agent):
    roleName = "Consolidator"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        joined = ""

        for r in previous:
            joined += f"\n\n=== {r.agentRole} ===\n"
            for a in r.artifacts:
                joined += f"[{a.type}] {a.description}\n"
                joined += f"{a.payload.get('text', '')}\n"

        system = ChatMessage(
            role="system",
            content="You are a Tech Lead. Consolidate into a final actionable plan.",
        )

        user = ChatMessage(
            role="user",
            content=(
                f"ProjectId: {task.projectId}\n"
                f"Goal: {task.goal}\n\n"
                f"Inputs:{joined}\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Consolidated final plan",
            artifacts=[
                Artifact(
                    type="finalPlan",
                    description="Final consolidated plan (text)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
