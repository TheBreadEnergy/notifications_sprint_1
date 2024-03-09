from aiokafka import AIOKafkaConsumer
from src.core.config import settings


class KafkaConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_CLICK_TOPIC,
            settings.KAFKA_SEEN_TOPIC,
            settings.KAFKA_VIDEO_TOPIC,
            settings.KAFKA_FILM_TOPIC,
            settings.KAFKA_FILTER_TOPIC,
            bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
            group_id=settings.KAFKA_GROUP,
        )

    async def consume_messages(self):
        await self.consumer.start()
        try:
            while True:
                result = await self.consumer.getmany(timeout_ms=1000, max_records=1000)
                for tp, messages in result.items():
                    yield messages
        finally:
            await self.consumer.stop()
