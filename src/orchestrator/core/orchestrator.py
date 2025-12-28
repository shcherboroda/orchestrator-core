from __future__ import annotations

from orchestrator.core.contracts import (
    PipelineMeta,
    PipelineResult,
    Task,
    LlmInfo,
)
from orchestrator.core.llm.base import LlmClient
from orchestrator.core.plugins.registry import PluginRegistry
from orchestrator.core.storage.base import ResultStore


class Orchestrator:
    def __init__(
        self,
        llm: LlmClient,
        llmType: str,
        llmModel: str,
        registry: PluginRegistry,
        store: ResultStore,
    ) -> None:
        self.llm = llm
        self.llmType = llmType
        self.llmModel = llmModel
        self.registry = registry
        self.store = store

    async def runPipeline(self, task: Task, roles: list[str]) -> PipelineResult:
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

        meta = PipelineMeta(
            llm=LlmInfo(
                type=self.llmType,
                model=self.llmModel,
            )
        )

        pipelineResult = PipelineResult(
            task=task,
            results=results,
            finalSummary=finalSummary,
            finalArtifacts=finalArtifacts,
            meta=meta,
        )

        self.store.save(pipelineResult)

        return pipelineResult
