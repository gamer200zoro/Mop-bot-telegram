"""Note domain service."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories import NoteRepository


class NoteService:
    """Business rules for user notes."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = NoteRepository(session)

    async def list_notes(self, user_id: int) -> Sequence[object]:
        """Return all notes for a user."""

        return await self.repository.list_for_user(user_id)

    async def create_note(self, user_id: int, title: str, content: str, is_pinned: bool = False) -> object:
        """Create a note and return it."""

        return await self.repository.create(user_id=user_id, title=title, content=content, is_pinned=is_pinned)
