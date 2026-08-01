"""Smoke tests for the Telegram bot factory."""

from __future__ import annotations

from bot.client import build_telegram_application


def test_bot_factory_returns_none_without_token() -> None:
    """The bot should stay disabled when no token is configured."""

    assert build_telegram_application() is None
