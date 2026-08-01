"""Telegram reminder command handlers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from database.models import Reminder
from database.session import AsyncSessionLocal
from services.reminders import ReminderService
from services.users import UserService


def _parse_duration_minutes(payload: str) -> tuple[str, int]:
    """Parse reminder title and minutes offset."""

    parts = [part.strip() for part in payload.split("|", 1)]
    title = parts[0] if parts else ""
    minutes = 0
    if len(parts) == 2 and parts[1]:
        try:
            minutes = int(parts[1])
        except ValueError:
            minutes = 0
    return title, minutes


async def create_reminder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a reminder using title | minutes."""

    if update.message is None or update.effective_user is None:
        return

    payload = " ".join(context.args).strip()
    title, minutes = _parse_duration_minutes(payload)
    if not title or minutes <= 0:
        await update.message.reply_text("Usage: /remind title | minutes_from_now")
        return

    remind_at = datetime.now(tz=UTC) + timedelta(minutes=minutes)

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        session.add(Reminder(user_id=user_id, title=title, remind_at=remind_at))
        await session.commit()

    await update.message.reply_text(f"Reminder saved for {minutes} minute(s) from now.")


async def list_reminders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List current user's upcoming reminders."""

    _ = context
    if update.message is None or update.effective_user is None:
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        reminder_service = ReminderService(session)
        reminders = await reminder_service.upcoming_reminders(user_id=user_id)

    if not reminders:
        await update.message.reply_text("No reminders yet. Use /remind title | minutes_from_now")
        return

    lines = [f"#{reminder.id} {reminder.title}" for reminder in reminders[:10]]
    await update.message.reply_text("Your reminders:\n" + "\n".join(lines))
