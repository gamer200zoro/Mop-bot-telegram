"""Smoke tests for the dashboard routes."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_dashboard_home_page_renders() -> None:
    """The dashboard home page should render successfully."""

    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Jarvis control panel" in response.text


def test_dashboard_login_page_renders() -> None:
    """The dashboard login page should render successfully."""

    response = client.get("/dashboard/login")
    assert response.status_code == 200
    assert "Jarvis login" in response.text
