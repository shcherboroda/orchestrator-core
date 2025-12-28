from __future__ import annotations

from orchestrator.core.contracts import AgentResult, Task


def getProjectContextText(task: Task) -> str:
    projectContext = ""

    if isinstance(task.context, dict):
        projectContext = str(task.context.get("projectContext", "")).strip()

    if projectContext == "":
        return "NO_PROJECT_CONTEXT_FOUND. Do not invent missing facts. Ask for required info explicitly."

    return projectContext


def buildCommonHeader(task: Task) -> str:
    projectContext = getProjectContextText(task)

    return (
        "You MUST base your work strictly on the provided PROJECT CONTEXT PACK.\n"
        "Do NOT invent unrelated product details.\n"
        "Do NOT propose changes to external repositories; only produce plans/specs/artifacts.\n"
        "If info is missing, list concrete questions.\n"
        "\n"
        "=== PROJECT CONTEXT PACK (facts) ===\n"
        f"{projectContext}\n"
        "\n"
        "=== TASK ===\n"
        f"ProjectId: {task.projectId}\n"
        f"Goal: {task.goal}\n"
    )


def findArtifactText(previous: list[AgentResult], artifactType: str) -> str:
    for r in previous:
        for a in r.artifacts:
            if a.type == artifactType:
                return str(a.payload.get("text", ""))
    return ""
