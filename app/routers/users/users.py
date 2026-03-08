
from typing import Annotated

from fastapi import APIRouter, status, Path, HTTPException,Response
from fastapi.params import Depends
from pydantic import EmailStr
from sqlmodel import Session, select

from app.dependencies import ActiveEngine, get_current_active_user
from app.logic.users import create_user, select_users, delete_user_by_email, update_user, update_user_status, \
    get_user_by_email
from app.models.users import UserBase, UserRegister, UserResponse, User, UserStatus, PreferencesUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(engine: ActiveEngine, user_data: UserRegister) -> UserResponse:
    """Register a new user"""
    new_user = create_user(engine, user_data)
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        google_id=new_user.google_id,
        role=new_user.role,
        status=new_user.status,
        joined=new_user.joined,
        favorite_genre=new_user.favorite_genre,
        preferred_store=new_user.preferred_store
    )


@router.get('/', status_code=status.HTTP_200_OK)
async def get_users(engine: ActiveEngine):
    return select_users(engine)


@router.delete('/{email}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(engine: ActiveEngine, email: EmailStr):
    delete_user_by_email(engine, email)


@router.put('/{email}', status_code=status.HTTP_202_ACCEPTED)
async def edit_user(engine: ActiveEngine, email: Annotated[EmailStr, Path()], user: UserBase):

    if email != user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Changing email is not allowed")

    update_user(
        engine=engine,
        edit_user=user,
        email=email
    )

@router.get('/me', status_code=status.HTTP_200_OK)
async def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.put('/{email}/logout', status_code=status.HTTP_202_ACCEPTED)
async def logout_user(engine: ActiveEngine, email: Annotated[EmailStr, Path()], disable: UserStatus,response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("sign_action")
    update_user_status(
        engine=engine,
        email=email,
        disable=disable
    )
