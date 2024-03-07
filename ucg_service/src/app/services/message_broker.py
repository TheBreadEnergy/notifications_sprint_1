from abc import ABC, abstractmethod

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
