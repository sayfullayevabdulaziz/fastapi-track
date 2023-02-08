import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, validator
from sqlmodel import Field, SQLModel, Relationship, Column, DateTime

from fast_app.models.base_class import BaseModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )  # birthday with timezone
    role_id: int = Field(default=None, foreign_key="Role.id")
    phone: Optional[str] = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )

    @validator('phone')
    def phone_check(cls, phone):
        assert re.search("^[\+]?998[389][012345789][0-9]{7}$",
                         phone), "Telefon raqam +998901234567 shu ko'rinishda bo'lishi kerak"
        return phone


class User(BaseModel, UserBase, table=True):
    hashed_password: Optional[str] = Field(nullable=False, index=True)
    role: Optional["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
