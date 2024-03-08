from confluent_kafka import Consumer, KafkaError
from src.core.config import settings


class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer(
            {
                "bootstrap.servers": f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
                "group.id": settings.KAFKA_GROUP,
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe(
            [
                settings.KAFKA_CLICK_TOPIC,
                settings.KAFKA_SEEN_TOPIC,
                settings.KAFKA_VIDEO_TOPIC,
                settings.KAFKA_FILM_TOPIC,
                settings.KAFKA_FILTER_TOPIC,
            ]
        )

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                yield msg
        finally:
            self.consumer.close()
