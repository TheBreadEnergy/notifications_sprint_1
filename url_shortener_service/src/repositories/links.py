from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.cache.cache import CacheABC
from src.models.short_link import ShortLink
from src.repositories.base import PostgresRepository, RepositoryABC
from src.schemas.links import ShortLinkCreateSchema


class LinksRepositoryABC(RepositoryABC, ABC):
    @abstractmethod
    async def get_link_by_short_url(self, short_url: str) -> ShortLink | None:
        ...


class LinksRepository(
    PostgresRepository[ShortLink, ShortLinkCreateSchema], LinksRepositoryABC
):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ShortLink)

    async def get_link_by_short_url(self, short_url: str) -> ShortLink | None:
        statement = select(self._model).where(ShortLink.short_link == short_url)
        results = await self._session.execute(statement)
        return results.scalar_one_or_none()


class CacheableLinksRepository(LinksRepositoryABC):
    def __init__(self, repository: LinksRepository, cache: CacheABC[ShortLink]):
        self._repository = repository
        self._cache = cache

    async def get_link_by_short_url(self, short_url: str) -> ShortLink | None:
        key = f"short_link_{short_url}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._repository.get_link_by_short_url(short_url=short_url)
            if entity:
                await self._cache.set(key=key, value=entity)
        return entity

    async def delete(self, *, entity_id: UUID):
        return await self._repository.delete(entity_id=entity_id)

    async def insert(self, data: ShortLinkCreateSchema) -> ShortLink:
        return await self._repository.insert(data=data)

    async def get(self, *, entity_id: UUID) -> ShortLink | None:
        key = f"short_link_id_{entity_id}"
        entity = await self._cache.get(key=key)
        if not entity:
            entity = await self._repository.get(entity_id=entity_id)
            if entity:
                await self._cache.set(key=key, value=entity)
        return entity

    async def gets(self, *, skip: int = 0, limit: int = 100) -> Sequence[ShortLink]:
        return await self._repository.gets(skip=skip, limit=limit)
