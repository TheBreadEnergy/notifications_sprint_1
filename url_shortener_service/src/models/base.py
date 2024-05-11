from abc import ABC, abstractmethod

from sqlalchemy.orm import DeclarativeBase


class CacheableABC(ABC):
    @abstractmethod
    def serialize_object(self, *args, **kwargs):
        ...


class Base(DeclarativeBase):
    ...
