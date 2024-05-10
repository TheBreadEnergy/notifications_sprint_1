from abc import ABC, abstractmethod

from src.events.films.v1.published import FilmPublishedEvent
from src.events.users.v1.activated import UserActivatedEvent
from src.events.users.v1.no_seen import UserNotSeenEvent
from src.events.users.v1.registered import UserRegisteredEvent
from src.schemas.status import StatusSchema


class NotificationServiceABC(ABC):
    @abstractmethod
    async def notify_registration(self, event: UserRegisteredEvent) -> StatusSchema:
        ...

    @abstractmethod
    async def notify_activation(self, event: UserActivatedEvent) -> StatusSchema:
        ...

    @abstractmethod
    async def notify_long_seen(self, event: UserNotSeenEvent) -> StatusSchema:
        ...

    @abstractmethod
    async def notify_new_film(self, event: FilmPublishedEvent) -> StatusSchema:
        ...
