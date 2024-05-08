from typing import Type
from uuid import UUID

from pydantic import BaseModel
from src.brokers.rabbitmq import RabbitConnection
from src.core.config import settings
from src.db.postgres import async_session
from src.models.base import NotificationStatus
from src.models.system_notification import ContentType, SystemNotificationTask
from src.models.user_notification import UserNotificationTask
from src.schemas.events.v1.send_message import SendMessageSchema
from src.services.grpc.v1 import VERSION


async def process_system_notification(
    broker: RabbitConnection,
    content_type: ContentType,
    notification_type: Type[BaseModel],
    routing_key: str,
    data: dict,
    key: str = "user_id",
) -> None:
    async with async_session() as session:
        try:
            if key not in data:
                raise KeyError(f"{key} missed in data!")
            event = SystemNotificationTask(
                content_type=content_type, content_id=data[key]
            )
            session.add(event)
            data["task_id"] = event.id
            notification = notification_type(**data)
            await broker.send_messages(
                messages=notification.model_dump(),
                routing_key=f"{settings.routing_prefix}.{VERSION}.{routing_key}",
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def process_user_notification(
    broker: RabbitConnection,
    data: dict,
    routing_key: str,
    user_ids: list[str],
    delay: int | None = None,
) -> None:
    async with async_session() as session:
        try:
            messages = []
            for user_id in user_ids:
                event = UserNotificationTask(user_id=UUID(user_id), **data)
                message = SendMessageSchema(
                    user_id=event.user_id,
                    task_id=event.id,
                    notification_id=event.notification_id,
                    template_id=event.template_id,
                    subject=event.subject,
                    text=event.text,
                )
                messages.append(message)
                event.status = NotificationStatus.in_progress
                session.add(event)

            for indx in range(0, len(messages), settings.batch_size):
                await broker.send_messages(
                    messages=messages[indx : indx + settings.batch_size],
                    routing_key=f"{settings.routing_prefix}.{VERSION}.{routing_key}",
                    delay=delay,
                )
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
