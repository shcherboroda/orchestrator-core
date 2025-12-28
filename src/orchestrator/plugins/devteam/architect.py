from __future__ import annotations

from orchestrator.core.contracts import AgentResult, Artifact, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent
from orchestrator.plugins.devteam.prompt import buildCommonHeader


class ArchitectAgent(Agent):
    roleName = "Architect"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        system = ChatMessage(
            role="system",
            content=(
                "You are a Staff Software Architect.\n"
                "Your job: produce a short, actionable v0 completion plan strictly for THIS project.\n"
                "Output must be concise and structured.\n"
            ),
        )

        header = buildCommonHeader(task)

        user = ChatMessage(
            role="user",
            content=(
                f"{header}\n"
                "\n"
                "Deliverable format (Markdown, max ~80 lines):\n"
                "1) What is broken / missing (from context)\n"
                "2) v0 Milestones (3-6)\n"
                "3) Work packages (API / Consumer Web / Brand Web / SDK / DB)\n"
                "4) Critical dependencies and risks\n"
                "5) Questions (only if needed)\n"
                "\n"
                "Important: reference real paths like /root/aoproof/apps/... and /root/aoproof/packages/...\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="AOProof v0 architecture + decomposition",
            artifacts=[
                Artifact(
                    type="architecture",
                    description="AOProof v0 plan (structured markdown)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
