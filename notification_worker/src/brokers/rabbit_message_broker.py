import aio_pika
import backoff
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractRobustConnection,
    AbstractRobustQueue,
    ExchangeType,
)
from src.brokers.base import MessageBrokerABC
from src.brokers.functions import process_message
from src.core.config import ROUTING_KEYS, settings


class RabbitMessageBroker(MessageBrokerABC):
    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._incoming_exchange: AbstractExchange | None = None
        self.queue: AbstractRobustQueue | None = None

    async def consume_messages(self):
        if not self._channel or self._connection.is_closed:
            raise Exception("Соединение или канал недоступны")

        async for message in self.queue:
            async with message.process():
                await process_message(message)

    @backoff.on_exception(wait_gen=backoff.expo, max_tries=3, exception=Exception)
    async def idempotency_startup(self) -> None:
        self._connection = await aio_pika.connect_robust(
            host=self._host,
            port=self._port,
            login=self._username,
            password=self._password,
        )

        self._channel = await self._connection.channel()

        # Обменник отправляющий в рабочие очереди
        exchange_sorting = await self._channel.declare_exchange(  # noqa: F841
            name=settings.sorting_exchange,
            type=ExchangeType.DIRECT,
            durable=True,
        )

        self.queue = await self._channel.declare_queue(
            name=settings.queue_name,
            durable=True,
            arguments={"x-dead-letter-exchange": settings.retry_exchange},
        )

        for version in settings.supported_message_versions:
            for routing_key in ROUTING_KEYS:
                await self.queue.bind(
                    exchange_sorting,
                    f"{settings.routing_prefix}.{version}.{routing_key}",
                )

    def _check_availibility(self) -> bool:
        return (
                self._connection
                and not self._connection.is_closed
                and self._channel
                and not self._channel.is_closed
        )

    async def idempotency_shutdown(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
