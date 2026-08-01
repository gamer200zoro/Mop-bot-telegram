"""Asynchronous database session management.

Jarvis uses SQLAlchemy's async engine so the Telegram bot and FastAPI backend
can share one database layer without blocking the event loop.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import get_settings

settings = get_settings()
database_url = settings.resolved_database_url()
engine_kwargs: dict[str, Any] = {"echo": settings.debug, "pool_pre_ping": True}
if not database_url.startswith("sqlite"):
    engine_kwargs.update({"pool_size": 5, "max_overflow": 10})

engine = create_async_engine(database_url, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for dependency injection and service code."""

    async with AsyncSessionLocal() as session:
        yield session
