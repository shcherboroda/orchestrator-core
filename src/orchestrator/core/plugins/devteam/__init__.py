from orchestrator.core.plugins.registry import PluginRegistry
from orchestrator.plugins.devteam.architect import ArchitectAgent
from orchestrator.plugins.devteam.backendDev import BackendDevAgent
from orchestrator.plugins.devteam.qa import QaAgent
from orchestrator.plugins.devteam.consolidator import ConsolidatorAgent


def register(registry: PluginRegistry) -> None:
    registry.register("Architect", lambda: ArchitectAgent())
    registry.register("BackendDev", lambda: BackendDevAgent())
    registry.register("QA", lambda: QaAgent())
    registry.register("Consolidator", lambda: ConsolidatorAgent())
