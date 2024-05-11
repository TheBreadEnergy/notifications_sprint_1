from aiokafka import AIOKafkaProducer

kafka_producer: AIOKafkaProducer | None = None


async def get_producer() -> AIOKafkaProducer | None:
    return kafka_producer
