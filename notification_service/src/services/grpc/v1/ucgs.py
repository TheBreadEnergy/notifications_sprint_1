import grpc.aio
from src.brokers.base import MessageBrokerABC
from src.core.config import settings
from src.core.grpc import status_pb2, ucg_pb2
from src.core.grpc.ucg_pb2_grpc import UcgNotificationServicer
from src.models.system_notification import ContentType
from src.schemas.events.v1.user_notification import UserNotificationSchema
from src.services.grpc.v1.base import process_system_notification


class UcgGrpcNotificationService(UcgNotificationServicer):
    def __init__(self, message_broker: MessageBrokerABC):
        self.message_broker = message_broker

    async def SendOldBookmarkedNotification(
        self,
        request: ucg_pb2.OldBookmarkedNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> status_pb2.Status:
        status = await process_system_notification(
            broker=self.message_broker,
            content_type=ContentType.bookmark_expired,
            notification_type=UserNotificationSchema,
            routing_key=settings.bookmark_routing_key,
            data={"user_id": request.user_id},
            key="user_id",
        )
        return status_pb2.Status(
            status=status.code, message=status.message, description=status.description
        )
