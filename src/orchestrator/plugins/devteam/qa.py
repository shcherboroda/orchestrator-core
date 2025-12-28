from __future__ import annotations

from orchestrator.core.contracts import AgentResult, Artifact, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent
from orchestrator.plugins.devteam.prompt import buildCommonHeader, findArtifactText


class QaAgent(Agent):
    roleName = "QA"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        architectureText = findArtifactText(previous, "architecture")
        implText = findArtifactText(previous, "implementation")
        header = buildCommonHeader(task)

        system = ChatMessage(
            role="system",
            content=(
                "You are a QA engineer.\n"
                "Your job: produce a practical v0 test plan (E2E scenarios + edge cases) for AOProof.\n"
                "Keep it concise and executable.\n"
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"{header}\n"
                "\n"
                "Architect output:\n"
                f"{architectureText}\n"
                "\n"
                "Backend output:\n"
                f"{implText}\n"
                "\n"
                "Deliverable format (Markdown, max ~120 lines):\n"
                "1) E2E scenarios (verify -> claim -> transfer -> proof)\n"
                "2) Negative cases (expired/revoked links, lost/stolen, auth failures)\n"
                "3) API contract checks (status codes, invariants)\n"
                "4) Minimal automation suggestions (what to cover first)\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="QA v0 plan",
            artifacts=[
                Artifact(
                    type="qaPlan",
                    description="QA plan (structured markdown)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
