from math import ceil
from typing import Any, Dict, Generic, Union, Optional, TypeVar, Sequence
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")
T = TypeVar("T")


class PageBase(Page[T], Generic[T]):
    pages: int
    next_page: Optional[int]
    previous_page: Optional[int]


class ResponsePage(AbstractPage[T], Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: PageBase[T]

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Union[PageBase[T], None]:
        if params.size is not None and total is not None and params.size != 0:
            pages = ceil(total / params.size)
        else:
            pages = 0

        return cls(
            data=PageBase(
                items=items,
                page=params.page,
                size=params.size,
                total=total,
                pages=pages,
                next_page=params.page + 1 if params.page < pages else None,
                previous_page=params.page - 1 if params.page > 1 else None,
            )
        )



class ResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class GetResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class GetResponsePaginated(ResponsePage[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class PostResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class PutResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class DeleteResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Optional[DataType],
    message: Optional[str] = "",
    meta: Optional[Union[Dict, Any]] = {},
) -> Union[Dict[str, DataType], DataType]:
    if isinstance(data, ResponsePage):
        data.message = "Data paginated correctly" if not message else message
        data.meta = meta
        return data
    body_response = {"data": data, "message": message, "meta": meta}
    return {k: v for k, v in body_response.items() if v is not None}
