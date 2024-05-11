from abc import ABC, abstractmethod
from uuid import UUID

from src.core.config import settings
from src.publishers.base import PublisherABC
from src.schemas.events.v1.user import UserActivatedEvent, UserRegisteredEvent


class EventHandlerABC(ABC):
    @abstractmethod
    async def handle_registration(self, user_id: UUID):
        ...

    @abstractmethod
    async def handle_activation(self, user_id: UUID):
        ...


class EventHandler(EventHandlerABC):
    def __init__(self, event_producer: PublisherABC):
        self.event_producer = event_producer

    async def handle_registration(self, user_id: UUID):
        await self.event_producer.publish(
            topic=f"{settings.message_version}.{settings.user_registration}",
            payload=UserRegisteredEvent(user_id=str(user_id), short_url=""),
            key=str(user_id),
        )

    async def handle_activation(self, user_id: UUID):
        await self.event_producer.publish(
            topic=f"{settings.message_version}.{settings.user_activation}",
            payload=UserActivatedEvent(user_id=str(user_id)),
            key=user_id,
        )
