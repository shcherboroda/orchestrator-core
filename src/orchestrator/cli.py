from __future__ import annotations

import json
import typer
from dotenv import load_dotenv

from orchestrator.teams import get_team, list_teams


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
    team: str = typer.Option(..., "--team", help="Team to run (marketing | dev)"),
    project: str | None = typer.Option(None, "--project", help="Project id (required for dev team)"),
    goal: str | None = typer.Option(None, "--goal", help="Goal for this run"),
    llm: str = typer.Option(
        "fake",
        "--llm",
        help="LLM backend to use: fake | ollama | openai",
    ),
) -> None:
    """
    Run a team workflow and emit a JSON array of artifacts to stdout.
    """
    load_dotenv()

    try:
        selected_team = get_team(team)
    except KeyError:
        typer.echo(f"Unknown team: {team}. Available: {', '.join(list_teams())}", err=True)
        raise typer.Exit(code=1)

    if team == "dev" and project is None:
        typer.echo("ERROR: --project is required for dev team", err=True)
        raise typer.Exit(code=1)

    try:
        artifacts = selected_team.run(
            project=project,
            goal=goal,
            llm=llm,
        )
    except Exception as e:
        typer.echo(f"ERROR: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(
        json.dumps(
            artifacts,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
