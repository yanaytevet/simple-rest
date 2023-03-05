import json
import math
from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..api_request import APIRequest
from ..async_api_request import AsyncAPIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncGetListAPIView(AsyncAPIViewComponent, ABC):
    DEFAULT_PAGE_SIZE = 25
    MIN_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        objects = self.get_model_cls().objects
        objects = await self.filter_objects_by_request(request, objects, **kwargs)
        objects = await self.order_objects_by_request(request, objects, **kwargs)
        page = int(request.query_params.get('page', 0))
        page_size = self.get_page_size(request)

        if self.should_filter_only_by_objects():
            total_amount = await objects.acount()
            data = await self.serialize_objects(request, objects, page, page_size, **kwargs)
        else:
            objects_list = self.filter_and_sort_list(request, objects)
            total_amount = len(objects_list)
            data = await self.serialize_list(request, objects_list, page, page_size, **kwargs)
        res = {
            'total_amount': total_amount,
            'pages_amount': math.ceil(total_amount / page_size),
            'data': data,
            'page': page,
            'page_size': page_size,
        }
        return JsonResponse(res, status=StatusCode.HTTP_200_OK, safe=False)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    async def filter_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        return objects

    @classmethod
    async def order_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        order_by_str = request.query_params.get('order_by')
        if order_by_str:
            objects = objects.order_by(order_by_str)
        return objects

    @classmethod
    def get_page_size(cls, request: AsyncAPIRequest) -> int:
        page_size = int(request.query_params.get('page_size', cls.DEFAULT_PAGE_SIZE))
        return min(max(cls.MIN_PAGE_SIZE, page_size), cls.MAX_PAGE_SIZE)

    @classmethod
    @abstractmethod
    def should_filter_only_by_objects(cls) -> bool:
        raise NotImplementedError()

    @classmethod
    async def serialize_objects(cls, request: AsyncAPIRequest, objects: QuerySet, page: int, page_size: int,
                                **kwargs) -> list[JSONType]:
        start = page * page_size
        end = (page + 1) * page_size
        return [await cls.serialize_object(request, obj, **kwargs) async for obj in objects[start: end]]

    @classmethod
    async def serialize_list(cls, request: AsyncAPIRequest, objects_list: list[Model], page: int, page_size: int,
                             **kwargs) -> list[JSONType]:
        start = page * page_size
        end = (page + 1) * page_size
        return [await cls.serialize_object(request, obj, **kwargs) for obj in objects_list[start: end]]

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()

    @classmethod
    def get_filter_params_from_request(cls, request: APIRequest) -> JSONType:
        filter_params_str = request.query_params.get('filter_params')
        if not filter_params_str:
            return {}
        return json.loads(filter_params_str)
