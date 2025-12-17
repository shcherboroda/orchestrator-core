from __future__ import annotations

import asyncio
import typer

from dto.core.contracts import Task
from dto.core.llm.fake import FakeLlmClient
from dto.core.orchestrator import Orchestrator
from dto.core.plugins.registry import PluginRegistry
from dto.core.storage.jsonStore import JsonResultStore
from dto.plugins import devteam


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def root() -> None:
    """
    Dev Team Orchestrator CLI.
    """
    return


@app.command("run")
def runCommand(
    project: str = typer.Option(..., "--project", help="Project identifier"),
    goal: str = typer.Option(..., "--goal", help="High-level goal for the team"),
) -> None:
    registry = PluginRegistry()
    devteam.register(registry)

    llm = FakeLlmClient()
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
            "environment": "Ubuntu VPS",
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

    typer.echo("\n=== FINAL PLAN ===\n")
    typer.echo(result.finalSummary)
    typer.echo("\nSaved into runs/ as JSON")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
