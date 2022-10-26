from abc import ABC, abstractmethod
from typing import Type, Optional, Set

from django.db.models import Model
from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.model_utils import ModelUtils
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class PostCreateAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.POST

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest,  **kwargs) -> JsonResponse:
        self.check_permitted(request, **kwargs)
        self.run_before_creation(request, **kwargs)
        obj = self.create_obj(request, **kwargs)
        self.run_after_post(request, obj, **kwargs)
        data = self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    def check_permitted(cls, request: APIRequest,  **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    def run_before_creation(cls, request: APIRequest,  **kwargs) -> None:
        pass

    @classmethod
    def create_obj(cls, request: APIRequest,  **kwargs) -> Optional[Model]:
        data = dict(request.data)
        if data:
            model_cls = cls.get_model_cls()
            obj = ModelUtils.create_from_json(model_cls, data, cls.get_allowed_creation_fields())
            return obj
        return None

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        raise NotImplementedError()

    @classmethod
    def run_after_post(cls, request: APIRequest,  obj: Model, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    def serialize_object(cls, request: APIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
