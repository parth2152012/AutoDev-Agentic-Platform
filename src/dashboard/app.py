"""FastAPI Dashboard Application"""
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.cors import CORSMiddleware
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

app = FastAPI(title="AutoDev Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections: Dict[str, Any] = {}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok", "service": "autodev-dashboard"}

@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Get system status"""
    return {
        "agents": 8,
        "active_workflows": 3,
        "completed_tasks": 42,
        "failed_tasks": 2
    }

@app.get("/api/agents")
async def list_agents() -> Dict[str, Any]:
    """List all agents"""
    return {
        "agents": [
            {"name": "ado_parser", "status": "active"},
            {"name": "coordinator", "status": "active"},
            {"name": "frontend_agent", "status": "active"},
            {"name": "backend_agent", "status": "active"},
            {"name": "database_agent", "status": "active"},
            {"name": "testing_agent", "status": "active"},
            {"name": "legacy_analyzer", "status": "active"},
            {"name": "prompt_refiner", "status": "active"}
        ]
    }

@app.get("/api/workflows")
async def list_workflows() -> Dict[str, Any]:
    """List workflows"""
    return {"workflows": [], "total": 0}

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time events"""
    await websocket.accept()
    active_connections["default"] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections.pop("default", None)
