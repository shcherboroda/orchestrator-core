from orchestrator.teams.registry import get_team, list_teams, register_team
from orchestrator.teams.dev.team import DevTeam
from orchestrator.teams.marketing.team import MarketingTeam

register_team(DevTeam)
register_team(MarketingTeam)

__all__ = [
    "get_team",
    "list_teams",
    "register_team",
    "DevTeam",
    "MarketingTeam",
]
