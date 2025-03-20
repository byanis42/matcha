from typing import Protocol, TypeVar, Generic, ClassVar, List
from pydantic import BaseModel

from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.services.message_bus import DomainEvent

T = TypeVar("T", bound=BaseModel)


class Command(BaseModel):
    """
    Base class for commands.
    Commands are objects that represent an intention to change the system state.
    """
    command_type: str = ""

    class Config:
        populate_by_name = True

    def __init_subclass__(cls, **kwargs):
        """Set command_type automatically for each subclass."""
        super().__init_subclass__(**kwargs)
        cls.command_type = cls.__name__


class CommandResult(BaseModel):
    """
    Base class for command execution results.
    Contains information about the command execution status and any events generated.
    """
    success: bool = True
    error_message: str = ""
    events: List[DomainEvent] = []


class CommandHandler(Protocol, Generic[T]):
    """
    Base command handler interface.
    Defines the contract for handling commands.
    """

    command_type: ClassVar[type[T]]

    async def handle(self, command: T, uow: MatchaUnitOfWork) -> CommandResult:
        """Handle the command and return a result."""
        ...


class BaseCommandHandler(Generic[T]):
    """
    Base implementation of a command handler.
    Provides common functionality for command handlers.
    """

    command_type: ClassVar[type[T]]

    async def handle(self, command: T, uow: MatchaUnitOfWork) -> CommandResult:
        """
        Handle the command within a UoW transaction and return a result.
        The actual command handling logic is in the _handle method.
        """
        try:
            async with uow:
                result = await self._handle(command, uow)

                # Add any generated events to the message bus
                for event in result.events:
                    uow.message_bus.add_event(event)

                return result
        except Exception as e:
            # Log the exception
            return CommandResult(
                success=False,
                error_message=str(e)
            )

    async def _handle(self, command: T, uow: MatchaUnitOfWork) -> CommandResult:
        """Concrete implementation should override this method."""
        raise NotImplementedError
