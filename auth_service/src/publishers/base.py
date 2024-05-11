from abc import ABC, abstractmethod


class PublisherABC(ABC):
    @abstractmethod
    def publish(self, *args, **kwargs):
        ...
