"""Redis Client for Caching and State"""
import logging
import json
from typing import Any, Optional

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis wrapper for caching and state management"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Connect to Redis"""
        try:
            import redis
            self.client = redis.Redis(host=self.host, port=self.port, db=self.db)
            self.client.ping()
            self.connected = True
            logger.info(f"Connected to Redis at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.connected = False
            return False
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set key-value in Redis"""
        if not self.connected or not self.client:
            return False
        try:
            if isinstance(value, dict):
                value = json.dumps(value)
            if ttl:
                self.client.setex(key, ttl, value)
            else:
                self.client.set(key, value)
            return True
        except Exception as e:
            logger.error(f"Redis set failed: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.connected or not self.client:
            return None
        try:
            value = self.client.get(key)
            return value.decode() if value else None
        except Exception as e:
            logger.error(f"Redis get failed: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.connected or not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete failed: {e}")
            return False
    
    async def flush(self) -> bool:
        """Flush all data"""
        if not self.connected or not self.client:
            return False
        try:
            self.client.flushdb()
            logger.info("Redis database flushed")
            return True
        except Exception as e:
            logger.error(f"Redis flush failed: {e}")
            return False
