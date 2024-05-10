from abc import ABC, abstractmethod


class MessageBrokerABC(ABC):
    @abstractmethod
    async def idempotency_shutdown(self) -> None:
        ...
