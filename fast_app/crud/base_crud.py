from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params, Page
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import SQLModel, select, func, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
        self, *, id: int, db_session: Optional[AsyncSession] = None
    ) -> Optional[ModelType]:
        db_session = db_session or db.session
        query = select(self.model).where(self.model.id == id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: List[int],
        db_session: Optional[AsyncSession] = None,
    ) -> Optional[List[ModelType]]:
        db_session = db_session or db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_count(
        self, db_session: Optional[AsyncSession] = None
    ) -> Optional[ModelType]:
        db_session = db_session or db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def get_all(
            self,
            *,
            query: Optional[Union[T, Select[T]]] = None,
            db_session: Optional[AsyncSession] = None,
    ) -> List[ModelType]:
        db_session = db_session or db.session
        if query is None:
            query = select(self.model).order_by(desc(self.model.id))
        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_multi_paginated(
            self,
            *,
            params: Optional[Params] = Params(),
            query: Optional[Union[T, Select[T]]] = None,
            db_session: Optional[AsyncSession] = None,
    ) -> Page[ModelType]:
        db_session = db_session or db.session
        if query is None:
            query = select(self.model).order_by(desc(self.model.id))
        return await paginate(db_session, query, params)


    async def create(
        self,
        *,
        obj_in: Union[CreateSchemaType, ModelType],
        created_by_id: int = None,
        db_session: Optional[AsyncSession] = None,
    ) -> ModelType:
        db_session = db_session or db.session
        db_obj = self.model.from_orm(obj_in)

        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            db_session.add(db_obj)
            await db_session.commit()
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: Union[UpdateSchemaType, Dict[str, Any], ModelType],
        db_session: Optional[AsyncSession] = None,
    ) -> ModelType:
        db_session = db_session or db.session
        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def remove(
        self, *, id: int, db_session: Optional[AsyncSession] = None
    ) -> ModelType:
        db_session = db_session or db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
