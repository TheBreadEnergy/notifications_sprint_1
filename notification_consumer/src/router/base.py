from abc import ABC, abstractmethod

from aiokafka import ConsumerRecord


class RouterABC(ABC):
    @abstractmethod
    async def route_message(self, message: ConsumerRecord):
        ...
