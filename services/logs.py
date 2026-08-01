"""Persistent log service for Jarvis."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories import LogRepository


class LogService:
    """Persist important system events."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = LogRepository(session)

    async def record(self, level: str, source: str, message: str, user_id: int | None = None, metadata_json: str | None = None) -> object:
        """Create a log entry and return it."""

        return await self.repository.create(level=level, source=source, message=message, user_id=user_id, metadata_json=metadata_json)
