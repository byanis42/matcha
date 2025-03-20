from typing import List

from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.services.message_bus import MessageBus, DomainEvent


class MockMessageBus(MessageBus):
    """
    Mock implementation of the MessageBus for testing.
    Provides additional methods to inspect processed events.
    """

    def __init__(self, uow: MatchaUnitOfWork):
        super().__init__(uow)
        self.processed_events: List[DomainEvent] = []

    async def handle_events(self):
        """Process events and record them for test verification."""
        while self.queue:
            event = self.queue.pop(0)
            self.processed_events.append(event)

            event_name = event.event_name
            if event_name in self.event_handlers:
                for handler in self.event_handlers[event_name]:
                    await handler(event, self.uow)

    async def clear_queue(self):
        """Clear the event queue without processing."""
        self.queue.clear()

    def get_processed_events(self, event_type=None):
        """
        Get all processed events, optionally filtered by event type.
        Useful for assertions in tests.
        """
        if event_type is None:
            return self.processed_events

        return [
            event for event in self.processed_events
            if event.event_name == event_type.event_name
        ]

    def clear_processed_events(self):
        """Clear the record of processed events."""
        self.processed_events.clear()
