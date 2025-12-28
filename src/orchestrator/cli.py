from __future__ import annotations

import asyncio
import os
import typer
from dotenv import load_dotenv

from orchestrator.core.contracts import Task
from orchestrator.core.llm.factory import LlmFactory
from orchestrator.core.orchestrator import Orchestrator
from orchestrator.core.plugins.registry import PluginRegistry
from orchestrator.core.storage.jsonStore import JsonResultStore
from orchestrator.plugins import devteam


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def root() -> None:
    """
    Orchestrator Core CLI.
    """
    return


@app.command("run")
def runCommand(
    project: str = typer.Option(..., "--project"),
    goal: str = typer.Option(..., "--goal"),
    llm: str = typer.Option(
        "fake",
        "--llm",
        help="LLM backend to use: fake | ollama | openai",
    ),
) -> None:
    load_dotenv()

    registry = PluginRegistry()
    devteam.register(registry)

    llmClient = LlmFactory.create(llm)

    if llm == "fake":
        llmModel = "fake"
    elif llm == "ollama":
        llmModel = os.getenv("DTOollamaModel", "qwen2.5:3b")
    else:
        llmModel = os.getenv("DTOllmModel", "gpt-4o-mini")

    store = JsonResultStore()

    orchestrator = Orchestrator(
        llm=llmClient,
        llmType=llm,
        llmModel=llmModel,
        registry=registry,
        store=store,
    )

    contextPath = f"projects/{project}/context.md"
    projectContext = ""

    if os.path.exists(contextPath):
        with open(contextPath, "r", encoding="utf-8") as f:
            projectContext = f.read()


    task = Task(
        projectId=project,
        goal=goal,
        context={
            "projectContext": projectContext,
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

    try:
        result = asyncio.run(orchestrator.runPipeline(task, roles))
    except Exception as e:
        typer.echo(f"ERROR: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo("\n=== FINAL PLAN ===\n")
    typer.echo(result.finalSummary)
    typer.echo(f"\nLLM used: {llm} ({llmModel})")
    typer.echo("\nSaved into runs/ as JSON")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
