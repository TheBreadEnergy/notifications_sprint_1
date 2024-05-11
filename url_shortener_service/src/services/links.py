import datetime
from abc import ABC, abstractmethod

from src.core.config import settings
from src.exceptions.link import LinkExpiredException, LinkNotFound
from src.repositories.links import LinksRepositoryABC
from src.schemas.links import ShortDbLinkCreateSchema
from src.services.base import Md5ShortUrlGenerator, ShortUrlGeneratorABC


class LinksShortenerABC(ABC):
    @abstractmethod
    async def shorten(self, url: str, ttl_s: int = settings.long_live_seconds) -> str:
        ...

    @abstractmethod
    async def unshorten(self, url: str) -> str:
        ...


class LinksShortener(LinksShortenerABC):
    def __init__(
        self,
        repository: LinksRepositoryABC,
        algorithm: ShortUrlGeneratorABC = Md5ShortUrlGenerator(),
    ):
        self._repository = repository
        self._algorithm = algorithm

    async def unshorten(self, url: str) -> str:
        short_url = await self._repository.get_link_by_short_url(short_url=url)
        if not short_url:
            raise LinkNotFound()
        if str(short_url.expires_at) <= str(
            datetime.datetime.now(datetime.timezone.utc)
        ):
            raise LinkExpiredException()
        return short_url.original_link

    async def shorten(self, url: str, ttl_s: int = settings.long_live_seconds) -> str:
        current_url = url
        candidate = self._algorithm.shorten_url(url=url)
        entity = await self._repository.get_link_by_short_url(short_url=candidate)
        while entity:
            candidate = self._algorithm.shorten_url(url=current_url)
            entity = await self._repository.get_link_by_short_url(short_url=candidate)
            current_url += candidate
        entity = ShortDbLinkCreateSchema(
            short_link=candidate,
            original_link=url,
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(
                seconds=ttl_s,
            ),
        )
        await self._repository.insert(data=entity)
        return candidate
