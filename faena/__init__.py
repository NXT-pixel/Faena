"""
Faena: Autonomous AI Factory for End-to-End Ticket Implementation.
"""
__version__ = "1.0.0"

from faena.orchestrator.pipeline import FaenaPipeline
from faena.providers.factory import create_provider, auto_detect_provider
from faena.agents.registry import AgentRegistry

__all__ = [
    "FaenaPipeline",
    "create_provider",
    "auto_detect_provider",
    "AgentRegistry",
]
