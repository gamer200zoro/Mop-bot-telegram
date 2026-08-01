"""Authentication routes for the dashboard and future APIs."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.dependencies import get_current_subject
from auth.jwt import create_access_token
from auth.schemas import LoginRequest, TokenResponse
from config.settings import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response) -> TokenResponse:
    """Issue a dashboard token using the shared dashboard secret.

    This is the initial authentication shell. It is intentionally simple so the
    rest of the dashboard can be built and later replaced with richer account
    flows without changing the public route contract.
    """

    expected_password = settings.dashboard_secret_key.get_secret_value().strip()
    if not expected_password or payload.password != expected_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=payload.username)
    response.set_cookie("jarvis_session", token, httponly=True, secure=not settings.debug, samesite="lax", max_age=settings.access_token_minutes * 60)
    return TokenResponse(access_token=token)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    """Clear the dashboard session cookie."""

    response.delete_cookie("jarvis_session")
    return {"detail": "logged_out"}


@router.get("/me")
async def me(subject: str = Depends(get_current_subject)) -> dict[str, str]:
    """Return the authenticated subject."""

    return {"subject": subject}
