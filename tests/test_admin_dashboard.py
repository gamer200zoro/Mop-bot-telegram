"""Smoke tests for the admin dashboard route."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_admin_dashboard_requires_authentication() -> None:
    """The admin overview should reject anonymous requests."""

    response = client.get("/dashboard/admin")
    assert response.status_code == 401
