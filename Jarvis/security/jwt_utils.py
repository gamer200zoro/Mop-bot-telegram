"""Legacy JWT compatibility wrapper.

This module now delegates to the single active JWT implementation in
``auth/jwt.py`` so the repository has only one token logic path.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Optional

from auth.jwt import create_access_token as _create_access_token, decode_access_token


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Compatibility wrapper for older imports that expected a dict payload."""

    payload = dict(data)
    sub = payload.get("sub")
    if sub is None:
        raise ValueError("sub claim is required")

    expires_minutes: int | None = None
    if expires_delta is not None:
        expires_minutes = max(1, int(expires_delta.total_seconds() // 60))
    return _create_access_token(subject=str(sub), expires_minutes=expires_minutes)


def verify_token(token: str, credentials_exception):
    """Compatibility wrapper that validates a JWT and returns the subject."""

    try:
        payload = decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except Exception:  # noqa: BLE001
        raise credentials_exception
