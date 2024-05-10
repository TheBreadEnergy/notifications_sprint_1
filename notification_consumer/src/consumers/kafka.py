from aiokafka import AIOKafkaConsumer
from src.consumers.base import ConsumerABC
from src.core.config import TOPICS, settings


class KafkaConsumer(ConsumerABC):
    def __init__(
        self,
        bootstrap_servers: str = f"{settings.kafka_host}:{settings.kafka_port}",
        group_id: str = settings.kafka_group,
        topics: list[str] | None = None,
    ):
        if not topics:
            topics = TOPICS
        self._consumer = AIOKafkaConsumer(
            *topics, bootstrap_servers=bootstrap_servers, group_id=group_id
        )

    async def consume_batch(self, max_record: int = 1000, timeout_ms: int = 1000):
        await self._consumer.start()
        try:
            while True:
                result = await self._consumer.getmany(
                    timeout_ms=timeout_ms, max_records=max_record
                )
                for tp, messages in result.items():
                    yield messages
        finally:
            await self._consumer.stop()
