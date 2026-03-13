import logging
from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from google.auth.exceptions import TransportError

from app.config.settings import settings
from app.dependencies import ActiveEngine
from app.logic.auth import (
    create_access_token,
)
from google.oauth2 import id_token
from google.auth.transport import requests

logger = logging.getLogger(__name__)

from sqlmodel import Session, select

from app.logic.users import create_user_from_google, get_user_by_email, get_user_by_google_id, select_user, \
    update_user_status
from app.models.token import Token, TokenRequest
from app.models.users import User, UserStatus
from app.utilities.passwords import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"description": "Not found"}},
)

@router.post("/google", response_model=Token)
async def google_auth(engine: ActiveEngine, data: TokenRequest):
    """Login or signup with Google authentication. Returns a LevelUp JWT."""
    try:
        id_info = id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        # Covers: wrong audience, expired token, invalid signature, malformed token
        logger.warning("Google token verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Google token",
        )
    except TransportError as exc:
        # Google's cert endpoint was unreachable
        logger.error("Google certs transport error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not verify Google token — try again",
        )

    if not id_info.get("email_verified"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google email not verified")

    email = id_info["email"]
    name = id_info.get("name")
    google_id = id_info["sub"]

    # Look up by email first to prevent duplicates, then fall back to google_id
    user = get_user_by_email(engine, email) or get_user_by_google_id(engine, google_id)

    if user:
        # Existing user — update google_id if not yet linked
        if not user.google_id:
            with Session(engine) as session:
                statement = select(User).where(User.id == user.id)
                db_user = session.exec(statement).first()
                if db_user:
                    db_user.google_id = google_id
                    db_user.status = UserStatus.ACTIVE
                    session.add(db_user)
                    session.commit()
                    session.refresh(db_user)
                    user = db_user
    else:
        # New user — create from Google profile
        user = create_user_from_google(engine, email, name, google_id)

    if user.status == UserStatus.SUSPENDED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already suspended")

    update_user_status(engine=engine, email=user.email, disable=UserStatus.ACTIVE)

    # Issue a LevelUp JWT — same as regular login
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def login(engine: ActiveEngine, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login and get access token."""
    user = select_user(engine, form_data)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.status == UserStatus.SUSPENDED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already suspended")

    update_user_status(engine=engine, email=user.email, disable=UserStatus.ACTIVE)

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")




