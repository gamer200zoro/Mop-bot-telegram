"""Jarvis application entrypoint.

Running ``python main.py`` starts the FastAPI server in a background thread and
runs the Telegram bot in the main process.
"""

from __future__ import annotations

import asyncio
import threading
from contextlib import suppress

import uvicorn
from telegram.ext import Application

from api.app import app as fastapi_app
from bot.client import build_telegram_application
from config.settings import get_settings
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


async def main() -> None:
    """Boot the complete application stack."""

    configure_logging()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)

    web_thread = threading.Thread(target=_run_uvicorn, name="fastapi-server", daemon=True)
    web_thread.start()

    telegram_application = build_telegram_application()
    await _start_bot(telegram_application)

    try:
        await asyncio.Event().wait()
    finally:
        await _stop_bot(telegram_application)


if __name__ == "__main__":
    asyncio.run(main())
