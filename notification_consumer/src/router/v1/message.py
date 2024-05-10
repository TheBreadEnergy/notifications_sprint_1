import json
import logging

from aiokafka import ConsumerRecord
from src.core.config import settings
from src.events.films.v1.published import FilmPublishedEvent
from src.events.users.v1.activated import UserActivatedEvent
from src.events.users.v1.no_seen import UserNotSeenEvent
from src.events.users.v1.registered import UserRegisteredEvent
from src.router.base import RouterABC
from src.router.v1 import VERSION
from src.schemas import status
from src.services.base import NotificationServiceABC

logger = logging.getLogger(__name__)


class MessageRouter(RouterABC):
    def __init__(self, service: NotificationServiceABC):
        self._service = service
        self._topic_handler = {
            f"{VERSION}.{settings.film_added_topic}": process_film_added,
            f"{VERSION}.{settings.user_registered_topic}": process_user_registered,
            f"{VERSION}.{settings.user_activated_topic}": process_user_activated,
            f"{VERSION}.{settings.user_no_see_topic}": process_user_no_seen,
        }

    async def route_message(self, message: ConsumerRecord):
        try:
            topic_name = message.topic
            if topic_name in self._topic_handler:
                await self._topic_handler[topic_name](
                    service=self._service, event=message
                )
            else:
                logger.warning(f"Нет обработчика для топика: {topic_name}")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")


async def process_film_added(
    service: NotificationServiceABC, event: ConsumerRecord
) -> status.StatusSchema:
    event = FilmPublishedEvent(**json.loads(event.value.decode("utf-8")))
    return await service.notify_new_film(event=event)


async def process_user_registered(
    service: NotificationServiceABC, event: ConsumerRecord
) -> status.StatusSchema:
    event = UserRegisteredEvent(**json.loads(event.value.decode("utf-8")))
    return await service.notify_registration(event=event)


async def process_user_activated(service, event: ConsumerRecord) -> status.StatusSchema:
    event = UserActivatedEvent(**json.loads(event.value.decode("utf-8")))
    return await service.notify_activation(event=event)


async def process_user_no_seen(service, event: ConsumerRecord) -> status.StatusSchema:
    event = UserNotSeenEvent(**json.loads(event.value.decode("utf-8")))
    return await service.notify_long_seen(event=event)
