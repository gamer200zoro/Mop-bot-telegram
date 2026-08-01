"""Supabase Storage service for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from supabase import Client

from config.settings import get_settings
from storage.client import get_supabase_client

settings = get_settings()


@dataclass(slots=True)
class StoredObject:
    """Describe an object stored in Supabase."""

    path: str
    bucket: str
    public_url: str | None = None


class StorageService:
    """Upload and download helpers backed by Supabase Storage."""

    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_supabase_client()

    @property
    def is_enabled(self) -> bool:
        """Return True when Supabase storage credentials are configured."""

        return self.client is not None

    def _bucket(self):
        """Return the configured storage bucket client."""

        if self.client is None:
            raise RuntimeError("Supabase storage is not configured")
        return self.client.storage.from_(settings.supabase_storage_bucket)

    def upload_bytes(self, path: str, payload: bytes, content_type: str | None = None, upsert: bool = True) -> StoredObject:
        """Upload binary data to Supabase Storage."""

        bucket = self._bucket()
        file_options = {"upsert": "true" if upsert else "false"}
        if content_type:
            file_options["content-type"] = content_type
        response = bucket.upload(path=path, file=BytesIO(payload), file_options=file_options)
        public_url: str | None = None
        try:
            public_url = bucket.get_public_url(path)
        except Exception:  # noqa: BLE001
            public_url = None
        return StoredObject(path=str(response), bucket=settings.supabase_storage_bucket, public_url=public_url)

    def download_bytes(self, path: str) -> bytes:
        """Download binary data from Supabase Storage."""

        bucket = self._bucket()
        return bucket.download(path)
