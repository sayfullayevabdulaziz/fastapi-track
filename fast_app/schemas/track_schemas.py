from typing import Optional, List

from pydantic import BaseModel

from fast_app.models.image_model import ImageMediaBase
from fast_app.models.track_model import TrackBase
from fast_app.utils.partial import optional


class TrackCreate(TrackBase):
    pass


# All these fields are optional
@optional
class TrackUpdate(TrackBase):
    pass


class TrackRead(TrackBase):
    id: int
    images: Optional[List[ImageMediaBase]]


class TrackIsActive(BaseModel):
    is_active: bool