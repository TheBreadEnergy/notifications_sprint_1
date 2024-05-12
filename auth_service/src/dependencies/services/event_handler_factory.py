from functools import cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from src.brokers.kafka import get_producer
from src.dependencies.registrator import add_factory_to_mapper
from src.publishers.kafka import KafkaPublisher
from src.services.event_handler import EventHandler, EventHandlerABC


@add_factory_to_mapper(EventHandlerABC)
@cache
def create_event_handler(
    kafka_broker: AIOKafkaProducer = Depends(get_producer),
) -> EventHandler:
    return EventHandler(event_producer=KafkaPublisher(kafka_producer=kafka_broker))
