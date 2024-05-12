import datetime

from loguru import logger
from sqlmodel import select
from src.db.postgres import async_session
from src.models.notification import RecurringNotification


async def fetch_recurring_notifications():
    async with async_session() as session:
        query = select(RecurringNotification)
        result = await session.execute(query)
        return result.scalars().all()


async def update_recurring_notification(
    reccuring: list[RecurringNotification], notification_date: datetime.datetime
):
    async with async_session() as session:
        try:
            for notification in reccuring:
                notification.last_notified = notification_date
            await session.commit()
            logger.info(
                f"Сохранение даты последней отправки уведомлений: {notification_date}"
            )
        except Exception as e:
            await session.rollback()
            logger.error(str(e))
