from sqlmodel import select
from src.db.postgres import async_session
from src.models.notification import RecurringNotification


async def fetch_recurring_notifications():
    async with async_session() as session:
        query = select(RecurringNotification)
        result = await session.execute(query)
        return result.scalars().all()
