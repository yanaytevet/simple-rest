from abc import ABC, abstractmethod

from django.db.models import Model
from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException
from ..views.api_view_component import APIViewComponent


class PutActionsItemAPIView(APIViewComponent, ABC):
    ACTION_FIELD = 'action'

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.PUT

    def put(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted_before_object(request, **kwargs)
        obj = self.get_object(request, **kwargs)
        self.check_permitted_after_object(request, obj, **kwargs)
        self.run_action(request, obj, **kwargs)
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

    def run_action(self, request: APIRequest, obj: Model, **kwargs) -> None:
        if self.ACTION_FIELD not in request.data:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_field_is_missing',
                message="'action' field is missing",
            )
        action = request.data[self.ACTION_FIELD]
        action_func_name = f'put_{action}'
        if not hasattr(self, action_func_name):
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_function_is_not_implemented',
                message=f"action '{action}' is not implemented",
            )
        getattr(self, action_func_name)(request, obj, **kwargs)

    @classmethod
    @abstractmethod
    def serialize_object(cls, request: APIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
