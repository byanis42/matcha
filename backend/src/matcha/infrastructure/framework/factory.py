from typing import TypeVar, Dict, Any, Generic, Protocol, ClassVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Factory(Protocol, Generic[T]):
    """
    Base factory interface for creating domain entities.
    """

    @staticmethod
    def create(**kwargs) -> T:
        """Create a new instance of the entity."""
        ...

    @staticmethod
    def build_from_dict(data: Dict[str, Any]) -> T:
        """Build an entity from a dictionary of attributes."""
        ...


class EntityFactory(Generic[T]):
    """
    Base implementation of a factory for creating domain entities.
    """

    model_class: ClassVar[type[T]]

    @classmethod
    def create(cls, **kwargs) -> T:
        """Create a new instance of the entity with the given attributes."""
        return cls.model_class(**kwargs)

    @classmethod
    def build_from_dict(cls, data: Dict[str, Any]) -> T:
        """Build an entity from a dictionary of attributes."""
        return cls.model_class(**data)
