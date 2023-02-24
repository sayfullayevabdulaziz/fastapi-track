from typing import Optional
from fastapi import APIRouter, Depends, status, Body, UploadFile, File, HTTPException, Request

from fast_app import crud
from fast_app.api import deps

from fast_app.models import Track, ImageMedia
from fast_app.models import User
from fast_app.schemas.response_schema import (
    GetResponseBase,
    PostResponseBase,
    PutResponseBase,
    DeleteResponseBase,
    create_response,
)
from fast_app.schemas.role_schema import RoleEnum
from fast_app.schemas.track_schemas import TrackCreate, TrackRead, TrackUpdate
from fast_app.utils.exceptions import IdNotFoundException
from fast_app.utils.image_save import image_save_file

router = APIRouter()


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_all_trucks() -> GetResponseBase[list[TrackRead]]:
    trucks = await crud.track.get_all()
    return create_response(data=trucks)


@router.get("/{track_id}", status_code=status.HTTP_200_OK)
async def get_track_by_id(
        track_id: int

) -> GetResponseBase[TrackRead]:
    track = await crud.track.get(id=track_id)
    if not track:
        raise IdNotFoundException(User, id=track_id)

    # track_get = await crud.track.get_truck(track_id=track_id)
    # print(track_get)
    return create_response(data=track)


@router.post("")
async def create_track(
        name: Optional[str] = Body(None),
        description: Optional[str] = Body(None),
        price: Optional[int] = Body(default=0),
        is_active: Optional[bool] = Body(default=True),
        images: list[UploadFile] = File(...),
        current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager]))
) -> PostResponseBase[TrackRead]:
    new_track = {
        'name': name,
        'description': description,
        'price': price,
        'is_active': is_active
    }
    # add truck and get truck_id

    if images:

        track_id = await crud.track.create(obj_in=TrackCreate(**new_track), created_by_id=current_user.id)
        # save image to local and pydantic obj
        image_saved_to_local_file_n_db = await image_save_file(images=images)
        # save image to db
        await crud.image.create_image(images=image_saved_to_local_file_n_db, track_id=track_id.id)
        # get images where track_id=track_id.id
        image_list = await crud.image.get_all_images(track_id=track_id.id)

        await crud.track.add_image_to_track(images=image_list, track_id=track_id.id)

        return create_response(data=track_id)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Image not uploaded"})


@router.post("/image/{track_id}")
async def image_update(
        track_id: int,
        image: list[UploadFile] = File(...),
        current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager]))
) -> PostResponseBase[ImageMedia]:
    current_track = await crud.track.get(id=track_id)
    if not current_track:
        raise IdNotFoundException(Track, track_id)

    image_saved_to_local_file_n_db = await image_save_file(images=image)
    image_obj = await crud.image.create_image_while_update(images=image_saved_to_local_file_n_db, track_id=track_id)

    return create_response(data=image_obj)


@router.put("/{track_id}")
async def update_track(
        track_id: int,
        track: TrackUpdate,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        ),
) -> PutResponseBase[TrackRead]:
    current_track = await crud.track.get(id=track_id)
    if not current_track:
        raise IdNotFoundException(Track, track_id)
    track_updated = await crud.track.update(obj_new=track, obj_current=current_track)
    return create_response(data=track_updated)


@router.patch("/{track_id}")
async def update_is_active(
        track_id: int,
        is_active: Optional[bool] = Body(default=True, embed=True),
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        )
) -> PutResponseBase[TrackRead]:

    new_obj = TrackUpdate(is_active=is_active)

    current_track = await crud.track.get(id=track_id)
    if not current_track:
        raise IdNotFoundException(Track, track_id)
    track_update_is_active = await crud.track.update(obj_new=new_obj, obj_current=current_track)
    return create_response(data=track_update_is_active)


@router.delete("/image/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def image_remove(
        track_id: int,
        image_id: int = Body(embed=True),
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
        ),
):
    track = await crud.track.get(id=track_id)
    if not track:
        raise IdNotFoundException(Track, id=track_id)
    image_ids = [images_id.id for images_id in track.images]


    if image_id in image_ids:
        await crud.image.remove(id=image_id)
    else:
        raise IdNotFoundException(ImageMedia, id=image_id)



@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_track(
        track_id: int,
        current_user: User = Depends(
            deps.get_current_user(required_roles=[RoleEnum.admin])
        ),
):
    """
    Deletes a user by his/her id
    """
    track = await crud.track.get(id=track_id)
    if not track:
        raise IdNotFoundException(Track, id=track_id)

    await crud.track.remove(id=track_id)
    # return {"msg": "Deleted"}


