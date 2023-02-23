from typing import Optional

from fastapi import APIRouter, Depends, status, Body, UploadFile, File, Query

from fast_app import crud
from fast_app.api import deps
from fastapi_pagination import Params
from fast_app.models.blog_model import Blog
from fast_app.models.user_model import User
from fast_app.schemas.response_schema import (
    GetResponseBase,
    PostResponseBase,
    PutResponseBase,
    create_response, GetResponsePaginated,
)
from fast_app.schemas.blog_schema import BlogCreate, BlogRead, BlogUpdate
from fast_app.schemas.role_schema import RoleEnum
from fast_app.utils.exceptions import IdNotFoundException
from fast_app.utils.media_save_blog import media_save_file

router = APIRouter()

@router.get("/list")
async def read_blog_list(
    params: Params = Depends(),
) -> GetResponsePaginated[BlogRead]:
    """
    Retrieve users. Requires admin or manager role
    """

    blogs = await crud.blog.get_multi_paginated(params=params)
    print(blogs)
    return create_response(data=blogs)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: Optional[str] = Body(None),
    link: Optional[str] = Body(None),
    hashtag: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    type: Optional[str] = Body(None),
    file: UploadFile = File(...),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
    ),
) -> PostResponseBase[BlogRead]:
    """
    Create a new blog
    """

    media_name = await media_save_file(media=file)
    new_blog = {
        'title': title,
        'link': link,
        'hashtag': hashtag,
        'description': description,
        'type': type,
        **media_name
    }

    blog = await crud.blog.create(obj_in=BlogCreate(**new_blog))
    return create_response(data=blog)


@router.patch("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
    ),
) -> PutResponseBase[BlogRead]:
    """
    Updates the permission of a blog by its id
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


    await crud.blog.remove(id=blog_id)
