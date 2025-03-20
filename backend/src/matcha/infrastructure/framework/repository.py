from typing import Protocol, TypeVar, Generic, List, Dict, Any

T = TypeVar("T")  # Type générique pour l'entité


class Repository(Protocol, Generic[T]):
    """
    Base repository interface that defines common operations.
    All concrete repositories should implement this protocol.
    """

    async def add(self, entity: T) -> None:
        """Add a new entity to the repository."""
        ...

    async def get(self, id_: str) -> T:
        """Retrieve an entity by its ID."""
        ...

    async def update(self, entity: T) -> None:
        """Update an existing entity."""
        ...

    async def remove(self, id_: str) -> None:
        """Remove an entity from the repository."""
        ...

    async def list(self, filters: Dict[str, Any] = None) -> List[T]:
        """List all entities in the repository, optionally filtered."""
        ...
