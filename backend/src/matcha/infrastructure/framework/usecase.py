import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from matcha.domain.uow import MatchaUnitOfWork

Input = TypeVar("Input", bound=BaseModel)
Output = TypeVar("Output", bound=BaseModel)
T = TypeVar("T", bound=MatchaUnitOfWork)


class UseCase(Generic[T], ABC):
    """Base abstract class for all use cases."""

    def __init__(self, uow: T):
        self.uow = uow
        if hasattr(self.uow, "log"):
            self.log = self.uow.log.set_name(self.__class__.__name__)
        else:
            self.log = logging.getLogger(__name__)

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """Execute the use case with the provided arguments."""
        ...


class CommandUseCase(UseCase[T], Generic[T, Input, Output]):
    """
    Base class for command use cases that work with a UnitOfWork.
    Command use cases typically modify the system state.
    """

    async def execute(self, input_data: Input) -> Output:
        """Execute the command with a unit of work transaction."""
        async with self.uow:
            return await self._execute(input_data)

    @abstractmethod
    async def _execute(self, input_data: Input) -> Output:
        """Concrete implementation should override this method."""
        ...


class QueryUseCase(UseCase[T], Generic[T, Input, Output]):
    """
    Base class for query use cases.
    Query use cases typically read the system state without modifying it.
    """

    async def execute(self, input_data: Input) -> Output:
        """Execute the query directly without transaction boundaries."""
        return await self._execute(input_data)

    @abstractmethod
    async def _execute(self, input_data: Input) -> Output:
        """Concrete implementation should override this method."""
        ...
