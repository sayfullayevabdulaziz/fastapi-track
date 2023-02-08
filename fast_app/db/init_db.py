from typing import Dict, List, Union

from sqlmodel.ext.asyncio.session import AsyncSession

from fast_app import crud
from fast_app.core.config import settings
from fast_app.schemas.role_schema import RoleCreate
from fast_app.schemas.user_schema import UserCreate

roles: List[RoleCreate] = [
    RoleCreate(name="admin", description="This the Admin role"),
    RoleCreate(name="manager", description="Manager role"),
    RoleCreate(name="user", description="User role"),
]


users: List[Dict[str, Union[str, UserCreate]]] = [
    {
        "data": UserCreate(
            first_name="Admin",
            last_name="Katta Bola",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            phone="+998903470113",
            is_superuser=True,
        ),
        "role": "admin",
    },
    {
        "data": UserCreate(
            first_name="Manager",
            last_name="Manager aka",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="manager@example.com",
            phone="+998900711313",
            is_superuser=False,
        ),
        "role": "manager",
    },
    {
        "data": UserCreate(
            first_name="User",
            last_name="Userjon",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="user@example.com",
            phone="+998919713733",
            is_superuser=False,
        ),
        "role": "user",
    },
]



async def init_db(db_session: AsyncSession) -> None:

    for role in roles:
        role_current = await crud.role.get_role_by_name(
            name=role.name, db_session=db_session
        )
        if not role_current:
            await crud.role.create(obj_in=role, db_session=db_session)

    for user in users:
        current_user = await crud.user.get_by_email(
            email=user["data"].email, db_session=db_session
        )
        role = await crud.role.get_role_by_name(
            name=user["role"], db_session=db_session
        )
        if not current_user:
            user["data"].role_id = role.id
            await crud.user.create_with_role(obj_in=user["data"], db_session=db_session)

