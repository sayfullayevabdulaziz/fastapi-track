from typing import Optional, List

from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fast_app.crud.base_crud import CRUDBase
from fast_app.models.image_model import ImageMedia, ImageMediaBase
from fast_app.models.track_model import Track
from fast_app.schemas.image_schemas import ImageMediaCreate, ImageMediaUpdate


class CRUDImage(CRUDBase[ImageMedia, ImageMediaCreate, ImageMediaUpdate]):
    async def get_image_by_id(
        self, *, id: int, db_session: Optional[AsyncSession] = None
    ) -> ImageMedia:
        db_session = db_session or db.session
        image = await db_session.execute(select(ImageMedia).where(ImageMedia.id == id))
        return image.scalar_one_or_none()

    async def create_image(
            self, *, images: list[ImageMediaBase], track_id: int, db_session: Optional[AsyncSession] = None
    ) -> None:
        db_session = db_session or db.session
        for image in images:
            db_obj = ImageMedia.from_orm(image, update={"track_id": track_id})
            # db_obj.track_id = track_id
            db.session.add(db_obj)
            await db.session.commit()
            await db.session.refresh(db_obj)


    async def create_image_while_update(
            self, *, images: list[ImageMediaBase], track_id: int, db_session: Optional[AsyncSession] = None
    ) -> ImageMedia:
        db_session = db_session or db.session
        for image in images:
            db_obj = ImageMedia.from_orm(image, update={"track_id": track_id})
            db_obj.track_id = track_id
            db.session.add(db_obj)
            await db.session.commit()
            await db.session.refresh(db_obj)
            return db_obj


    async def get_all_images(
            self,
            *,
            track_id: int,
            db_session: Optional[AsyncSession] = None,
    ) -> List[ImageMedia]:
        db_session = db_session or db.session
        query = select(ImageMedia).where(ImageMedia.track_id == track_id)
        response = await db_session.execute(query)
        return response.scalars().all()


image = CRUDImage(ImageMedia)
