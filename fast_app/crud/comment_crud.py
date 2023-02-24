from fast_app.crud.base_crud import CRUDBase
from fast_app.models.comment_model import Comment
from fast_app.schemas.comment_schema import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    pass


comment = CRUDComment(Comment)
