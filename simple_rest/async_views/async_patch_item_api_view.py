from abc import ABC, abstractmethod
from typing import Set

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..utils.model_utils import ModelUtils


class AsyncPatchItemAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.PATCH

    async def patch(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted_before_object(request, **kwargs)
        obj = await self.get_object(request, **kwargs)
        await self.check_permitted_after_object(request, obj, **kwargs)
        await self.update_item(request, obj, **kwargs)
        await self.run_after_edit(request, obj, **kwargs)
        data = await self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_object(cls, request: AsyncAPIRequest, **kwargs) -> Model:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    async def update_item(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        data = await cls.get_modified_request_data_for_editing(request, obj)
        await ModelUtils.async_update_from_json(obj, data, cls.get_allowed_edit_fields())

    @classmethod
    async def get_modified_request_data_for_editing(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> JSONType:
        return dict(request.data)

    @classmethod
    @abstractmethod
    def get_allowed_edit_fields(cls) -> Set[str]:
        raise NotImplementedError()

    @classmethod
    async def run_after_edit(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
