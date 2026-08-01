"""Permission and admin checks for Jarvis."""

from __future__ import annotations

from config.settings import get_settings

settings = get_settings()


class PermissionService:
    """Resolve whether a Telegram user can perform admin actions."""

    def __init__(self, telegram_user_id: int) -> None:
        self.telegram_user_id = telegram_user_id

    def is_admin(self) -> bool:
        """Return True when the user is configured as an administrator."""

        return self.telegram_user_id in settings.admin_ids
