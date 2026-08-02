"""Broad import smoke tests for core Jarvis modules."""

from __future__ import annotations


def test_core_modules_import_cleanly() -> None:
    """Import the main runtime modules to catch syntax and wiring issues early."""

    import ai.service  # noqa: F401
    import api.app  # noqa: F401
    import auth.jwt  # noqa: F401
    import bot.client  # noqa: F401
    import commands.registry  # noqa: F401
    import config.settings  # noqa: F401
    import dashboard.admin  # noqa: F401
    import dashboard.router  # noqa: F401
    import database.models  # noqa: F401
    import database.repositories  # noqa: F401
    import database.session  # noqa: F401
    import handlers.admin  # noqa: F401
    import handlers.ai  # noqa: F401
    import handlers.files  # noqa: F401
    import handlers.help  # noqa: F401
    import handlers.images  # noqa: F401
    import handlers.notes  # noqa: F401
    import handlers.pdf  # noqa: F401
    import handlers.reminders  # noqa: F401
    import handlers.start  # noqa: F401
    import handlers.todos  # noqa: F401
    import handlers.uploads  # noqa: F401
    import main  # noqa: F401
    import middleware.errors  # noqa: F401
    import middleware.request_logging  # noqa: F401
    import middleware.security  # noqa: F401
    import scheduler.service  # noqa: F401
    import services.currency  # noqa: F401
    import services.images  # noqa: F401
    import services.logs  # noqa: F401
    import services.news  # noqa: F401
    import services.notes  # noqa: F401
    import services.permissions  # noqa: F401
    import services.pdf  # noqa: F401
    import services.qr  # noqa: F401
    import services.reminders  # noqa: F401
    import services.storage  # noqa: F401
    import services.todos  # noqa: F401
    import services.uploads  # noqa: F401
    import services.users  # noqa: F401
    import services.weather  # noqa: F401
    import storage.client  # noqa: F401
    import utils.files  # noqa: F401
