from typing import AsyncGenerator, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from fast_app import crud
from fast_app.core import security
from fast_app.core.config import settings
from fast_app.db.session import SessionLocal
from fast_app.models.user_model import User
from fast_app.schemas.common_schema import MetaGeneral
from fast_app.schemas.user_schema import UserCreate
from fast_app.schemas.user_schema import UserRead

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_general_meta() -> MetaGeneral:
    current_roles = await crud.role.get_all()
    return MetaGeneral(roles=current_roles)


def get_current_user(required_roles: List[str] = None) -> User:
    async def current_user(
        token: str = Depends(reusable_oauth2),
    ) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Could not validate credentials"},
            )
        user_id = int(payload["sub"])

        user: User = await crud.user.get(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail={"message": "User not found"})

        if not user.is_active:
            raise HTTPException(status_code=400, detail={"message": "Inactive user"})

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    detail={"message": f"Role {required_roles} is required for this action"},
                )

        return user

    return current_user


async def user_exists(new_user: UserCreate) -> UserCreate:
    user = await crud.user.get_by_email(email=new_user.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "There is already a user with same email"},
        )
    return new_user


async def is_valid_user(user_id: int) -> UserRead:
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail={"message": "User no found"})

    return user