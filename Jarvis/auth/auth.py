from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Authentication is not yet implemented.")


@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User retrieval is not yet implemented.")
