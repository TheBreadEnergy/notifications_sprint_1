import json
import logging
import re

from src.core.config import settings
from src.db.functions import get_template_by_id, get_user_by_id
from src.mail.send import send_email
from src.models.user_notification import NotificationChannelType
from src.render.render import render_template


# Задачи обработки для каждого типа ключа
async def handle_manager_message(data):
    logging.info(data)
    user = await get_user_by_id(data["user_id"])
    template = await get_template_by_id(data["template_id"])
    rendered_content = await render_template(template.layout, {"user": user})
    logging.info(rendered_content)
    if data["notification_channel_type"] == NotificationChannelType.email:
        await send_email(user, rendered_content, data["subject"])
    if data["notification_channel_type"] == NotificationChannelType.push:
        ...


async def handle_register(data):
    ...


async def handle_film_published(data):
    ...


async def process_message(message):
    message_data = json.loads(message.body)
    routing_key = message.routing_key

    # Разбор ключа маршрутизации
    match = re.match(
        rf"^{re.escape(settings.routing_prefix)}\.(\w+)\.([\w-]+)$", routing_key
    )
    if not match:
        logging.error(f"Неверный формат ключа маршрутизации: {routing_key}")
        return

    version = match.group(1)
    actual_routing_key = match.group(2)

    # Составной ключ для поиска обработчика
    handler = handlers.get((version, actual_routing_key))
    if handler:
        try:
            await handler(message_data)
        except Exception as e:
            logging.error(f"Ошибка при обработке сообщения: {e}")
    else:
        logging.error(
            f"Неизвестный ключ маршрутизации или версия: "
            f"{actual_routing_key}, версия: {version}"
        )


handlers = {}
for version in settings.supported_message_versions:
    handlers.update(
        {
            (version, settings.register_routing_key): handle_register,
            (version, settings.activating_routing_key): handle_manager_message,
            (version, settings.long_no_see_routing_key): handle_manager_message,
            (version, settings.film_routing_key): handle_film_published,
            (version, settings.bookmark_routing_key): handle_manager_message,
            (version, settings.message_routing_key): handle_manager_message,
        }
    )
