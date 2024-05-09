import json

import aio_pika
import backoff
from aio_pika import Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractRobustConnection,
    DeliveryMode,
    ExchangeType,
)
from pamqp.commands import Basic
from src.brokers.base import MessageBrokerABC
from src.core.config import ROUTING_KEYS, settings
from src.exceptions.broker import ConnectionIsNotEstablishedException


class RabbitMessageBroker(MessageBrokerABC):
    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._incoming_exchange: AbstractExchange | None = None

    @backoff.on_exception(wait_gen=backoff.expo, max_tries=3, exception=Exception)
    async def publish(
        self,
        messages: dict | list,
        routing_key: str,
        message_headers: dict | None = None,
        delay: int | float = 0,
    ) -> bool:
        if not self._check_availibility():
            raise ConnectionIsNotEstablishedException()

        if isinstance(messages, dict):
            messages = [messages]
        message = Message(
            headers=message_headers or {},
            body=json.dumps(messages).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            expiration=delay,
        )
        result = await self._incoming_exchange.publish(
            message=message, routing_key=routing_key
        )
        return isinstance(result, Basic.Ack)

    @backoff.on_exception(wait_gen=backoff.expo, max_tries=3, exception=Exception)
    async def idempotency_startup(self) -> None:
        self._connection = await aio_pika.connect_robust(
            host=self._host,
            port=self._port,
            login=self._username,
            password=self._password,
        )

        self._channel = await self._connection.channel()

        # Обменник, принимающий все сообщения
        self._incoming_exchange = await self._channel.declare_exchange(
            name=settings.incoming_exchange,
            type=ExchangeType.FANOUT,
            durable=True,
        )
        # Обменник отправляющий в рабочие очереди
        exchange_sorting = await self._channel.declare_exchange(  # noqa: F841
            name=settings.sorting_exchange,
            type=ExchangeType.DIRECT,
            durable=True,
        )

        exchange_retry = await self._channel.declare_exchange(
            name=settings.retry_exchange,
            type=ExchangeType.FANOUT,
            durable=True,
        )

        queue_waiting = await self._channel.declare_queue(
            name=settings.queue_waiting,
            durable=True,
            arguments={"x-dead-letter-exchange": settings.sorting_exchange},
        )
        queue_live = await self._channel.declare_queue(
            name=settings.queue_name,
            durable=True,
            arguments={"x-dead-letter-exchange": settings.retry_exchange},
        )
        queue_retry = await self._channel.declare_queue(
            name=settings.queue_retry,
            durable=True,
            arguments={
                "x-dead-letter-exchange": settings.sorting_exchange,
                "x-message-ttl": settings.default_ttl_ms,
            },
        )
        await queue_waiting.bind(self._incoming_exchange)
        await queue_retry.bind(exchange_retry)
        for version in settings.supported_message_versions:
            for routing_key in ROUTING_KEYS:
                await queue_live.bind(
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
