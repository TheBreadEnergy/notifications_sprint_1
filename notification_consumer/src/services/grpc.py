import backoff
import grpc.aio
from google.protobuf.json_format import MessageToDict
from src.events.films.v1.published import FilmPublishedEvent
from src.events.users.v1.activated import UserActivatedEvent
from src.events.users.v1.no_seen import UserNotSeenEvent
from src.events.users.v1.registered import UserRegisteredEvent
from src.grpc.models import auth_pb2, file_pb2, status_pb2
from src.grpc.models.status_pb2 import Status
from src.grpc.services import auth_pb2_grpc, file_pb2_grpc
from src.services.base import NotificationServiceABC


class GrpcNotificationService(NotificationServiceABC):
    def __init__(self, server_dsn: str):
        self.server_dsn = server_dsn

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception, max_tries=3)
    async def notify_registration(self, event: UserRegisteredEvent) -> Status:
        async with grpc.aio.insecure_channel(self.server_dsn) as channel:
            stub = auth_pb2_grpc.UserNotificationStub(channel)
            request = auth_pb2.UserRegisteredNotificationRequest(
                user_id=event.user_id,
                short_url=event.short_url,
            )
            response: status_pb2.Status = await stub.SendRegistrationNotification(
                request
            )
        return Status(**MessageToDict(response))

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception, max_tries=3)
    async def notify_activation(self, event: UserActivatedEvent) -> Status:
        async with grpc.aio.insecure_channel(self.server_dsn) as channel:
            stub = auth_pb2_grpc.UserNotificationStub(channel)
            request = auth_pb2.UserActivatedAccountNotificationRequest(
                user_id=event.user_id
            )
            response: status_pb2.Status = await stub.SendActivationNotification(request)
        return Status(**MessageToDict(response))

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception, max_tries=3)
    async def notify_long_seen(self, event: UserNotSeenEvent) -> Status:
        async with grpc.aio.insecure_channel(self.server_dsn) as channel:
            stub = auth_pb2_grpc.UserNotificationStub(channel)
            request = auth_pb2.UserLongNoSeeNotificationRequest(user_id=event.user_id)
            response: status_pb2.Status = await stub.SendLongNoSeeNotification(request)
        return Status(**MessageToDict(response))

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception, max_tries=3)
    async def notify_new_film(self, event: FilmPublishedEvent) -> Status:
        async with grpc.aio.insecure_channel(self.server_dsn) as channel:
            stub = file_pb2_grpc.FilmNotificationStub(channel)
            request = file_pb2.FilmUploadedNotificationRequest(film_id=event.film_id)
            response: status_pb2.Status = await stub.SendFilmNotification(request)
        return Status(**MessageToDict(response))
