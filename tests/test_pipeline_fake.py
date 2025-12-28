from __future__ import annotations

import asyncio

from orchestrator.core.contracts import Task
from orchestrator.core.llm.fake import FakeLlmClient
from orchestrator.core.orchestrator import Orchestrator
from orchestrator.core.plugins.registry import PluginRegistry
from orchestrator.core.storage.jsonStore import JsonResultStore
from orchestrator.plugins import devteam


def testFakePipelineProducesFinalPlan() -> None:
    registry = PluginRegistry()
    devteam.register(registry)

    llm = FakeLlmClient()
    store = JsonResultStore(baseDir="runs-test")

    orchestrator = Orchestrator(
        llm=llm,
        llmType="fake",
        llmModel="fake",
        registry=registry,
        store=store,
    )

    task = Task(
        projectId="test",
        goal="Test goal",
    )

    roles = [
        "Architect",
        "BackendDev",
        "QA",
        "Consolidator",
    ]

    result = asyncio.run(orchestrator.runPipeline(task, roles))

    assert "FAKE_LLM_OUTPUT" in result.finalSummary
    assert result.meta.llm.type == "fake"
