"""JWT helper functions for dashboard sessions and API auth."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from config.settings import get_settings

settings = get_settings()


def _require_jwt_secret() -> str:
    """Return the JWT secret or raise a runtime error if it is missing."""

    secret = settings.jwt_secret_key.get_secret_value().strip()
    if not secret:
        raise RuntimeError("JWT secret is not configured")
    return secret


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """Create a signed access token for the given subject."""

    expires_delta = timedelta(minutes=expires_minutes or settings.access_token_minutes)
    now = datetime.now(tz=UTC)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "iss": settings.app_name,
    }
    return jwt.encode(payload, _require_jwt_secret(), algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and verify a signed access token."""

    return jwt.decode(token, _require_jwt_secret(), algorithms=[settings.jwt_algorithm])
