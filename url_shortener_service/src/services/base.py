import hashlib
from abc import ABC, abstractmethod


class ShortUrlGeneratorABC(ABC):
    @abstractmethod
    def shorten_url(self, url: str) -> str:
        ...


class Md5ShortUrlGenerator(ShortUrlGeneratorABC):
    def shorten_url(self, url: str, size: int = 5) -> str:
        return hashlib.md5(url.encode("utf-8")).hexdigest()[:5]
