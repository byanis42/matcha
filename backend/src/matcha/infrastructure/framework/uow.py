from typing import final


class UnitOfWork:
    """
    Base Unit of Work abstract class that defines the transaction boundary interface.
    All concrete UoW implementations should inherit from this class.
    """

    @final
    async def __aenter__(self):
        """Start a new transaction and return self."""
        await self.begin()
        return self

    @final
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        """Commit or rollback the transaction based on if an exception occurred."""
        if exc_type:
            await self.rollback()
            raise
        else:
            await self.commit()

    async def begin(self):
        """Initialize the transaction."""
        ...

    async def commit(self):
        """Commit the transaction."""
        ...

    async def rollback(self):
        """Rollback the transaction."""
        ...
