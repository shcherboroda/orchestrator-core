from __future__ import annotations

from orchestrator.core.contracts import AgentResult, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent


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
            content=(
                "You are a pragmatic QA engineer. "
                "You focus on edge cases, test plan, failure modes, and acceptance criteria coverage."
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"Goal: {task.goal}\n\n"
                "Implementation notes:\n"
                f"{implText}\n\n"
                "Deliver:\n"
                "1) Test plan (unit/integration/e2e)\n"
                "2) Edge cases\n"
                "3) Non-functional checks (security/perf/reliability)\n"
                "4) Questions / missing requirements\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Produced QA test plan and risk checklist",
            artifacts=[
                {
                    "type": "qaPlan",
                    "description": "Test plan + edge cases",
                    "payload": {
                        "text": text,
                    },
                }
            ],
        )
