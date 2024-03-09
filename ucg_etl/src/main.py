import asyncio
import logging.config

from src.clickhouse.client import ClickHouseClient
from src.core.logger import LOGGING
from src.kafka.consumer import KafkaConsumer
from src.message_router import MessageRouter

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Запуск приложения")

    clickhouse_client = ClickHouseClient()
    consumer = KafkaConsumer()
    router = MessageRouter(clickhouse_client)

    try:
        async for messages in consumer.consume_messages():
            for msg in messages:
                await router.route_message(msg)
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке сообщений: {e}")
    finally:
        logger.info("Приложение завершает работу.")


if __name__ == "__main__":
    asyncio.run(main())
