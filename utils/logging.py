"""Logging helpers for Jarvis.

The application uses a single logging configuration so Telegram handlers, the
FastAPI app, schedulers, and background tasks all emit consistent records.
"""

from __future__ import annotations

import logging
import sys
from logging.config import dictConfig

from config.settings import get_settings


def configure_logging() -> None:
    """Configure process-wide logging with a compact JSON-friendly layout."""

    settings = get_settings()
    level = settings.log_level.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": sys.stdout,
                }
            },
            "root": {
                "level": level,
                "handlers": ["console"],
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module logger after logging has been configured."""

    return logging.getLogger(name)
