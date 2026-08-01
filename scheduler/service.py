"""Scheduler service for Jarvis."""

from __future__ import annotations

from datetime import UTC, datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application

from database.session import AsyncSessionLocal
from database.repositories import ReminderRepository
from utils.logging import get_logger

logger = get_logger(__name__)


async def dispatch_due_reminders(application: Application) -> None:
    """Deliver reminders that are due and mark them as sent."""

    async with AsyncSessionLocal() as session:
        repository = ReminderRepository(session)
        reminders = await repository.due_reminders(datetime.now(tz=UTC))
        for reminder in reminders:
            user = reminder.user
            if user is None:
                continue
            try:
                await application.bot.send_message(chat_id=user.telegram_id, text=f"Reminder: {reminder.title}")
                await repository.mark_sent(reminder.id)
                logger.info("Delivered reminder %s to user %s", reminder.id, user.telegram_id)
            except Exception:  # noqa: BLE001
                logger.exception("Failed to deliver reminder %s", reminder.id)
        await session.commit()


def build_scheduler(application: Application) -> AsyncIOScheduler:
    """Create and configure the background scheduler."""

    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(dispatch_due_reminders, "interval", minutes=1, args=[application], id="dispatch_due_reminders", replace_existing=True)
    return scheduler
