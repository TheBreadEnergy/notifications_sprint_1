import json
import uuid
from dataclasses import dataclass

from aio_pika import Message, connect_robust
from aio_pika.abc import (
    AbstractRobustChannel,
    AbstractRobustConnection,
    AbstractRobustExchange,
    DeliveryMode,
    ExchangeType,
)
from src.core.config import settings


@dataclass
class RabbitConnection:
    _connection: AbstractRobustConnection | None = None
    _channel: AbstractRobustChannel | None = None
    _exchange: AbstractRobustExchange | None = None

    async def _clear(self) -> None:
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self.connection = None
        self.channel = None

    async def connect(self, host: str | None = None) -> None:
        try:
            if not host:
                host = f"amqp://{settings.rabbit_login}:{settings.rabbit_password}@"
                f"{settings.rabbit_host}:{settings.rabbit_port}"
            self._connection = await connect_robust(host)
            self._channel = await self.connection.channel(publisher_confirms=False)
            self._exchange = await self.channel.declare_exchange(
                settings.delayed_exchange,
                ExchangeType.X_DELAYED_MESSAGE,
                arguments={"x-delayed-type": "direct"},
                durable=True,
            )
            await self._channel.declare_queue(name=settings.queue_name, durable=True)
        except Exception as e:
            await self._clear()
            raise e

    async def disconnect(self) -> None:
        await self._clear()

    async def send_messages(
        self, messages: list | dict, routing_key: str, delay: int | None = None
    ) -> None:
        if not self.channel:
            raise RuntimeError(
                "The message could not be sent because"
                " the connection with RabbitMQ is not established"
            )
        if isinstance(messages, dict):
            messages = [messages]
        async with self.channel.transaction():
            headers = None
            if delay:
                headers = {"x-delay": delay * 1000, "X-Request-Id": str(uuid.uuid4())}
            for message in messages:
                message = Message(
                    body=json.dumps(message).encode(),
                    headers=headers,
                    delivery_mode=DeliveryMode.PERSISTENT,
                )
                await self._exchange.publish(
                    message, routing_key=routing_key, mandatory=False if delay else True
                )


rabbit_connection: RabbitConnection | None = None


async def get_rabbit_connection() -> RabbitConnection:
    return rabbit_connection
