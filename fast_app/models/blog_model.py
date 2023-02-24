from fast_app.models.base_class import BaseModel
from sqlmodel import SQLModel, Field


class BlogBase(SQLModel):
    title: str
    link: str = Field(default="new", nullable=True)
    hashtag: str = Field(default="new", nullable=True)
    description: str = Field(default="new", nullable=True)
    file_name: str
    file_url: str
    type: str


class Blog(BaseModel, BlogBase, table=True):
    pass
