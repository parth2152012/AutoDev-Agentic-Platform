"""Event Bus for inter-agent communication and event publishing"""

import asyncio
import logging
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """Event data structure for publishing across agents"""
    event_type: str
    source_agent: str
    data: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class EventBus:
    """Central event bus for async event publishing and subscription"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self._lock = asyncio.Lock()
        
    async def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe a callback to an event type"""
        async with self._lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
            logger.info(f"Subscribed {callback.__name__} to {event_type}")
    
    async def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe a callback from an event type"""
        async with self._lock:
            if event_type in self.subscribers:
                self.subscribers[event_type] = [
                    c for c in self.subscribers[event_type] if c != callback
                ]
                logger.info(f"Unsubscribed {callback.__name__} from {event_type}")
    
    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers"""
        await self.event_queue.put(event)
        logger.debug(f"Event published: {event.event_type} from {event.source_agent}")
    
    async def emit(self, event: Event) -> None:
        """Emit event to all subscribed callbacks"""
        if event.event_type in self.subscribers:
            tasks = []
            for callback in self.subscribers[event.event_type]:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(event))
                else:
                    callback(event)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def get_events(self) -> Event:
        """Get events from the queue"""
        return await self.event_queue.get()
    
    async def process_events(self) -> None:
        """Process events from queue and emit to subscribers"""
        while True:
            try:
                event = await self.get_events()
                await self.emit(event)
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    def get_subscribers_count(self, event_type: str) -> int:
        """Get count of subscribers for an event type"""
        return len(self.subscribers.get(event_type, []))
    
    async def clear(self) -> None:
        """Clear all subscribers"""
        async with self._lock:
            self.subscribers.clear()
            logger.info("EventBus cleared")

# Global event bus instance
_event_bus: EventBus = None

def get_event_bus() -> EventBus:
    """Get or create the global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
