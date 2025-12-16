from __future__ import annotations

import json
import os
import time
from dto.core.contracts import PipelineResult
from dto.core.storage.base import ResultStore


class JsonResultStore(ResultStore):
    def __init__(self, baseDir: str = "runs") -> None:
        self.baseDir = baseDir
        os.makedirs(self.baseDir, exist_ok=True)

    def save(self, result: PipelineResult) -> str:
        ts = int(time.time())
        filePath = os.path.join(self.baseDir, f"{result.task.projectId}-{ts}.json")

        with open(filePath, "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))

        return filePath
