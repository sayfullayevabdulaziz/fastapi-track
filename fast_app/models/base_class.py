from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel as _SQLModel, Field


class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           sa_column_kwargs={"onupdate": datetime.utcnow})
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
