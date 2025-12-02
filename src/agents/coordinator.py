"""Coordinator Agent - Multi-agent Workflow Orchestration"""
import asyncio
import logging
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    """Task assigned to an agent"""
    id: str
    title: str
    description: str
    assigned_agent: str
    priority: int = 2
    state: TaskState = TaskState.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

class EventBus:
    """Event publishing system for inter-agent communication"""
    def __init__(self):
        self.subscribers: Dict[str, List] = {}
    
    def subscribe(self, event_type: str, handler) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: Dict) -> None:
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")

class Coordinator:
    """Orchestrates multi-agent workflows with task management and parallel execution"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Any] = {}
        self.event_bus = EventBus()
    
    def register_agent(self, name: str, agent) -> None:
        """Register an agent with coordinator"""
        self.agents[name] = agent
        logger.info(f"Agent registered: {name}")
    
    def create_task(self, title: str, description: str, agent: str, 
                   priority: int = 2, deps: List[str] = None) -> str:
        """Create and add task to workflow"""
        task_id = str(uuid.uuid4())[:8]
        task = Task(id=task_id, title=title, description=description,
                   assigned_agent=agent, priority=priority,
                   dependencies=deps or [])
        self.tasks[task_id] = task
        return task_id
    
    def get_ready_tasks(self) -> List[Task]:
        """Get tasks ready for execution"""
        completed = {t_id for t_id, t in self.tasks.items() 
                    if t.state == TaskState.COMPLETED}
        ready = [t for t_id, t in self.tasks.items() 
                if t.state == TaskState.PENDING 
                and all(d in completed for d in t.dependencies)]
        return sorted(ready, key=lambda t: t.priority, reverse=True)
    
    async def execute_task(self, task: Task) -> None:
        """Execute single task"""
        try:
            task.state = TaskState.RUNNING
            await self.event_bus.publish('task_started', {'task_id': task.id})
            
            agent = self.agents.get(task.assigned_agent)
            if agent and hasattr(agent, 'execute'):
                result = await agent.execute({'task_id': task.id, 'title': task.title,
                                             'description': task.description})
                task.result = result
                task.state = TaskState.COMPLETED
                await self.event_bus.publish('task_completed', 
                                            {'task_id': task.id, 'result': result})
            else:
                raise ValueError(f"Agent '{task.assigned_agent}' not found")
        except Exception as e:
            task.state = TaskState.FAILED
            task.error = str(e)
            await self.event_bus.publish('task_failed', 
                                        {'task_id': task.id, 'error': str(e)})
            logger.error(f"Task {task.id} failed: {e}")
    
    async def run_workflow(self) -> Dict[str, Any]:
        """Execute entire workflow with parallel task execution"""
        logger.info("Starting workflow execution")
        
        while any(t.state in [TaskState.PENDING, TaskState.RUNNING] 
                 for t in self.tasks.values()):
            ready = self.get_ready_tasks()
            if not ready:
                await asyncio.sleep(0.1)
                continue
            
            await asyncio.gather(*[self.execute_task(t) for t in ready])
        
        logger.info("Workflow execution complete")
        return self.get_status()
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get task status"""
        task = self.tasks.get(task_id)
        if task:
            return {'id': task.id, 'title': task.title, 'state': task.state.value,
                   'result': task.result, 'error': task.error}
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get full workflow status"""
        states = {}
        for task in self.tasks.values():
            s = task.state.value
            states[s] = states.get(s, 0) + 1
        return {'total_tasks': len(self.tasks), 'state_breakdown': states,
               'tasks': {t_id: t for t_id, t in self.tasks.items()}}
