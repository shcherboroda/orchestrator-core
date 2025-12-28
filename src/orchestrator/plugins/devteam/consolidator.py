from __future__ import annotations

from orchestrator.core.contracts import AgentResult, Artifact, ChatMessage, Task
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import Agent
from orchestrator.plugins.devteam.prompt import buildCommonHeader


class ConsolidatorAgent(Agent):
    roleName = "Consolidator"

    async def run(self, llm: LlmClient, task: Task, previous: list[AgentResult]) -> AgentResult:
        header = buildCommonHeader(task)

        joined = ""
        for r in previous:
            joined += f"\n\n=== {r.agentRole} ===\n"
            for a in r.artifacts:
                joined += f"[{a.type}] {a.description}\n"
                joined += f"{a.payload.get('text', '')}\n"

        system = ChatMessage(
            role="system",
            content=(
                "You are a Tech Lead.\n"
                "Your job: consolidate into a single v0 execution plan.\n"
                "Be concrete, short, and reference the project DoD from context.\n"
            ),
        )

        user = ChatMessage(
            role="user",
            content=(
                f"{header}\n"
                "\n"
                "Inputs:\n"
                f"{joined}\n"
                "\n"
                "Deliverable format (Markdown, max ~160 lines):\n"
                "- v0 Milestones with checklists\n"
                "- Dependencies\n"
                "- Risk list\n"
                "- Next actions for the next 1-2 days (very concrete)\n"
            ),
        )

        text = await llm.chat([system, user])

        return AgentResult(
            agentRole=self.roleName,
            summary="Consolidated v0 execution plan",
            artifacts=[
                Artifact(
                    type="finalPlan",
                    description="Final consolidated plan (structured markdown)",
                    payload={
                        "text": text,
                    },
                ),
            ],
        )
