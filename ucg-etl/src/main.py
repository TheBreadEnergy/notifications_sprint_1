import json

from message_router import MessageRouter
from src.clickhouse.client import ClickHouseClient
from src.kafka.consumer import KafkaConsumer


def main():
    consumer = KafkaConsumer()
    clickhouse_client = ClickHouseClient()
    router = MessageRouter(clickhouse_client)

    for msg in consumer.consume_messages():
        if msg.error():
            print(f"Kafka error: {msg.error()}")
            continue
        topic_name = msg.topic()
        message = json.loads(msg.value().decode("utf-8"))
        router.route_message(message, topic_name, msg)


if __name__ == "__main__":
    main()
