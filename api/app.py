"""FastAPI application for Jarvis.

This app exposes operational endpoints, dashboard routes, and future public
integrations such as webhooks, file uploads, and admin actions.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.health import router as health_router
from config.settings import get_settings
from dashboard.router import router as dashboard_router
from middleware.security import RateLimitMiddleware

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_per_minute)

app.include_router(health_router)
app.include_router(dashboard_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Return the service identity for a quick browser check."""

    return {"app": settings.app_name, "version": settings.app_version}
