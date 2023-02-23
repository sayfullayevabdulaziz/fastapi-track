from datetime import datetime
from typing import Optional

from fast_app.models.blog_model import BlogBase
from fast_app.utils.partial import optional


class BlogCreate(BlogBase):
    pass


# All these fields are optional
@optional
class BlogUpdate(BlogBase):
    pass


class BlogRead(BlogBase):
    id: int
    created_at: Optional[datetime]
