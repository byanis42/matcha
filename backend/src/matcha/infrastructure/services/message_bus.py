from pydantic import BaseModel, Field
from typing import Dict, List, Type, Callable, Awaitable
import uuid

from matcha.domain.uow import MatchaUnitOfWork


class DomainEvent(BaseModel):
    """Base class for all domain events."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_name: str = ""

    class Config:
        populate_by_name = True

    def __init_subclass__(cls, **kwargs):
        """Set event_name automatically for each subclass."""
        super().__init_subclass__(**kwargs)
        cls.event_name = cls.__name__


class MessageBus:
    """
    Service for handling domain events in an asynchronous manner.
    Collects events during a transaction and processes them after commit.
    """

    def __init__(self, uow: MatchaUnitOfWork):
        self.uow = uow
        self.event_handlers: Dict[str, List[Callable[[DomainEvent, MatchaUnitOfWork], Awaitable[None]]]] = {}
        self.queue: List[DomainEvent] = []

    def register_event_handler(
        self,
        event_type: Type[DomainEvent],
        handler: Callable[[DomainEvent, MatchaUnitOfWork], Awaitable[None]]
    ):
        """Register a handler for a specific event type."""
        event_name = event_type.event_name
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)

    def add_event(self, event: DomainEvent):
        """Add an event to the queue for processing after transaction commit."""
        self.queue.append(event)

    async def handle_events(self):
        """Process all queued events with their registered handlers."""
        while self.queue:
            event = self.queue.pop(0)
            event_name = event.event_name

            if event_name in self.event_handlers:
                for handler in self.event_handlers[event_name]:
                    await handler(event, self.uow)

    async def clear_queue(self):
        """Clear all queued events without processing them."""
        self.queue.clear()
