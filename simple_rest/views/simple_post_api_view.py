from abc import ABC, abstractmethod

from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class SimplePostAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.POST

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted(request, **kwargs)
        data = self.run_action(request, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    def check_permitted(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def run_action(cls, request: APIRequest, **kwargs) -> JSONType:
        raise NotImplementedError()
