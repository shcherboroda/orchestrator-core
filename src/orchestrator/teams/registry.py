from __future__ import annotations

from typing import Dict, List, Type

from orchestrator.teams.base import BaseTeam


_TEAM_REGISTRY: Dict[str, Type[BaseTeam]] = {}


def register_team(team_cls: Type[BaseTeam]) -> None:
    """
    Register a team class by its declared name.
    """
    _TEAM_REGISTRY[team_cls.name] = team_cls


def get_team(team_name: str) -> BaseTeam:
    """
    Instantiate a team by name.
    """
    team_cls = _TEAM_REGISTRY.get(team_name)
    if team_cls is None:
        raise KeyError(f"Unknown team: {team_name}")
    return team_cls()


def list_teams() -> List[str]:
    """
    Return sorted list of registered team names.
    """
    return sorted(_TEAM_REGISTRY.keys())
