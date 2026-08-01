"""Jarvis application entrypoint.

Running ``python main.py`` starts the FastAPI server in a background thread and
starts the Telegram bot when credentials are available.
"""

from __future__ import annotations

import asyncio
import threading
from contextlib import suppress

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application

from api.app import app as fastapi_app
from bot.client import build_telegram_application
from config.settings import get_settings
from scheduler.service import build_scheduler
from utils.logging import configure_logging, get_logger

settings = get_settings()
logger = get_logger(__name__)


def _run_uvicorn() -> None:
    """Run the FastAPI app in a dedicated thread."""

    config = uvicorn.Config(
        fastapi_app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        loop="asyncio",
        lifespan="on",
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


async def _start_bot(application: Application) -> None:
    """Start the Telegram bot using polling mode."""

    await application.initialize()
    await application.start()
    if settings.enable_polling:
        await application.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram bot started")


async def _stop_bot(application: Application) -> None:
    """Shut the Telegram bot down cleanly."""

    with suppress(Exception):
        if settings.enable_polling:
            await application.updater.stop()
    with suppress(Exception):
        await application.stop()
    with suppress(Exception):
        await application.shutdown()


async def _start_scheduler(application: Application) -> AsyncIOScheduler:
    """Start the background scheduler."""

    scheduler = build_scheduler(application)
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler


async def _stop_scheduler(scheduler: AsyncIOScheduler) -> None:
    """Stop the background scheduler."""

    with suppress(Exception):
        scheduler.shutdown(wait=False)


async def main() -> None:
    """Boot the complete application stack."""

    configure_logging()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)

    web_thread = threading.Thread(target=_run_uvicorn, name="fastapi-server", daemon=True)
    web_thread.start()

    telegram_application = build_telegram_application()
    scheduler: AsyncIOScheduler | None = None

    if telegram_application is not None:
        await _start_bot(telegram_application)
        scheduler = await _start_scheduler(telegram_application)
    else:
        logger.warning("Telegram bot disabled until TELEGRAM_BOT_TOKEN is configured")

    try:
        await asyncio.Event().wait()
    finally:
        if scheduler is not None:
            await _stop_scheduler(scheduler)
        if telegram_application is not None:
            await _stop_bot(telegram_application)


if __name__ == "__main__":
    asyncio.run(main())
