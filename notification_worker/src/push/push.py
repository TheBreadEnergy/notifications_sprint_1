import logging

import httpx
from src.core.config import settings


async def send_push(user_id: str, content: str, task_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.push_url}{user_id}",
                json={"message": content, "task_id": task_id},
            )
            response.raise_for_status()
    except httpx.HTTPError as error:
        logging.error(f"Ошибка при отправке уведомления через HTTP: {error}")
