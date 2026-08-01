"""Upload metadata service for Jarvis."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Upload
from database.repositories import UploadRepository


class UploadService:
    """Business rules for stored file metadata."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = UploadRepository(session)

    async def list_uploads(self, user_id: int) -> Sequence[Upload]:
        """Return uploads for a user."""

        return await self.repository.list_for_user(user_id)

    async def record_upload(
        self,
        user_id: int,
        original_filename: str,
        storage_path: str,
        bucket: str,
        content_type: str | None,
        public_url: str | None,
        file_size: int | None,
    ) -> Upload:
        """Persist upload metadata and return the row."""

        return await self.repository.create(
            user_id=user_id,
            original_filename=original_filename,
            storage_path=storage_path,
            bucket=bucket,
            content_type=content_type,
            public_url=public_url,
            file_size=file_size,
        )
