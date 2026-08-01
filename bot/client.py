"""Telegram application factory and lifecycle helpers for Jarvis."""

from __future__ import annotations

from telegram import BotCommand
from telegram.ext import Application, ApplicationBuilder, CommandHandler

from commands.registry import COMMANDS
from config.settings import get_settings
from database.session import AsyncSessionLocal
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

    builder = (
        ApplicationBuilder()
        .token(token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
    )
    application = builder.build()
    application.bot_data["session_factory"] = AsyncSessionLocal

    for command in COMMANDS:
        application.add_handler(CommandHandler(command.name, command.handler))

    return application


async def post_init(application: Application) -> None:
    """Register the command menu after startup."""

    commands = [BotCommand(command.name, command.description) for command in COMMANDS]
    await application.bot.set_my_commands(commands)
    logger.info("Telegram command menu registered")


async def post_shutdown(application: Application) -> None:
    """Hook for future shutdown tasks such as flushing queues."""

    _ = application
