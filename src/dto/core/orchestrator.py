from __future__ import annotations

from dto.core.contracts import PipelineResult, Task
from dto.core.llm.base import LlmClient
from dto.core.plugins.registry import PluginRegistry
from dto.core.storage.base import ResultStore


class Orchestrator:
    def __init__(self, llm: LlmClient, registry: PluginRegistry, store: ResultStore) -> None:
        self.llm = llm
        self.registry = registry
        self.store = store

    async def runDevTeamPipeline(self, task: Task) -> PipelineResult:
        roles = [
            "Architect",
            "BackendDev",
            "QA",
            "Consolidator",
        ]

        results = []

        for roleName in roles:
            agent = self.registry.create(roleName)
            agentResult = await agent.run(self.llm, task, results)
            results.append(agentResult)

        finalSummary = ""
        finalArtifacts = []

        for r in results:
            for a in r.artifacts:
                if a.type == "finalPlan":
                    finalSummary = a.payload.get("text", "")
                    finalArtifacts.append(a)

        pipelineResult = PipelineResult(
            task=task,
            results=results,
            finalSummary=finalSummary,
            finalArtifacts=finalArtifacts,
        )

        self.store.save(pipelineResult)

        return pipelineResult
