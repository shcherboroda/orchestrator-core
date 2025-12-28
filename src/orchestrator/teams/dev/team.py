from __future__ import annotations

import asyncio
import os
from typing import Any, List

from dotenv import load_dotenv

from orchestrator.core.contracts import Task
from orchestrator.core.llm.factory import LlmFactory
from orchestrator.core.orchestrator import Orchestrator
from orchestrator.core.plugins.registry import PluginRegistry
from orchestrator.core.storage.jsonStore import JsonResultStore
from orchestrator.plugins import devteam as devteam_plugin
from orchestrator.teams.base import ArtifactDict, BaseTeam


class DevTeam(BaseTeam):
    name = "dev"

    def run(self, project: str | None = None, goal: str | None = None, llm: str = "fake", **_: Any) -> List[ArtifactDict]:
        if not project:
            raise ValueError("Dev team requires --project")
        if not goal:
            raise ValueError("Dev team requires --goal")

        load_dotenv()

        registry = PluginRegistry()
        devteam_plugin.register(registry)

        llm_client = LlmFactory.create(llm)

        if llm == "fake":
            llm_model = "fake"
        elif llm == "ollama":
            llm_model = os.getenv("DTOollamaModel", "qwen2.5:3b")
        else:
            llm_model = os.getenv("DTOollmModel", "gpt-4o-mini")

        store = JsonResultStore()

        orchestrator = Orchestrator(
            llm=llm_client,
            llmType=llm,
            llmModel=llm_model,
            registry=registry,
            store=store,
        )

        context_path = f"projects/{project}/context.md"
        project_context = ""

        if os.path.exists(context_path):
            with open(context_path, "r", encoding="utf-8") as f:
                project_context = f.read()

        task = Task(
            projectId=project,
            goal=goal,
            context={
                "projectContext": project_context,
            },
            constraints=[
                "Modular design",
                "Replaceable components",
            ],
            acceptanceCriteria=[
                "A concrete plan and task list",
            ],
        )

        roles = [
            "Architect",
            "BackendDev",
            "QA",
            "Consolidator",
        ]

        result = asyncio.run(orchestrator.runPipeline(task, roles))

        artifacts: List[ArtifactDict] = [
            self._build_artifact(a.type, a.payload) for a in result.finalArtifacts
        ]

        if not artifacts and result.finalSummary:
            artifacts.append(
                self._build_artifact(
                    "final_summary",
                    {
                        "text": result.finalSummary,
                    },
                )
            )

        return artifacts
