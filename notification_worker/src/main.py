import asyncio
import logging

from src.brokers.rabbit_message_broker import RabbitMessageBroker
from src.core.config import settings


async def broker() -> None:
    logging.info("Broker Starting")
    message_broker = RabbitMessageBroker(
        host=settings.rabbit_host,
        port=settings.rabbit_port,
        username=settings.rabbit_login,
        password=settings.rabbit_password,
    )
    try:
        await message_broker.idempotency_startup()
        await message_broker.consume_messages()
    finally:
        await message_broker.idempotency_shutdown()
        logging.info("Broker Shutdown")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(broker())
