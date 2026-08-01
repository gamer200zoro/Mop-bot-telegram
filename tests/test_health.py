"""Smoke tests for the operational endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """The health endpoint should return an ok status."""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ping_endpoint() -> None:
    """The ping endpoint should return pong."""

    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json()["message"] == "pong"
