"""Security middleware for FastAPI.

The middleware layer applies light-weight request throttling and security headers
so the dashboard and public endpoints behave predictably under load.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
from typing import Awaitable, cast

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


@dataclass(slots=True)
class RateLimitBucket:
    """Track request timestamps for a single client key."""

    timestamps: deque[float]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """A simple in-memory token bucket middleware.

    This is designed for single-instance deployments. In a horizontally scaled
    setup, move rate-limiting to Redis or a gateway.
    """

    def __init__(self, app: ASGIApp, requests_per_minute: int) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._buckets: dict[str, RateLimitBucket] = defaultdict(lambda: RateLimitBucket(deque()))
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Reject clients that exceed the configured request rate."""

        client = request.client.host if request.client else "unknown"
        now = monotonic()
        window_start = now - 60.0

        async with self._lock:
            bucket = self._buckets[client]
            while bucket.timestamps and bucket.timestamps[0] < window_start:
                bucket.timestamps.popleft()
            bucket.timestamps.append(now)
            if len(bucket.timestamps) > self.requests_per_minute:
                return Response(status_code=429, content="Too Many Requests")

        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
        return response
