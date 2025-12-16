from __future__ import annotations

from abc import ABC, abstractmethod
from dto.core.contracts import PipelineResult


class ResultStore(ABC):
    @abstractmethod
    def save(self, result: PipelineResult) -> str:
        raise NotImplementedError
