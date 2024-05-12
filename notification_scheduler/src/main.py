import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from croniter import croniter
from loguru import logger
from src.db.functions import fetch_recurring_notifications
from src.grpc.utils import send_notification


async def schedule_notifications():
    notifications = await fetch_recurring_notifications()
    logger.info(f"Fetched {len(notifications)} recurring notifications")
    scheduler = AsyncIOScheduler()
    for notification in notifications:
        cron_schedule = notification.cron_string
        if croniter.is_valid(cron_schedule):
            trigger = CronTrigger.from_crontab(cron_schedule)
            scheduler.add_job(send_notification, trigger, args=[notification])
    return scheduler


async def run_scheduler():
    scheduler = await schedule_notifications()
    scheduler.start()


if __name__ == "__main__":
    logger.info("Recurring notifications scheduler is starting...")
    asyncio.run(run_scheduler())
