"""Dashboard package - Real-time monitoring and visualization APIs"""

from src.dashboard.app import create_app
from src.dashboard.routes import DashboardRoutes

__all__ = [
    "create_app",
    "DashboardRoutes",
]
