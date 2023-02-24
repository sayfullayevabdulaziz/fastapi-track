from fastapi import APIRouter, Depends, status

from fast_app import crud
from fast_app.api import deps
from fast_app.models.comment_model import Comment
from fast_app.models.user_model import User
from fast_app.schemas.response_schema import (
    GetResponseBase,
    PostResponseBase,
    create_response,
)
from fast_app.schemas.comment_schema import CommentCreate, CommentRead
from fast_app.schemas.role_schema import RoleEnum
from fast_app.utils.exceptions import IdNotFoundException

router = APIRouter()


@router.get("/list")
async def read_comment_list(
        current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager]))
) -> GetResponseBase[list[CommentRead]]:
    """
    Retrieve users. Requires admin or manager role
    """
    comments = await crud.comment.get_all()
    return create_response(data=comments)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blog(
        comment: CommentCreate
) -> PostResponseBase[CommentRead]:
    """
    Create a new comment
    """

    comment = await crud.comment.create(obj_in=comment)
    return create_response(data=comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_comment(
        comment_id: int,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
):
    """
    Deletes a comment by id
    """
    comment = await crud.comment.get(id=comment_id)
    if not comment:
        raise IdNotFoundException(Comment, id=comment_id)

    await crud.comment.remove(id=comment_id)
