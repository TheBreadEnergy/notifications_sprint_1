import grpc
from google.protobuf import empty_pb2
from src.brokers.rabbitmq import RabbitConnection
from src.core.config import settings
from src.core.grpc import auth_pb2
from src.core.grpc.auth_pb2_grpc import UserNotificationServicer
from src.models.system_notification import ContentType
from src.schemas.events.v1.user_notification import UserNotificationSchema
from src.services.grpc.v1.base import process_system_notification


class AuthGrpcNotificationService(UserNotificationServicer):
    def __init__(self, rabbit_connection: RabbitConnection):
        self.rabbit_connection = rabbit_connection

    async def SendRegistrationNotification(
        self,
        request: auth_pb2.UserRegisteredNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> None:
        await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_registered,
            notification_type=UserNotificationSchema,
            routing_key=settings.register_routing_key,
            data={"user_id": request.user_id},
        )
        return empty_pb2.Empty()

    async def SendActivationNotification(
        self,
        request: auth_pb2.UserActivatedAccountNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> None:
        await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_activated,
            notification_type=UserNotificationSchema,
            routing_key=settings.activation_routing_key,
            data={"user_id": request.user_id},
        )
        return empty_pb2.Empty()

    async def SendLongNoSeeNotification(
        self,
        request: auth_pb2.UserLongNoSeeNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> None:
        await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_deactivated,
            notification_type=UserNotificationSchema,
            routing_key=settings.long_notification_routing_key,
            data={"user_id": request.user_id},
        )
        return empty_pb2.Empty()
