from fast_app.models.comment_model import CommentBase
from fast_app.utils.partial import optional


class CommentCreate(CommentBase):
    pass


# All these fields are optional
@optional
class CommentUpdate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
