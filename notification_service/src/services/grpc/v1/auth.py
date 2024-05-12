import logging

import grpc
from src.brokers.base import MessageBrokerABC
from src.core.config import settings
from src.core.grpc import auth_pb2, status_pb2
from src.core.grpc.auth_pb2_grpc import UserNotificationServicer
from src.core.grpc.status_pb2 import Status
from src.models.system_notification import ContentType
from src.schemas.events.v1.user_notification import UserNotificationSchema
from src.services.grpc.v1.base import process_system_notification


class AuthGrpcNotificationService(UserNotificationServicer):
    def __init__(self, rabbit_connection: MessageBrokerABC):
        self.rabbit_connection = rabbit_connection

    async def SendRegistrationNotification(
        self,
        request: auth_pb2.UserRegisteredNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> status_pb2.Status:
        logging.info("Processing registration notification task sending")
        status = await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_registered,
            notification_type=UserNotificationSchema,
            routing_key=settings.register_routing_key,
            data={"user_id": request.user_id},
        )
        logging.info(
            f"Registration notification task sending completed"
            f" with status code: {status.code}"
        )
        return status_pb2.Status(
            status=status.code,
            message=status.message,
            description=status.description,
        )

    async def SendActivationNotification(
        self,
        request: auth_pb2.UserActivatedAccountNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> status_pb2.Status:
        logging.info("Processing activation user account notification task sending")
        status = await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_activated,
            notification_type=UserNotificationSchema,
            routing_key=settings.activation_routing_key,
            data={"user_id": request.user_id},
        )
        logging.info(
            f"Activation user account notification"
            f" task completed with status code: {status.code}"
        )
        return status_pb2.Status(
            status=status.code, message=status.message, description=status.description
        )

    async def SendLongNoSeeNotification(
        self,
        request: auth_pb2.UserLongNoSeeNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> Status:
        logging.info("Processing user no seen notification task sending")
        status = await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.user_deactivated,
            notification_type=UserNotificationSchema,
            routing_key=settings.long_notification_routing_key,
            data={"user_id": request.user_id},
        )
        logging.info(
            f"User no seen notification task completed with status code: {status.code}"
        )
        return status_pb2.Status(
            status=status.code, message=status.message, description=status.description
        )
