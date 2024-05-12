import logging

import sendgrid
from python_http_client.exceptions import HTTPError
from sendgrid.helpers.mail import Mail
from src.core.config import settings
from src.models.user import User


async def send_email_via_sendgrid(
        to_email: str, subject: str, content: str, from_email: str
):
    """
    Отправляет email через SendGrid.
    :param to_email: Email получателя.
    :param subject: Тема сообщения.
    :param content: HTML содержимое письма.
    :param from_email: Email отправителя.
    """
    sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
    message = Mail(
        from_email=from_email, to_emails=to_email, subject=subject, html_content=content
    )

    try:
        response = await sg.send(message)
        logging.info(f"Статус отправки: {response.status_code}")
    except HTTPError as e:
        logging.exception(f"Ошибка при отправке сообщения: {e.to_dict}")
        logging.exception(e.body)


async def send_email(user: User, content: str, subject: str):
    await send_email_via_sendgrid(
        to_email=user.email,
        subject=subject,
        content=content,
        from_email=settings.host_email,
    )
