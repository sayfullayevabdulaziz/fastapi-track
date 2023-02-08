from enum import Enum

from fast_app.models.role_model import RoleBase
from fast_app.utils.partial import optional


class RoleCreate(RoleBase):
    pass


# All these fields are optional
@optional
class RoleUpdate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
