"""
AutoDev-Agentic-Platform - Main package initialization
Initializes the AutoDev Platform with all agents and support modules
"""

from src.config import Config
from src.orchestration.workflow import WorkflowEngine
from src.orchestration.state_manager import StateManager
from src.infrastructure.redis_client import RedisClient
from src.infrastructure.database import DatabaseConnection
from src.infrastructure.docker_executor import DockerExecutor

__version__ = "1.0.0"
__author__ = "AutoDev Team"

# Export main components for easy imports
__all__ = [
    "Config",
    "WorkflowEngine",
    "StateManager",
    "RedisClient",
    "DatabaseConnection",
    "DockerExecutor",
]
