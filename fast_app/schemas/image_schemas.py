from typing import Optional
from fast_app.models.image_model import ImageMediaBase
from fast_app.utils.partial import optional
from pydantic import AnyUrl


class ImageMediaCreate(ImageMediaBase):
    pass


# All these fields are optional
@optional
class ImageMediaUpdate(ImageMediaBase):
    pass


class ImageMediaRead(ImageMediaBase):
    track_id: int
    url: AnyUrl = f"localhost:8000/static/path"


