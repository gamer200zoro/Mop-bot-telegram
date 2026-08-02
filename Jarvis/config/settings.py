"""Application settings for Jarvis (legacy location).

Note: Use config/settings.py instead. This file is maintained for backward compatibility.
"""

from __future__ import annotations

from config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings", "settings"]

settings = get_settings()
