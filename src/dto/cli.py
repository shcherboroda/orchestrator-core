from __future__ import annotations

import asyncio
import os
import typer
from dotenv import load_dotenv

from dto.core.contracts import Task
from dto.core.llm.openaiCompat import OpenAiCompatLlmClient
from dto.core.orchestrator import Orchestrator
from dto.core.plugins.registry import PluginRegistry
from dto.core.storage.jsonStore import JsonResultStore
from dto.plugins import devteam


app = typer.Typer(add_completion=False)


@app.command()
def run(
    project: str = typer.Option(..., "--project"),
    goal: str = typer.Option(..., "--goal"),
) -> None:
    load_dotenv()

    registry = PluginRegistry()
    devteam.register(registry)

    llm = OpenAiCompatLlmClient()
    store = JsonResultStore()

    orchestrator = Orchestrator(
        llm=llm,
        registry=registry,
        store=store,
    )

    task = Task(
        projectId=project,
        goal=goal,
        context={
            "preferredEnvironment": "Ubuntu VPS",
            "editor": "VSCode",
        },
        constraints=[
            "Prefer modular design",
            "Prefer clear interfaces and replaceable components",
        ],
        acceptanceCriteria=[
            "Concrete plan and task list",
            "Clear risks and mitigations",
        ],
    )

    result = asyncio.run(orchestrator.runDevTeamPipeline(task))

    typer.echo("\n=== FINAL PLAN ===\n")
    typer.echo(result.finalSummary)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
