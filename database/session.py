"""Asynchronous PostgreSQL session management.

Jarvis uses SQLAlchemy's async engine so the Telegram bot and FastAPI backend
can share one database layer without blocking the event loop.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    str(settings.database_url),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for dependency injection and service code."""

    async with AsyncSessionLocal() as session:
        yield session
