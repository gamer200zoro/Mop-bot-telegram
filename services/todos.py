"""Todo domain service."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories import TodoRepository


class TodoService:
    """Business rules for todo management."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = TodoRepository(session)

    async def list_todos(self, user_id: int) -> Sequence[object]:
        """Return all todo items for a user."""

        return await self.repository.list_for_user(user_id)

    async def create_todo(self, user_id: int, title: str, priority: int = 0) -> object:
        """Create a todo item."""

        return await self.repository.create(user_id=user_id, title=title, priority=priority)

    async def mark_done(self, todo_id: int, is_done: bool = True) -> None:
        """Mark a todo as completed or not completed."""

        await self.repository.mark_done(todo_id=todo_id, is_done=is_done)
