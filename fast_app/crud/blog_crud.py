from fast_app.crud.base_crud import CRUDBase
from fast_app.models.blog_model import Blog
from fast_app.schemas.blog_schema import BlogCreate, BlogUpdate


class CRUDBlog(CRUDBase[Blog, BlogCreate, BlogUpdate]):
    pass


blog = CRUDBlog(Blog)
