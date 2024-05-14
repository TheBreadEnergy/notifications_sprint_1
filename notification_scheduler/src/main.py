import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from croniter import croniter
from loguru import logger
from src.core.config import settings
from src.db.functions import (
    fetch_recurring_notifications,
    update_recurring_notification,
)
from src.grpc.utils import send_notification


async def schedule_notifications():
    notifications = await fetch_recurring_notifications()
    started_time = datetime.datetime.now(datetime.timezone.utc)
    logger.info(
        f"Fetched {len(notifications)} recurring notifications at time  {started_time}"
    )
    triggered_notifications = []
    for notification in notifications:
        cron_schedule = notification.cron_string
        last_notification = (
            notification.last_notified
            if notification.last_notified
            else notification.created
        )
        if croniter.is_valid(cron_schedule):
            cron = croniter(cron_schedule, last_notification)
            logger.info("Validate incoming task for execution")
            next_time_to_trigger = cron.get_next(datetime.datetime)
            print(
                abs(next_time_to_trigger - datetime.datetime.now(datetime.timezone.utc))
            )
            if abs(
                next_time_to_trigger - datetime.datetime.now(datetime.timezone.utc)
            ) <= datetime.timedelta(seconds=settings.delta):
                logger.info(
                    f"Task: {notification.id} with next time "
                    f"execution {next_time_to_trigger}  will be executed. "
                )
                await send_notification(notification)
                triggered_notifications.append(notification)
                await update_recurring_notification(
                    triggered_notifications, notification_date=started_time
                )


async def run_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(schedule_notifications, "interval", seconds=settings.interval)
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


async def main():
    logger.info("Recurring notifications scheduler is starting...")
    _ = asyncio.create_task(run_scheduler())
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        ...
