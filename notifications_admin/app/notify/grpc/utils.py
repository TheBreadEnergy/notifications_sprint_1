import grpc
from django.conf import settings
from django.utils import timezone
from django_currentuser.middleware import get_current_user
from notify.grpc import managers_pb2, managers_pb2_grpc


class GrpcClient:
    @staticmethod
    def send_instant_notification(notification):
        with grpc.insecure_channel(settings.NOTIFICATION_SERVICE_GRPC) as channel:
            stub = managers_pb2_grpc.ManagerNotificationStub(channel)
            request = managers_pb2.SendNotificationRequest(
                manager_id=str(get_current_user().id),
                user_ids=[str(user_id) for user_id in notification.user_ids],
                notification_id=str(notification.id),
                template_id=str(notification.template.id),
                subject=notification.subject,
                text=notification.text,
                type=notification.notification_channel_type,
            )
            return stub.SendNotificationToUsers(request)

    @staticmethod
    def create_scheduled_notification(notification):
        with grpc.insecure_channel(settings.NOTIFICATION_SERVICE_GRPC) as channel:
            stub = managers_pb2_grpc.ManagerNotificationStub(channel)
            request = managers_pb2.CreateDelayedNotificationRequest(
                manager_id=str(get_current_user().id),
                user_ids=[str(user_id) for user_id in notification.user_ids],
                notification_id=str(notification.id),
                template_id=str(notification.template.id),
                subject=notification.subject,
                text=notification.text,
                type=notification.notification_channel_type,
                delay=int((notification.scheduled_at - timezone.now()).total_seconds()),
            )
            return stub.CreateDelayedNotification(request)
