"""State Management for Workflows and Tasks"""
import logging
from typing import Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class StateManager:
    """Manages state for workflows, tasks, and agents"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.local_state: Dict[str, Any] = {}
    
    async def save_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> None:
        """Save workflow state"""
        self.local_state[f'workflow:{workflow_id}'] = workflow_data
        if self.redis:
            try:
                await self.redis.set(f'workflow:{workflow_id}', json.dumps(workflow_data))
            except Exception as e:
                logger.error(f"Redis save failed: {e}")
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow state"""
        key = f'workflow:{workflow_id}'
        if self.redis:
            try:
                data = await self.redis.get(key)
                return json.loads(data) if data else None
            except:
                pass
        return self.local_state.get(key)
    
    async def save_task(self, task_id: str, task_data: Dict[str, Any]) -> None:
        """Save task state"""
        self.local_state[f'task:{task_id}'] = task_data
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task state"""
        return self.local_state.get(f'task:{task_id}')
    
    async def save_agent_state(self, agent_id: str, state: Dict[str, Any]) -> None:
        """Save agent execution state"""
        self.local_state[f'agent:{agent_id}'] = {
            **state,
            'updated_at': datetime.now().isoformat()
        }
    
    async def get_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent state"""
        return self.local_state.get(f'agent:{agent_id}')
    
    async def clear_state(self) -> None:
        """Clear all state"""
        self.local_state.clear()
        logger.info("State cleared")
