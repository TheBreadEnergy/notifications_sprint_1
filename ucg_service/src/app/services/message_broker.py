from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer
from confluent_kafka import Producer


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
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def publish(self, topic: str, key: str, message: str):
        await self._producer.send(topic=topic, key=key, value=message.encode())
