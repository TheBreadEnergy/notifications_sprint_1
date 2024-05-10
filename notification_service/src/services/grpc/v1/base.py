import logging
import uuid
from typing import Type
from uuid import UUID

from grpc import StatusCode
from pydantic import BaseModel
from src.brokers.base import MessageBrokerABC
from src.db.postgres import async_session
from src.models.base import NotificationStatus
from src.models.system_notification import ContentType, SystemNotificationTask
from src.models.user_notification import UserNotificationTask
from src.schemas.events.errors import QueueError
from src.schemas.events.status import Status
from src.schemas.events.v1.send_message import SendMessageSchema
from src.services.grpc.v1 import PREFIX


async def process_system_notification(
    broker: MessageBrokerABC,
    content_type: ContentType,
    notification_type: Type[BaseModel],
    routing_key: str,
    data: dict,
    key: str = "user_id",
) -> Status:
    logging.info("Start database session")
    exception = False
    async with async_session() as session:
        try:
            if key not in data:
                raise KeyError(f"{key} missed in data!")
            event = SystemNotificationTask(
                content_type=content_type,
                content_id=data[key],
                status=NotificationStatus.started,
            )
            session.add(event)
            await session.commit()
            data["task_id"] = str(event.id)
            notification = notification_type(**data)
            logging.info("Send notification to message broker")
            published = await broker.publish(
                messages=notification.model_dump(),
                routing_key=f"{PREFIX}.{routing_key}",
            )
            if published:
                logging.info("Notification published successfully")
                event.status = NotificationStatus.in_progress
                logging.info("Message task change state to successfull")
            else:
                logging.error("Notification not published successfully")
                event.status = NotificationStatus.pending
                logging.info("Message task change state to cancelled")
            await session.commit()
        except Exception as e:
            exception = Status(
                code=StatusCode.INTERNAL, message=str(e), description=[str(e)]
            )
        finally:
            await session.close()
    if exception:
        return exception
    if published:
        return Status(code=StatusCode.OK, message="", description=[])
    else:
        return Status(code=StatusCode.CANCELLED, **QueueError().model_dump())


async def process_user_notification(
    broker: MessageBrokerABC,
    data: dict,
    routing_key: str,
    user_ids: list[str],
    delay: int | float = 0,
) -> Status:
    logging.info("Start user notification task process")
    status = Status(code=StatusCode.OK, message="", description=[])
    async with async_session() as session:
        try:
            for user_id in user_ids:
                logging.info("Build specific user notification task")
                event = UserNotificationTask(user_id=UUID(user_id), **data)
                event.id = uuid.uuid4()
                event.status = NotificationStatus.started
                published = await process_user_task(
                    broker=broker,
                    event=event,
                    routing_key=routing_key,
                    delay=delay,
                )
                if published:
                    event.status = NotificationStatus.in_progress
                else:
                    event.status = NotificationStatus.pending
                session.add(event)
            await session.commit()
        except Exception as e:
            status = Status(
                code=StatusCode.INTERNAL, message=str(e), description=[str(e)]
            )
        finally:
            await session.close()
    return status


async def process_user_task(
    broker: MessageBrokerABC,
    event: UserNotificationTask,
    routing_key: str,
    delay: int | float = 0,
) -> bool:
    message = SendMessageSchema(
        user_id=str(event.user_id),
        task_id=str(event.id),
        notification_channel_type=event.notification_channel_type,
        notification_id=str(event.notification_id),
        template_id=str(event.template_id),
        subject=event.subject,
        text=event.text,
    )
    logging.info(
        f"Send notication to message broker to the route {PREFIX}.{routing_key}"
    )
    try:
        published = await broker.publish(
            messages=message.model_dump(),
            routing_key=f"{PREFIX}.{routing_key}",
            delay=delay,
        )
        if published:
            logging.info("Notification published successfully")
        else:
            logging.error("Notification not published successfully")
            return published
    except Exception as e:
        logging.error(e)
        event.status = NotificationStatus.cancelled
        return False
