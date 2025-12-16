from dto.core.plugins.registry import PluginRegistry
from dto.plugins.devteam.architect import ArchitectAgent
from dto.plugins.devteam.backendDev import BackendDevAgent
from dto.plugins.devteam.qa import QaAgent
from dto.plugins.devteam.consolidator import ConsolidatorAgent


def register(registry: PluginRegistry) -> None:
    registry.register("Architect", lambda: ArchitectAgent())
    registry.register("BackendDev", lambda: BackendDevAgent())
    registry.register("QA", lambda: QaAgent())
    registry.register("Consolidator", lambda: ConsolidatorAgent())
