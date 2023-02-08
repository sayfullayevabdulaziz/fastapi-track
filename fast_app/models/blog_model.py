from fast_app.models.base_class import BaseModel
from sqlmodel import Field, SQLModel, Relationship
from pydantic import AnyUrl
from typing import Optional


class BlogBase(SQLModel):
    title: str
    file_name: str
    file_url: AnyUrl
    type: str


class Blog(BaseModel, BlogBase, table=True):
    pass
