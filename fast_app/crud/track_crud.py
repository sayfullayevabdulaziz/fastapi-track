from typing import Optional
from fastapi_async_sqlalchemy import db
from fast_app.crud.base_crud import CRUDBase
from fast_app.models import ImageMedia
from fast_app.models.track_model import Track
from fast_app.schemas.track_schemas import TrackCreate, TrackUpdate, TrackRead
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDTrack(CRUDBase[Track, TrackCreate, TrackUpdate]):
    async def add_image_to_track(self, *, images: list[ImageMedia], track_id: int) -> Track:
        track = await super().get(id=track_id)
        for image in images:
            track.images.append(image)
            db.session.add(track)
            await db.session.commit()
            await db.session.refresh(track)
        return track

    async def get_truck(self, *, track_id: int, db_session: Optional[AsyncSession] = None) -> TrackRead:
        db_session = db_session or db.session
        query = (
            select(ImageMedia).join(Track).where(Track.id == track_id)
        )
        response = await db_session.execute(query)
        return response.scalars().all()


track = CRUDTrack(Track)
