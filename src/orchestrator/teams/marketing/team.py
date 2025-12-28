from __future__ import annotations

from typing import Any, List

from orchestrator.teams.base import ArtifactDict, BaseTeam


class MarketingTeam(BaseTeam):
    name = "marketing"

    def run(self, goal: str | None = None, **_: Any) -> List[ArtifactDict]:
        marketing_goal = goal or "Grow product awareness and engagement"

        payload = {
            "goal": marketing_goal,
            "targetAudience": [
                "Developers evaluating workflow orchestration tools",
                "Team leads adopting AI-assisted delivery pipelines",
            ],
            "contentPlan": {
                "posts": [
                    {
                        "format": "blog",
                        "hook": "Why orchestration-as-code beats bespoke scripts for AI projects",
                        "cta": "Read the full guide and try the starter repo",
                    },
                    {
                        "format": "linkedin",
                        "hook": "A 3-step playbook to ship AI features weekly without firefighting",
                        "cta": "Download the playbook template",
                    },
                    {
                        "format": "email",
                        "hook": "Stop context chaos: unify prompts, tasks, and QA in one pipeline",
                        "cta": "Join the beta cohort",
                    },
                ],
                "distribution": [
                    "Company blog",
                    "LinkedIn company page",
                    "Product newsletter",
                    "Developer community forums",
                ],
            },
        }

        return [
            self._build_artifact(
                "marketing_plan",
                payload,
            )
        ]
