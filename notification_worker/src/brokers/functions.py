import json
import logging

from src.core.config import settings
from src.db.functions import get_user_by_id, get_template_by_id
from src.mail.send import send_email_via_sendgrid
from src.render.render import render_template


# Задачи обработки для каждого типа ключа
async def handle_manager_message(data):
    logging.info(data)
    user = await get_user_by_id(data["user_id"])
    template = await get_template_by_id(data['template_id'])
    rendered_content = await render_template(template.layout, {'user': user})
    logging.info(rendered_content)
    await send_email_via_sendgrid(
        to_email=user.email,
        subject=data['subject'],
        content=rendered_content,
        from_email="your-email@example.com"
    )


async def handle_register(data):
    ...


async def handle_film_published(data):
    ...


async def process_message(message):
    message_data = json.loads(message.body)
    routing_key = message.routing_key

    handler = handlers.get(routing_key)
    if handler:
        try:
            await handler(message_data)
        except Exception as e:
            logging.error(e)
    else:
        logging.error(f"Неизвестный ключ маршрутизации: {routing_key}")


handlers = {
    settings.register_routing_key: handle_register,
    settings.activating_routing_key: handle_manager_message,
    settings.long_no_see_routing_key: handle_manager_message,
    settings.film_routing_key: handle_film_published,
    settings.bookmark_routing_key: handle_manager_message,
    settings.message_routing_key: handle_manager_message,
}
