from fastapi import APIRouter, Depends, status

from fast_app import crud
from fast_app.api import deps
from fast_app.models.role_model import Role
from fast_app.models.user_model import User
from fast_app.schemas.response_schema import (
    GetResponseBase,
    PostResponseBase,
    PutResponseBase,
    create_response,
)
from fast_app.schemas.role_schema import RoleCreate, RoleEnum, RoleRead, RoleUpdate
from fast_app.utils.exceptions import IdNotFoundException, NameExistException, \
    ContentNoChangeException

router = APIRouter()

@router.get("/list")
async def read_roles_list(
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
) -> GetResponseBase[list[RoleRead]]:
    """
    Retrieve users. Requires admin or manager role
    """
    roles = await crud.role.get_all()
    return create_response(data=roles)


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
)
async def get_role_by_id(
    role_id: int,
    current_user: User = Depends(deps.get_current_user()),
) -> GetResponseBase[RoleRead]:
    """
    Gets a role by its id
    """
    role = await crud.role.get(id=role_id)
    if role:
        return create_response(data=role)
    else:
        raise IdNotFoundException(Role, id=role_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.admin])
    ),
) -> PostResponseBase[RoleRead]:
    """
    Create a new role
    """
    role_current = await crud.role.get_role_by_name(name=role.name)
    if role_current:
        raise NameExistException(Role, name=role_current.name)
    new_permission = await crud.role.create(obj_in=role)
    return create_response(data=new_permission)


@router.put("/{role_id}")
async def update_permission(
    role_id: int,
    role: RoleUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.admin])
    ),
) -> PutResponseBase[RoleRead]:
    """
    Updates the permission of a role by its id
    """
    current_role = await crud.role.get(id=role_id)
    if not current_role:
        raise IdNotFoundException(Role, id=role_id)

    if current_role.name == role.name and current_role.description == role.description:
        raise ContentNoChangeException()

    exist_role = await crud.role.get_role_by_name(name=role.name)
    if exist_role:
        raise NameExistException(Role, name=role.name)

    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role)