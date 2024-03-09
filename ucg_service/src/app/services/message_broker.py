from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer
from confluent_kafka import Producer
from src.config import Config


class MessageBrokerService(ABC):
    @abstractmethod
    def publish(self, topic: str, key: str, message: str):
        ...


class KafkaMessageBrokerService(MessageBrokerService):
    def __init__(self, producer: Producer):
        self._producer = producer

    def publish(self, topic: str, key: str, message: str):
        self._producer.produce(
            topic=topic,
            key=key,
            value=message,
        )


class AioKafkaMessageBrokerService(MessageBrokerService):
    """Плохой дизайн построения асинхронного обмена общения.
    При каждом сообщении плодится producer, что не есть хорошо
    """

    def __init__(
        self,
        bootstrap_server: str = Config.BOOTSTRAP_SERVERS,
        retry_backoff: int = Config.RETRY_BACKOFF_MS,
    ):
        self._bootstrap_server = bootstrap_server
        self._retry_backoff = retry_backoff

    async def publish(self, topic: str, key: str, message: str):
        producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_server,
            retry_backoff_ms=self._retry_backoff,
        )
        await producer.start()
        try:
            await producer.send(topic=topic, key=key, value=message.encode())
        finally:
            await producer.stop()
