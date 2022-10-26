import math
from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class GetListAPIView(APIViewComponent, ABC):
    DEFAULT_PAGE_SIZE = 25
    MIN_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted(request, **kwargs)
        objects = self.get_model_cls().objects
        objects = self.filter_objects_by_request(request, objects, **kwargs)
        objects = self.order_objects_by_request(request, objects, **kwargs)
        page = int(request.query_params.get('page', 0))
        page_size = self.get_page_size(request)

        if self.should_filter_only_by_objects():
            total_amount = objects.count()
            data = self.serialize_objects(request, objects, page, page_size, **kwargs)
        else:
            objects_list = self.filter_and_sort_list(request, objects)
            total_amount = len(objects_list)
            data = self.serialize_list(request, objects_list, page, page_size, **kwargs)
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
    def check_permitted(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    def filter_objects_by_request(cls, request: APIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        return objects

    @classmethod
    def order_objects_by_request(cls, request: APIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        order_by_str = request.query_params.get('order_by')
        if order_by_str:
            objects.order_by(order_by_str)
        return objects

    @classmethod
    def get_page_size(cls, request: APIRequest) -> int:
        page_size = int(request.query_params.get('page_size', cls.DEFAULT_PAGE_SIZE))
        return min(max(cls.MIN_PAGE_SIZE, page_size), cls.MAX_PAGE_SIZE)

    @classmethod
    @abstractmethod
    def should_filter_only_by_objects(cls) -> bool:
        raise NotImplementedError()

    @classmethod
    def serialize_objects(cls, request: APIRequest, objects: QuerySet, page: int, page_size: int, **kwargs) -> list[JSONType]:
        start = page * page_size
        end = (page + 1) * page_size
        return [cls.serialize_object(request, obj, **kwargs) for obj in objects[start: end]]

    @classmethod
    def serialize_list(cls, request: APIRequest, objects_list: list[Model], page: int, page_size: int, **kwargs) -> list[JSONType]:
        start = page * page_size
        end = (page + 1) * page_size
        return [cls.serialize_object(request, obj, **kwargs) for obj in objects_list[start: end]]

    @classmethod
    @abstractmethod
    def serialize_object(cls, request: APIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
