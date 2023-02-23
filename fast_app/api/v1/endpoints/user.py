from typing import Optional, List

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlmodel import and_, select

from fast_app import crud
from fast_app.api import deps
from fast_app.models import User
from fast_app.models.role_model import Role
from fast_app.schemas.response_schema import (
    DeleteResponseBase,
    GetResponseBase,
    PostResponseBase,
    create_response,
)
from fast_app.schemas.role_schema import RoleEnum
from fast_app.schemas.user_schema import (
    UserCreate,
    UserRead,
    UserStatus
)
from fast_app.utils.exceptions import (
    IdNotFoundException,
    NameNotFoundException,
    UserSelfDeleteException,
)

router = APIRouter()


@router.get("/list")
async def read_users_list(
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
) -> GetResponseBase[List[UserRead]]:
    """
    Retrieve users. Requires admin or manager role
    """
    users = await crud.user.get_all()
    return create_response(data=users)


@router.get("/list/by_role_name")
async def read_users_list_by_role_name(
        user_status: Optional[UserStatus] = Query(
            default=UserStatus.active,
            description="User status, It is optional. Default is active",
        ),
        role_name: str = Query(
            default="", description="String compare with name or last name"
        ),
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        ),
) -> GetResponseBase[List[UserRead]]:
    """
    Retrieve users by role name and status. Requires admin role
    """
    user_status = user_status == UserStatus.active
    role = await crud.role.get_role_by_name(name=role_name)
    if not role:
        raise NameNotFoundException(Role, name=role_name)
    query = (
        select(User)
        .join(Role, User.role_id == Role.id)
        .where(and_(Role.name == role_name, User.is_active == user_status))
        .order_by(User.first_name)
    )
    users = await crud.user.get_all(query=query)
    return create_response(data=users)


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
) -> GetResponseBase[UserRead]:
    """
    Gets a user by his/her id
    """
    if user := await crud.user.get(id=user_id):
        return create_response(data=user)
    else:
        raise IdNotFoundException(User, id=user_id)


@router.get("")
async def get_my_data(
        current_user: User = Depends(deps.get_current_user()),
) -> GetResponseBase[UserRead]:
    """
    Gets my user profile information
    """

    return create_response(data=current_user)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: UserCreate = Depends(deps.user_exists),
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        ),
) -> PostResponseBase[UserRead]:
    """
    Creates a new user
    """

    role = await crud.role.get(id=new_user.role_id)
    if not role:
        raise IdNotFoundException(Role, id=new_user.role_id)

    user = await crud.user.create_with_role(obj_in=new_user)
    return create_response(data=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
        user_id: int,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        ),
):
    """
    Deletes a user by his/her id
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    if current_user.id == user_id:
        raise UserSelfDeleteException()

    user = await crud.user.remove(id=user_id)
