"""HTTP request logging middleware."""

from __future__ import annotations

import logging
from time import perf_counter
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with timing information."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Measure and log request latency."""

        start = perf_counter()
        response = await call_next(request)
        duration_ms = (perf_counter() - start) * 1000.0
        logger.info("%s %s -> %s in %.2fms", request.method, request.url.path, response.status_code, duration_ms)
        response.headers.setdefault("X-Response-Time-ms", f"{duration_ms:.2f}")
        return response
