from typing import Optional

from fastapi import APIRouter, Depends, status, Body, UploadFile, File

from fast_app import crud
from fast_app.api import deps
from fast_app.models.blog_model import Blog
from fast_app.models.user_model import User
from fast_app.schemas.response_schema import (
    GetResponseBase,
    PostResponseBase,
    PutResponseBase,
    DeleteResponseBase,
    create_response,
)
from fast_app.schemas.blog_schema import BlogCreate, BlogRead, BlogUpdate
from fast_app.schemas.role_schema import RoleEnum
from fast_app.utils.exceptions import IdNotFoundException, NameExistException, \
    ContentNoChangeException

router = APIRouter()

@router.get("/list")
async def read_blog_list() -> GetResponseBase[list[BlogRead]]:
    """
    Retrieve users. Requires admin or manager role
    """
    blogs = await crud.blog.get_all()
    return create_response(data=blogs)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: Optional[str] = Body(None),
    type: Optional[str] = Body(None),
    file: UploadFile = File(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.manager, RoleEnum.manager])
    ),
) -> PostResponseBase[BlogRead]:
    """
    Create a new blog
    """
    new_blog = {
        'title': title,
        'type': type,
    }
    blog_id = await crud.blog.create(obj_in=BlogCreate(**new_blog))
    # new_blog = await crud.blog.create(obj_in=blog)
    # return create_response(data=new_blog)


@router.put("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
    ),
) -> PutResponseBase[BlogRead]:
    """
    Updates the permission of a role by its id
    """
    current_blog = await crud.blog.get(id=blog_id)
    if not current_blog:
        raise IdNotFoundException(Blog, blog_id)

    track_updated = await crud.track.update(obj_new=blog, obj_current=current_blog)
    return create_response(data=track_updated)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_blog(
        blog_id: int,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
):
    """
    Deletes a user by his/her id
    """
    blog = await crud.blog.get(id=blog_id)
    if not blog:
        raise IdNotFoundException(Blog, id=blog)


    blog = await crud.blog.remove(id=blog_id)
    return {"msg": "Deleted"}