from typing import List

from sqlmodel import SQLModel, Relationship

from fast_app.models.base_class import BaseModel


class RoleBase(SQLModel):
    name: str
    description: str


class Role(BaseModel, RoleBase, table=True):
    users: List["User"] = Relationship(
        back_populates="role", sa_relationship_kwargs={"lazy": "selectin"}
    )