import os
from typing import Annotated

from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from google.auth.transport import requests
from sqlalchemy import Engine
from starlette import status
from starlette.requests import HTTPConnection

from app.logic.users import get_user_by_email
from app.models.token import TokenData
from app.models.users import User, UserStatus
from google.oauth2 import id_token


async def get_engine(request: HTTPConnection) -> Engine:
    return request.state.engine


ActiveEngine = Annotated[Engine, Depends(get_engine)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(engine: ActiveEngine, access_token: Annotated[str | None, Cookie()] = None,
                           sign_action: Annotated[str | None, Cookie()] = None) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token or not sign_action:
        raise credentials_exception

    try:
        if sign_action == "password":
            payload = jwt.decode(
                access_token,
                os.environ["SECRET_KEY"],
                algorithms=[os.environ["ALGORITHM"]],
            )
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token = TokenData(username=username)
            user = get_user_by_email(engine, token.username)
            if user is None:
                raise credentials_exception
            return user

        id_info = id_token.verify_oauth2_token(
            access_token,
            requests.Request(),
            os.environ["GOOGLE_CLIENT_ID"],
        )
        email = id_info["email"]
        if email is None:
            raise credentials_exception
        user = get_user_by_email(engine, email)
        if user is None:
            raise credentials_exception
        return user


    except InvalidTokenError:
        raise credentials_exception


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



