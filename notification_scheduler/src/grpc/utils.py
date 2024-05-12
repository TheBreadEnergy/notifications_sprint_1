import grpc
from google.protobuf.json_format import MessageToDict
from loguru import logger
from src.core.config import settings
from src.grpc.notifications import managers_pb2, managers_pb2_grpc, status_pb2
from src.grpc.notifications.status_pb2 import Status


async def send_notification(notification):
    async with grpc.aio.insecure_channel(settings.notification_grpc) as channel:
        stub = managers_pb2_grpc.ManagerNotificationStub(channel)
        request = managers_pb2.SendNotificationRequest(
            user_ids=[str(user_id) for user_id in notification.user_ids],
            notification_id=str(notification.id),
            template_id=str(notification.template.id),
            subject=notification.subject,
            text=notification.text,
            type=notification.notification_channel_type,
        )
    response: status_pb2.Status = stub.SendNotificationToUsers(request)
    status = Status(**MessageToDict(response))
    logger.info(f"Notification sent. Status: {status}")
    return status
