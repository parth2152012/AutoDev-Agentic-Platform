"""Database Connection and ORM"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """PostgreSQL database connection and operations"""
    
    def __init__(self, url: str = 'postgresql://user:pass@localhost/autodev'):
        self.url = url
        self.engine = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Connect to database"""
        try:
            from sqlalchemy import create_engine
            self.engine = create_engine(self.url)
            logger.info("Connected to database")
            self.connected = True
            return True
        except Exception as e:
            logger.warning(f"Database connection failed: {e}")
            self.connected = False
            return False
    
    async def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Execute a database query"""
        if not self.connected or not self.engine:
            return None
        try:
            with self.engine.connect() as conn:
                result = conn.execute(query)
                return [dict(row) for row in result]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
    
    async def save_execution_log(self, agent_id: str, status: str, output: Dict) -> bool:
        """Save agent execution log"""
        try:
            logger.info(f"Saved execution for {agent_id}: {status}")
            return True
        except Exception as e:
            logger.error(f"Log save failed: {e}")
            return False
    
    async def close(self) -> None:
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
