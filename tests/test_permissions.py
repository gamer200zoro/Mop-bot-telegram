"""Smoke tests for permission checks."""

from __future__ import annotations

from services.permissions import PermissionService


def test_permission_service_returns_boolean() -> None:
    """The permission service should return a boolean admin decision."""

    service = PermissionService(telegram_user_id=123456789)
    assert isinstance(service.is_admin(), bool)
