from __future__ import annotations

from dto.core.contracts import AgentResult, ChatMessage, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import Agent


class ConsolidatorAgent(Agent):
    roleName = "Consolidator"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        system = ChatMessage(
            role="system",
            content=(
                "You are a Tech Lead consolidator. "
                "You combine outputs into a single actionable plan with clear next steps."
            ),
        )

        joined = ""
        for r in previous:
            joined += f"\n\n=== {r.agentRole} ===\n"
            for a in r.artifacts:
                joined += f"\n[{a.type}] {a.description}\n{a.payload.get('text','')}\n"

        user = ChatMessage(
            role="user",
            content=(
                f"Project: {task.projectId}\n"
                f"Goal: {task.goal}\n\n"
                "Inputs:\n"
                f"{joined}\n\n"
                "Deliver final:\n"
                "1) Consolidated plan with milestones\n"
                "2) Clear task list (as bullet points)\n"
                "3) Risks and mitigations\n"
                "4) What to do first in the next 2 hours\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Consolidated outputs",
            artifacts=[
                {
                    "type": "finalPlan",
                    "description": "Consolidated plan",
                    "payload": {
                        "text": text,
                    },
                }
            ],
        )
