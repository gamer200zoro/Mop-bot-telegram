"""Pydantic schemas for authentication flows."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Access token payload returned after login."""

    access_token: str
    token_type: str = Field(default="bearer")


class LoginRequest(BaseModel):
    """Login payload used by the dashboard."""

    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)
