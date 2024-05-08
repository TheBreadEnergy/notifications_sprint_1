import grpc.aio
from src.brokers.rabbitmq import RabbitConnection
from src.core.config import settings
from src.core.grpc import file_pb2
from src.core.grpc.file_pb2_grpc import FilmNotificationServicer
from src.models.system_notification import ContentType
from src.schemas.events.v1.film_notification import FilmNotificationSchema
from src.services.grpc.v1.base import process_system_notification


class FilmGrpcNotificationService(FilmNotificationServicer):
    def __init__(self, rabbit_connection: RabbitConnection):
        self.rabbit_connection = rabbit_connection

    async def SendFilmNotification(
        self,
        request: file_pb2.FilmUploadedNotificationRequest,
        context: grpc.aio.ServicerContext,
    ) -> None:
        await process_system_notification(
            broker=self.rabbit_connection,
            content_type=ContentType.film_published,
            notification_type=FilmNotificationSchema,
            routing_key=settings.film_routing_key,
            data={"film_id": request.film_id},
            key="film_id",
        )
