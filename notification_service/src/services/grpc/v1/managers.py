import datetime

import grpc.aio
from src.brokers.base import MessageBrokerABC
from src.core.config import settings
from src.core.grpc import managers_pb2
from src.core.grpc.managers_pb2_grpc import ManagerNotificationServicer
from src.core.grpc.status_pb2 import Status
from src.models.user_notification import NotificationChannelType, NotificationType
from src.services.grpc.v1.base import process_user_notification


class ManagerGrpcNotificationService(ManagerNotificationServicer):
    def __init__(self, message_broker: MessageBrokerABC):
        self._message_broker = message_broker

    async def SendNotificationToUsers(
        self,
        request: managers_pb2.SendNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> Status:
        data = {
            "notification_type": NotificationType.fast_notification,
            "notification_channel_type": NotificationChannelType(request.type),
            "template_id": request.template_id,
            "notification_id": request.notification_id,
            "subject": request.subject,
            "text": request.text,
            "execution_time": None,
        }
        status = await process_user_notification(
            broker=self._message_broker,
            data=data,
            user_ids=list(request.user_ids),
            routing_key=settings.message_routing_key,
        )
        return Status(
            status=status.code, message=status.message, description=status.description
        )

    async def CreateDelayedNotification(
        self, request: managers_pb2.CreateDelayedNotificationRequest, context
    ) -> Status:
        data = {
            "notification_type": NotificationType.fast_notification,
            "notification_channel_type": NotificationChannelType(request.type),
            "template_id": request.template_id,
            "notification_id": request.notification_id,
            "subject": request.subject,
            "text": request.text,
            "execution_time": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=request.delay),
        }
        status = await process_user_notification(
            broker=self._message_broker,
            data=data,
            user_ids=list(request.user_ids),
            routing_key=settings.message_routing_key,
            delay=request.delay,
        )
        return Status(
            status=status.code, message=status.message, description=status.description
        )
