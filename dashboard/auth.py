"""Dashboard session helpers."""

from __future__ import annotations

from fastapi import Request

from auth.jwt import decode_access_token


def read_dashboard_subject(request: Request) -> str | None:
    """Read the authenticated subject from the dashboard cookie."""

    token = request.cookies.get("jarvis_session", "")
    if not token:
        return None

    try:
        payload = decode_access_token(token)
    except Exception:  # noqa: BLE001
        return None

    subject = str(payload.get("sub", "")).strip()
    return subject or None
