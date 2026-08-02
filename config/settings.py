"""Application settings for Jarvis.

This module centralizes every environment-driven configuration value used by the
bot, API server, scheduler, database, and dashboard layers.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Jarvis"
    app_env: Literal["development", "testing", "production"] = "development"
    app_version: str = "0.1.0"
    debug: bool = False

    telegram_bot_token: SecretStr = Field(default=SecretStr(""))
    telegram_webhook_secret: SecretStr = Field(default=SecretStr(""))
    telegram_admin_ids: str = Field(default="")

    database_url: str = Field(default="")
    supabase_url: str = Field(default="")
    supabase_anon_key: SecretStr = Field(default=SecretStr(""))
    supabase_service_role_key: SecretStr = Field(default=SecretStr(""))
    supabase_storage_bucket: str = Field(default="jarvis-files")

    openai_api_key: SecretStr = Field(default=SecretStr(""))
    openai_base_url: str = Field(default="https://api.openai.com/v1")
    openai_model: str = Field(default="gpt-4o-mini")

    dashboard_secret_key: SecretStr = Field(default=SecretStr("change-me"))
    jwt_secret_key: SecretStr = Field(default=SecretStr("change-me-too"))
    jwt_algorithm: str = Field(default="HS256")
    access_token_minutes: int = Field(default=60)

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    log_level: str = Field(default="info")

    webhook_url: str = Field(default="")
    enable_polling: bool = Field(default=True)

    rate_limit_per_minute: int = Field(default=60)
    upload_max_mb: int = Field(default=25)

    def resolved_database_url(self) -> str:
        """Return the configured database URL or a local SQLite fallback."""

        if self.database_url.strip():
            return self.database_url.strip()
        return f"sqlite+aiosqlite:///{Path('jarvis.db').resolve()}"

    @property
    def admin_ids(self) -> list[int]:
        """Return the parsed administrator Telegram user IDs."""

        if not self.telegram_admin_ids.strip():
            return []

        ids: list[int] = []
        for raw_value in self.telegram_admin_ids.split(","):
            raw_value = raw_value.strip()
            if raw_value:
                ids.append(int(raw_value))
        return ids


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a process-wide settings instance."""

    return Settings()  # type: ignore[call-arg]
