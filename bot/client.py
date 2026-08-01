"""Telegram application factory and lifecycle helpers for Jarvis."""

from __future__ import annotations

from typing import Any

from telegram.ext import Application, ApplicationBuilder, CommandHandler

from config.settings import get_settings
from handlers.start import start_handler

settings = get_settings()


def build_telegram_application() -> Application:
    """Create a configured python-telegram-bot application instance."""

    builder = ApplicationBuilder().token(settings.telegram_bot_token.get_secret_value())
    application = builder.build()
    application.add_handler(CommandHandler("start", start_handler))
    return application


async def post_init(application: Application) -> None:
    """Hook for future startup tasks such as command registration."""

    _ = application


async def post_shutdown(application: Application) -> None:
    """Hook for future shutdown tasks such as flushing queues."""

    _ = application
