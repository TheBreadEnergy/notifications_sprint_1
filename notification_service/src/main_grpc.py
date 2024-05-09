import asyncio
import logging

import grpc
from src.core.config import settings
from src.core.grpc import auth_pb2_grpc, file_pb2_grpc, managers_pb2_grpc, ucg_pb2_grpc
from src.services.grpc.v1.auth import AuthGrpcNotificationService
from src.services.grpc.v1.films import FilmGrpcNotificationService
from src.services.grpc.v1.managers import ManagerGrpcNotificationService
from src.services.grpc.v1.ucgs import UcgGrpcNotificationService
from src.brokers.rabbit_message_broker import RabbitMessageBroker


async def serve() -> None:
    server = grpc.aio.server()
    broker = RabbitMessageBroker(
        host=settings.rabbit_host,
        port=settings.rabbit_port,
        username=settings.rabbit_login,
        password=settings.rabbit_password,
    )
    try:
        await broker.idempotency_startup()
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
        await broker.idempotency_shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
