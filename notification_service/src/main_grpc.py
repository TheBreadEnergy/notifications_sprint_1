import asyncio
import logging

import grpc
from core.config import settings
from core.grpc import auth_pb2_grpc, file_pb2_grpc, managers_pb2_grpc, ucg_pb2_grpc
from services.grpc.v1.auth import AuthGrpcNotificationService
from services.grpc.v1.films import FilmGrpcNotificationService
from services.grpc.v1.managers import ManagerGrpcNotificationService
from services.grpc.v1.ucgs import UcgGrpcNotificationService
from src.brokers.rabbitmq import RabbitConnection


async def serve() -> None:
    server = grpc.aio.server()
    broker = RabbitConnection()
    try:
        await broker.connect(
            host=f"amqp://{settings.rabbit_login}:{settings.rabbit_password}@"
            f"{settings.rabbit_host}:{settings.rabbit_port}"
        )
        auth_pb2_grpc.add_UserNotificationServicer_to_server(
            AuthGrpcNotificationService(rabbit_connection=broker), server
        )
        file_pb2_grpc.add_FilmNotificationServicer_to_server(
            FilmGrpcNotificationService(rabbit_connection=broker), server
        )
        managers_pb2_grpc.add_ManagerNotificationServicer_to_server(
            ManagerGrpcNotificationService(message_broker=broker), server
        )
        ucg_pb2_grpc.add_UcgNotificationServicer_to_server(
            UcgGrpcNotificationService(message_broker=broker), server
        )
        server.add_insecure_port(f"[::]:{settings.grpc_port}")
        await server.start()
        await server.wait_for_termination()
    finally:
        await broker.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
