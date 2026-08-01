"""Telegram application factory and lifecycle helpers for Jarvis."""

from __future__ import annotations

from typing import cast

from telegram.ext import Application, ApplicationBuilder, CommandHandler

from config.settings import get_settings
from handlers.start import start_handler
from utils.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


def build_telegram_application() -> Application | None:
    """Create a configured python-telegram-bot application instance.

    The bot is optional during local development. When the token is missing, the
    web app still starts cleanly so health checks and dashboard routes remain
    available.
    """

    token = settings.telegram_bot_token.get_secret_value().strip()
    if not token:
        logger.warning("Telegram bot token is missing, skipping bot startup")
        return None

    builder = ApplicationBuilder().token(token)
    application = builder.build()
    application.add_handler(CommandHandler("start", start_handler))
    return cast(Application, application)


async def post_init(application: Application) -> None:
    """Hook for future startup tasks such as command registration."""

    _ = application


async def post_shutdown(application: Application) -> None:
    """Hook for future shutdown tasks such as flushing queues."""

    _ = application
