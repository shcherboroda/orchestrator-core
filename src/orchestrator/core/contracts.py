from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class Task(BaseModel):
    projectId: str
    goal: str
    context: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    acceptanceCriteria: list[str] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class Artifact(BaseModel):
    type: str
    description: str
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agentRole: str
    summary: str
    decisions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    nextActions: list[str] = Field(default_factory=list)

class LlmInfo(BaseModel):
    type: str
    model: str


class PipelineMeta(BaseModel):
    llm: LlmInfo

class LlmInfo(BaseModel):
    type: str
    model: str


class PipelineMeta(BaseModel):
    llm: LlmInfo


class PipelineResult(BaseModel):
    task: Task
    results: list[AgentResult]
    finalSummary: str
    finalArtifacts: list[Artifact] = Field(default_factory=list)
    meta: PipelineMeta
