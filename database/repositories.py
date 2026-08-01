"""Repository helpers for database access.

These classes encapsulate common CRUD operations so the service layer stays
small, testable, and free from raw SQL scattered across the codebase.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import LogEntry, Note, Reminder, Todo, Upload, User


class UserRepository:
    """Data access helpers for users."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Return a user by Telegram ID if it exists."""

        statement: Select[tuple[User]] = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def upsert_from_telegram(self, telegram_id: int, full_name: str, username: str | None) -> User:
        """Create or refresh a Telegram user record."""

        existing = await self.get_by_telegram_id(telegram_id)
        if existing is not None:
            existing.full_name = full_name
            existing.username = username
            existing.last_seen_at = datetime.now(tz=UTC)
            await self.session.flush()
            return existing

        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
            last_seen_at=datetime.now(tz=UTC),
        )
        self.session.add(user)
        await self.session.flush()
        return user


class NoteRepository:
    """Data access helpers for notes."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int) -> Sequence[Note]:
        """Return all notes for a user ordered by pin and recency."""

        statement = select(Note).where(Note.user_id == user_id).order_by(Note.is_pinned.desc(), Note.created_at.desc())
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, user_id: int, title: str, content: str, is_pinned: bool = False) -> Note:
        """Persist a new note."""

        note = Note(user_id=user_id, title=title, content=content, is_pinned=is_pinned)
        self.session.add(note)
        await self.session.flush()
        return note


class TodoRepository:
    """Data access helpers for todos."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int) -> Sequence[Todo]:
        """Return todo items for a user."""

        statement = select(Todo).where(Todo.user_id == user_id).order_by(Todo.is_done.asc(), Todo.priority.desc(), Todo.created_at.desc())
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, user_id: int, title: str, priority: int = 0) -> Todo:
        """Create a todo item."""

        todo = Todo(user_id=user_id, title=title, priority=priority)
        self.session.add(todo)
        await self.session.flush()
        return todo

    async def mark_done(self, todo_id: int, is_done: bool = True) -> None:
        """Toggle a todo completion state."""

        statement = update(Todo).where(Todo.id == todo_id).values(is_done=is_done)
        await self.session.execute(statement)


class ReminderRepository:
    """Data access helpers for reminders."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int) -> Sequence[Reminder]:
        """Return future reminders for a user."""

        statement = (
            select(Reminder)
            .where(Reminder.user_id == user_id)
            .order_by(Reminder.is_sent.asc(), Reminder.remind_at.asc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def due_reminders(self, now: datetime) -> Sequence[Reminder]:
        """Return reminders that should fire now or earlier."""

        statement = (
            select(Reminder)
            .options(selectinload(Reminder.user))
            .where(Reminder.is_sent.is_(False), Reminder.remind_at <= now)
            .order_by(Reminder.remind_at.asc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def mark_sent(self, reminder_id: int) -> None:
        """Mark a reminder as sent."""

        statement = update(Reminder).where(Reminder.id == reminder_id).values(is_sent=True)
        await self.session.execute(statement)


class UploadRepository:
    """Data access helpers for stored uploads."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int) -> Sequence[Upload]:
        """Return uploads for a user, newest first."""

        statement = select(Upload).where(Upload.user_id == user_id).order_by(Upload.created_at.desc())
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(
        self,
        user_id: int,
        original_filename: str,
        storage_path: str,
        bucket: str,
        content_type: str | None,
        public_url: str | None,
        file_size: int | None,
    ) -> Upload:
        """Persist uploaded file metadata."""

        upload = Upload(
            user_id=user_id,
            original_filename=original_filename,
            storage_path=storage_path,
            bucket=bucket,
            content_type=content_type,
            public_url=public_url,
            file_size=file_size,
        )
        self.session.add(upload)
        await self.session.flush()
        return upload


class LogRepository:
    """Persist structured logs in the database."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, level: str, source: str, message: str, user_id: int | None = None, metadata_json: str | None = None) -> LogEntry:
        """Create a persistent log entry."""

        entry = LogEntry(level=level, source=source, message=message, user_id=user_id, metadata_json=metadata_json)
        self.session.add(entry)
        await self.session.flush()
        return entry
