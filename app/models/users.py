import datetime
from enum import  auto, StrEnum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel
from typing import Optional


class UserRole(StrEnum):
    """User permission tiers."""
    USER = auto()
    ADMIN = auto()


class UserStatus(StrEnum):
    """User status tiers."""
    ACTIVE = auto()
    SUSPENDED = auto()
    INACTIVE = auto()

class UserGenre(StrEnum):
    """User genre tiers."""
    ACTION= auto()
    ADVENTURE = auto()
    RGP = auto()
    STRATEGY = auto()
    SIMULATION = auto()
    SPORTS = auto()
    RACING = auto()
    PUZZLE = auto()

class UserStores(StrEnum):
    STEAM = auto()
    UPLAY = auto()
    DESURA = auto()
    AMAZON = auto()
    ORIGIN = auto()

class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    password:str | None = Field(default=None,min_length=3, max_length=1000)
    name:str = Field(max_length=255)
    google_id: Optional[str] = Field(default=None, max_length=255)
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.INACTIVE)
    joined: datetime.datetime = Field(default_factory=datetime.datetime.now)
    favorite_genre:UserGenre = Field(default=UserGenre.ACTION)
    preferred_store:UserStores = Field(default=UserStores.STEAM)

class User(UserBase, table=True):
    __tablename__ = "users"


class UserRegister(SQLModel):
    email: EmailStr
    password: str | None = Field(default=None,min_length=3, max_length=1000)
    name: str = Field(min_length=1, max_length=255)


class UserResponse(BaseModel):
    """User response model without password"""
    id: int
    email: EmailStr
    name: str
    google_id: Optional[str] = None
    role: UserRole
    status: UserStatus
    purchase: int | None = None
    joined: datetime.datetime | None = None
    favorite_genre: UserGenre
    preferred_store: UserStores

class PreferencesUpdate(BaseModel):
    """Model for updating user preferences"""
    favoriteGenre: Optional[str] = None
    preferredStore: Optional[str] = None









