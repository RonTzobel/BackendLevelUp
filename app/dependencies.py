from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import Engine
from starlette import status
from starlette.requests import HTTPConnection

from app.config.settings import settings
from app.logic.users import get_user_by_id
from app.models.token import TokenData
from app.models.users import User, UserStatus


async def get_engine(request: HTTPConnection) -> Engine:
    return request.state.engine


ActiveEngine = Annotated[Engine, Depends(get_engine)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(engine: ActiveEngine, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        sub: str | None = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(sub))
    except (JWTError, ValueError):
        raise credentials_exception

    user = get_user_by_id(engine, token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



