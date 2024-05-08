from sqlalchemy.ext.asyncio import AsyncSession
from src.unit_of_work.base import UnitOfWorkABC


class PostgresqlUnitOfWork(UnitOfWorkABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
