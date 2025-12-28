from __future__ import annotations

from orchestrator.core.contracts import AgentResult, Artifact, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent
from orchestrator.plugins.devteam.prompt import buildCommonHeader, findArtifactText


class BackendDevAgent(Agent):
    roleName = "BackendDev"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        architectureText = findArtifactText(previous, "architecture")
        header = buildCommonHeader(task)

        system = ChatMessage(
            role="system",
            content=(
                "You are a Senior Backend Developer (Fastify + PostgreSQL).\n"
                "Your job: produce an implementation-focused backlog for missing AOProof API flows.\n"
                "Do not invent endpoints beyond what context implies.\n"
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
                "Deliverable format (Markdown, max ~120 lines):\n"
                "A) Missing API endpoints and behaviors (prioritized)\n"
                "B) Suggested file/module touchpoints (paths under /root/aoproof/packages/api)\n"
                "C) DB touchpoints (tables already exist; list what to read/write)\n"
                "D) Minimal integration test plan (what to validate)\n"
                "\n"
                "Focus areas explicitly mentioned in context:\n"
                "- /v0/transfer (currently 501) must be implemented\n"
                "- custody auth endpoints (login/register)\n"
                "- wallet claim finalize / tx flow support (if backend changes needed)\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Backend implementation backlog",
            artifacts=[
                Artifact(
                    type="implementation",
                    description="Backend implementation plan (structured markdown)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
