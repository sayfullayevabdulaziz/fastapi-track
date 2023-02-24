from pydantic import EmailStr

from fast_app.models.base_class import BaseModel
from sqlmodel import SQLModel


class CommentBase(SQLModel):
    your_name: str
    company_name: str
    email_address: EmailStr
    phone_number: str
    comment: str


class Comment(BaseModel, CommentBase, table=True):
    pass
