from __future__ import annotations

from orchestrator.core.contracts import AgentResult, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent


class ArchitectAgent(Agent):
    roleName = "Architect"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        system = ChatMessage(
            role="system",
            content=(
                "You are a Staff Software Architect. "
                "You produce architecture and decomposition. "
                "Be concrete, propose components, interfaces, risks, and a plan."
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"ProjectId: {task.projectId}\n"
                f"Goal: {task.goal}\n"
                f"Context: {task.context}\n"
                f"Constraints: {task.constraints}\n"
                f"AcceptanceCriteria: {task.acceptanceCriteria}\n\n"
                "Deliver:\n"
                "1) High-level architecture\n"
                "2) Milestones\n"
                "3) Suggested repo changes\n"
                "4) Risks\n"
                "5) Open questions\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Produced architecture and decomposition",
            artifacts=[
                {
                    "type": "architecture",
                    "description": "Architecture + milestones + risks",
                    "payload": {
                        "text": text,
                    },
                }
            ],
        )
