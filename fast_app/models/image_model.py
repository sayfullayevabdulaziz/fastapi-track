from fast_app.models.base_class import BaseModel
from sqlmodel import Field, SQLModel, Relationship, ForeignKey, Column, Integer
from typing import Optional


class ImageMediaBase(SQLModel):
    id: int = None
    file_name: Optional[str]
    file_content: Optional[str]
    file_ext: str


class ImageMedia(BaseModel, ImageMediaBase, table=True):

    track_id: int = Field(default=None, nullable=True, sa_column=Column(Integer, ForeignKey("Track.id", ondelete="CASCADE")))
    track: Optional["Track"] = Relationship(back_populates='images')