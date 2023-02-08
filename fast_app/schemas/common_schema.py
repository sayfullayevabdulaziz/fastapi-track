from enum import Enum
from typing import List

from pydantic import BaseModel

from fast_app.schemas.role_schema import RoleRead


class MetaGeneral(BaseModel):
    roles: List[RoleRead]


class OrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"