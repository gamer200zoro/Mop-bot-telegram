"""Reminder domain service."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Reminder
from database.repositories import ReminderRepository


class ReminderService:
    """Business rules for reminders."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = ReminderRepository(session)

    async def upcoming_reminders(self, user_id: int) -> Sequence[Reminder]:
        """Return all reminders for a user."""

        return await self.repository.list_for_user(user_id)

    async def due_reminders(self, now: datetime) -> Sequence[Reminder]:
        """Return reminders that should be sent now."""

        return await self.repository.due_reminders(now)

    async def mark_sent(self, reminder_id: int) -> None:
        """Mark a reminder as sent."""

        await self.repository.mark_sent(reminder_id)
