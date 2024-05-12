from abc import ABC, abstractmethod


class UnitOfWorkABC(ABC):
    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    def __aenter__(self) -> "UnitOfWorkABC":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
