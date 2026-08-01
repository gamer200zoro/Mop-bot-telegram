"""FastAPI dependency functions for database and authentication."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import decode_access_token
from database.session import get_async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session to route handlers."""

    async for session in get_async_session():
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_subject(request: Request) -> str:
    """Resolve the current authenticated subject from a bearer token or cookie."""

    auth_header = request.headers.get("authorization", "")
    token = ""
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get("jarvis_session", "")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    try:
        payload = decode_access_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    subject = str(payload.get("sub", "")).strip()
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return subject
