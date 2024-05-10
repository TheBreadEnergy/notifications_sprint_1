from abc import ABC, abstractmethod


class MessageBrokerABC(ABC):
    @abstractmethod
    async def publish(
        self,
        messages: dict | list,
        routing_key: str,
        message_headers: dict | None = None,
        delay: int | float = 0,
    ) -> bool:
        ...

    @abstractmethod
    async def idempotency_startup(self) -> None:
        ...

    @abstractmethod
    async def idempotency_shutdown(self) -> None:
        ...
