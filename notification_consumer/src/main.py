import asyncio
import logging.config

from src.consumers.kafka import KafkaConsumer
from src.core.config import TOPICS, settings
from src.core.logger import LOGGING
from src.router.message import MessageRouter
from src.services.grpc import GrpcNotificationService

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Запуск приложения")
    logger.info(
        f"Брокер находится по адресу: {settings.kafka_host}:{settings.kafka_port}"
    )
    grpc_service = GrpcNotificationService(server_dsn=settings.notification_service)
    consumer = KafkaConsumer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
        group_id=settings.kafka_group,
        topics=TOPICS,
    )

    router = MessageRouter(service=grpc_service)

    try:
        async for messages in consumer.consume_batch():
            for msg in messages:
                await router.route_message(msg)
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке сообщений: {e}")
    finally:
        logger.info("Приложение завершает работу.")


if __name__ == "__main__":
    asyncio.run(main())
