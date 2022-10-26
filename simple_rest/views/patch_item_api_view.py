from abc import ABC, abstractmethod
from typing import Set

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..utils.model_utils import ModelUtils
from ..views.api_view_component import APIViewComponent


class PatchItemAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.PATCH

    def patch(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted_before_object(request, **kwargs)
        obj = self.get_object(request, **kwargs)
        self.check_permitted_after_object(request, obj, **kwargs)
        self.update_item(request, obj, **kwargs)
        self.run_after_edit(request, obj, **kwargs)
        data = self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    def check_permitted_before_object(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_object(cls, request: APIRequest, **kwargs) -> Model:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def check_permitted_after_object(cls, request: APIRequest,  obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def update_item(cls, request: APIRequest,  obj: Model, **kwargs) -> None:
        data = cls.get_modified_request_data_for_editing(request, obj)
        ModelUtils.update_from_json(obj, data, cls.get_allowed_edit_fields())

    @classmethod
    def get_modified_request_data_for_editing(cls, request: APIRequest,  obj: Model, **kwargs) -> JSONType:
        return dict(request.data)

    @classmethod
    @abstractmethod
    def get_allowed_edit_fields(cls) -> Set[str]:
        raise NotImplementedError()

    @classmethod
    def run_after_edit(cls, request: APIRequest,  obj: Model, **kwargs) -> QuerySet:
        pass

    @classmethod
    @abstractmethod
    def serialize_object(cls, request: APIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
