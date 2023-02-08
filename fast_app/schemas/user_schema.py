from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from fast_app.models.user_model import UserBase
from fast_app.utils.partial import optional
from .role_schema import RoleRead


class UserCreate(UserBase):
    password: Optional[str]

    class Config:
        hashed_password = None


# All these fields are optional
@optional
class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    role: Optional[RoleRead] = None


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
