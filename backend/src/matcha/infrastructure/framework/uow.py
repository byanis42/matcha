from typing import final


class UnitOfWork:
    @final
    async def __aenter__(self):
        await self.begin()
        return self

    @final
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            await self.rollback()
            raise
        else:
            await self.commit()

    async def begin(self): ...

    async def rollback(self): ...

    async def commit(self): ...
