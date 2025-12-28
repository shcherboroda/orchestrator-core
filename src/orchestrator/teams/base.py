from __future__ import annotations

from typing import Any, Dict, List


ArtifactDict = Dict[str, Any]


class BaseTeam:
    """
    Base class for team plugins.
    Each team must set a unique `name` and implement `run` to return artifact dicts.
    """

    name: str

    def run(self, **kwargs: Any) -> List[ArtifactDict]:
        raise NotImplementedError

    def _build_artifact(self, type: str, payload: Dict[str, Any]) -> ArtifactDict:
        """
        Helper to ensure a consistent artifact contract.
        """
        return {
            "type": type,
            "version": "1.0",
            "team": self.name,
            "payload": payload,
        }
