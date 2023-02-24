from sqlmodel import SQLModel, Field, Relationship
from typing import List
from fast_app.models.base_class import BaseModel


class TrackBase(SQLModel):
    name: str = Field(index=True)
    description: str
    price: int
    is_active: bool = Field(default=True)



class Track(BaseModel, TrackBase, table=True):
    created_by_id: int = Field(default=None, nullable=True, foreign_key="User.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={"lazy": "selectin", "primaryjoin": "Track.created_by_id==User.id"},

    )

    images: List["ImageMedia"] = Relationship(
        back_populates='track', sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete"}
    )