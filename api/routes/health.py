"""Operational endpoints for uptime monitoring and readiness checks."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(tags=["monitoring"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Return a lightweight liveness response."""

    return {"status": "ok", "timestamp": datetime.now(tz=UTC).isoformat()}


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Return a minimal ping response for uptime robots and smoke tests."""

    return {"message": "pong"}


@router.get("/metrics")
async def metrics() -> dict[str, str]:
    """Return a minimal metrics placeholder that can be expanded later."""

    return {"bot": "running", "database": "configured"}
