"""Smoke tests for the authentication routes."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_login_rejects_bad_password() -> None:
    """Login should fail with invalid credentials when secret is unset."""

    response = client.post("/auth/login", json={"username": "demo", "password": "wrong"})
    assert response.status_code == 401


def test_me_requires_authentication() -> None:
    """The me endpoint should require a session token."""

    response = client.get("/auth/me")
    assert response.status_code == 401
