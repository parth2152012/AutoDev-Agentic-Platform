#!/usr/bin/env python3
"""
AutoDevAgentic Platform - Main Entry Point
Collaborative Agentic Platform for Automated Full-Stack Development
Techfest 2025-26 AutoDev Hackathon | Team ID: Auto-250358
"""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Setup logging
logging.basicConfig(
    level=logging.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AutoDev Agentic Platform",
    description="Collaborative Agentic Platform for Automated Full-Stack Development",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AutoDev-Agentic-Platform",
        "version": "0.1.0"
    }

# Status endpoint
@app.get("/status")
async def status():
    """Get platform status"""
    return {
        "platform": "AutoDev Agentic Platform",
        "team_id": "Auto-250358",
        "event": "Techfest 2025-26 AutoDev Hackathon",
        "round": "Round 2 Development",
        "status": "initialization",
        "agents": {
            "ado_parser": "pending",
            "coordinator": "pending",
            "frontend_agent": "pending",
            "backend_agent": "pending",
            "database_agent": "pending",
            "testing_agent": "pending",
            "legacy_analyzer": "pending",
            "prompt_refiner": "pending"
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AutoDev Agentic Platform",
        "documentation": "/docs",
        "health": "/health",
        "status": "/status"
    }

def main():
    """Main entry point"""
    logger.info("Starting AutoDev Agentic Platform...")
    
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    workers = int(os.getenv("WORKERS", "4"))
    
    logger.info(f"Server configuration: {host}:{port} with {workers} workers")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        workers=1,  # Set to 1 for development, increase for production
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

if __name__ == "__main__":
    main()
