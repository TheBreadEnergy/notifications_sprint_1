import json
import asyncio
import logging.config

from src.message_router import MessageRouter
from src.clickhouse.client import ClickHouseClient
from src.kafka.consumer import KafkaConsumer
from src.core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Запуск приложения")
    consumer = KafkaConsumer()
    clickhouse_client = ClickHouseClient()
    router = MessageRouter(clickhouse_client)

    async for msg in consumer.consume_messages():
        topic_name = msg.topic
        try:
            message = json.loads(msg.value.decode("utf-8"))
            logger.info(f"topic: {topic_name}")
            logger.info(f"message: {message}")
            await router.route_message(message, topic_name, msg)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")


if __name__ == "__main__":
    asyncio.run(main())
