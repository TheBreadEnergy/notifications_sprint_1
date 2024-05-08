import datetime

import grpc.aio
from src.brokers.rabbitmq import RabbitConnection
from src.core.config import settings
from src.core.grpc import managers_pb2
from src.core.grpc.managers_pb2_grpc import ManagerNotificationServicer
from src.models.user_notification import NotificationChannelType, NotificationType
from src.services.grpc.v1.base import process_user_notification


class ManagerGrpcNotificationService(ManagerNotificationServicer):
    def __init__(self, message_broker: RabbitConnection):
        self._message_broker = message_broker

    async def SendNotificationToUsers(
        self,
        request: managers_pb2.SendNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> None:
        data = {
            "notification_type": NotificationType.fast_notification,
            "notification_channel_type": NotificationChannelType(request.type),
            "template_id": request.template_id,
            "notification_id": request.notification_id,
            "subject": request.subject,
            "text": request.text,
            "cron_expression": None,
            "execution_time": None,
        }
        await process_user_notification(
            broker=self._message_broker,
            data=data,
            user_ids=list(request.user_ids),
            routing_key=settings.message_routing_key,
            delay=None,
        )

    async def CreateDelayedNotification(
        self, request: managers_pb2.CreateDelayedNotificationRequest, context
    ) -> None:
        data = {
            "notification_type": NotificationType.fast_notification,
            "notification_channel_type": NotificationChannelType(request.type),
            "template_id": request.template_id,
            "notification_id": request.notification_id,
            "subject": request.subject,
            "text": request.text,
            "cron_expression": None,
            "execution_time": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=request.delay),
        }
        await process_user_notification(
            broker=self._message_broker,
            data=data,
            user_ids=list(request.user_ids),
            routing_key=settings.message_routing_key,
            delay=request.delay,
        )
