from abc import ABC, abstractmethod


class ConsumerABC(ABC):
    @abstractmethod
    async def consume_batch(self, max_record: int):
        ...
