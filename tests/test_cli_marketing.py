from __future__ import annotations

import json
from typer.testing import CliRunner

from orchestrator.cli import app


runner = CliRunner()


def test_marketing_team_outputs_json() -> None:
    result = runner.invoke(
        app,
        ["run", "--team", "marketing"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0

    stdout = result.stdout.strip()
    artifacts = json.loads(stdout)

    assert isinstance(artifacts, list)
    assert any(
        isinstance(item, dict)
        and item.get("team") == "marketing"
        and item.get("type") == "marketing_plan"
        for item in artifacts
    )
