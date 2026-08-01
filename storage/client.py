"""Supabase client helpers for storage operations."""

from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from config.settings import get_settings
from utils.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_supabase_client() -> Client | None:
    """Create a cached Supabase client when credentials are available."""

    url = settings.supabase_url.strip()
    key = settings.supabase_service_role_key.get_secret_value().strip()
    if not url or not key:
        logger.warning("Supabase credentials are missing, storage features are disabled")
        return None
    return create_client(url, key)
