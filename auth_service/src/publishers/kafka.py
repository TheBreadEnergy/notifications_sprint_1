from aiokafka import AIOKafkaProducer
from src.publishers.base import PublisherABC
from src.schemas.events.base import BaseEvent


class KafkaPublisher(PublisherABC):
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self._kafka_producer = kafka_producer

    async def publish(self, topic: str, payload: BaseEvent, key: str | None = None):
        async with self._kafka_producer.transaction():
            _ = await self._kafka_producer.send_and_wait(
                topic=topic,
                key=str(key).encode(),
                value=payload.model_dump_json().encode(),
            )
