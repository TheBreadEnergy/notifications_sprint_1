import asyncio
import logging

import grpc
from src.brokers.rabbit_message_broker import RabbitMessageBroker
from src.core.config import settings
from src.core.grpc import auth_pb2_grpc, file_pb2_grpc, managers_pb2_grpc, ucg_pb2_grpc
from src.services.grpc.v1.auth import AuthGrpcNotificationService
from src.services.grpc.v1.films import FilmGrpcNotificationService
from src.services.grpc.v1.managers import ManagerGrpcNotificationService
from src.services.grpc.v1.ucgs import UcgGrpcNotificationService


async def serve() -> None:
    logging.info("Server starting....")
    server = grpc.aio.server()
    broker = RabbitMessageBroker(
        host=settings.rabbit_host,
        port=settings.rabbit_port,
        username=settings.rabbit_login,
        password=settings.rabbit_password,
    )
    try:
        logging.info("Broker dlx infrastructure starting...")
        await broker.idempotency_startup()
        logging.info("Broker dlx infrastructure setup done")
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
        logging.info("Added active routes")
        server.add_insecure_port(f"[::]:{settings.grpc_port}")
        await server.start()
        logging.info("Server ready to receive requests...")
        await server.wait_for_termination()
    finally:
        await broker.idempotency_shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
