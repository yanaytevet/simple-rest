from abc import ABC, abstractmethod
from typing import Type, List

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from ..common.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class GetListAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted(request, **kwargs)
        objects = self.get_model_cls().objects
        objects = self.modify_objects_for_get(request, objects, **kwargs)
        data = self.serialize_all_objects(request, objects, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK, safe=False)

    @classmethod
    @abstractmethod
    def check_permitted(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    def modify_objects_for_get(cls, request: APIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        return objects.order_by('id')

    @classmethod
    def serialize_all_objects(cls, request: APIRequest, query_set: QuerySet, **kwargs) -> List[JSONType]:
        res: List[JSONType] = []
        for obj in query_set:
            res.append(cls.serialize_object(request, obj, **kwargs))
        res = [obj for obj in res if obj is not None]
        return res

    @classmethod
    @abstractmethod
    def serialize_object(cls, request: APIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
