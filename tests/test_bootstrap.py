"""Bootstrap smoke tests for the application stack."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import app
from config.settings import get_settings

client = TestClient(app)


def test_root_endpoint() -> None:
    """The root endpoint should identify the service."""

    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["app"] == "Jarvis"


def test_database_fallback_is_local_sqlite() -> None:
    """The settings object should fall back to a local SQLite database URL."""

    settings = get_settings()
    assert settings.resolved_database_url().startswith("sqlite+aiosqlite:///")
