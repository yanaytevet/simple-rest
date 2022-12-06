from abc import ABC, abstractmethod

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from simple_rest.utils.type_hints import JSONType
from simple_rest.constants.methods import Methods
from simple_rest.constants.status_code import StatusCode
from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest


class AsyncGetItemAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted_before_object(request, **kwargs)
        obj = await self.get_object(request, **kwargs)
        await self.check_permitted_after_object(request, obj, **kwargs)
        await self.run_after_get(request, obj, **kwargs)
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
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    async def run_after_get(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
