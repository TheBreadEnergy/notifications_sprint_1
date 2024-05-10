import aio_pika
import backoff
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractRobustConnection,
)

from src.brokers.base import MessageBrokerABC


class RabbitMessageBroker(MessageBrokerABC):
    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._incoming_exchange: AbstractExchange | None = None

    async def consume_messages(self, queue_name, callback):
        if not self._channel or self._connection.is_closed:
            raise Exception("Соединение или канал недоступны")

        queue = await self._channel.declare_queue(queue_name, durable=True)

        async for message in queue:
            async with message.process():
                await callback(message)

    @backoff.on_exception(wait_gen=backoff.expo, max_tries=3, exception=Exception)
    async def idempotency_startup(self) -> None:
        self._connection = await aio_pika.connect_robust(
            host=self._host,
            port=self._port,
            login=self._username,
            password=self._password,
        )

        self._channel = await self._connection.channel()

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
