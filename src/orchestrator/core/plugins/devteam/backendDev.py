from __future__ import annotations

from orchestrator.core.contracts import AgentResult, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent


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
            content=(
                "You are a Senior Backend Developer. "
                "You propose implementation details and concrete next steps. "
                "If code changes are needed, provide patch-like guidance."
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"Goal: {task.goal}\n\n"
                "Architecture from Architect:\n"
                f"{architectureText}\n\n"
                "Deliver:\n"
                "1) Implementation plan per module\n"
                "2) Key interfaces / API shape\n"
                "3) Test strategy suggestions\n"
                "4) If possible: draft diffs or file skeletons\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Produced implementation plan and code skeleton guidance",
            artifacts=[
                {
                    "type": "implementation",
                    "description": "Implementation plan + file skeletons",
                    "payload": {
                        "text": text,
                    },
                }
            ],
        )
