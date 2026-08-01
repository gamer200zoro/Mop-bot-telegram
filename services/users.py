"""User domain service for Jarvis."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories import UserRepository


class UserService:
    """Business rules around Telegram users."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def register_telegram_user(self, telegram_id: int, full_name: str, username: str | None) -> int:
        """Create or refresh the user and return its internal database ID."""

        user = await self.repository.upsert_from_telegram(telegram_id=telegram_id, full_name=full_name, username=username)
        return user.id
