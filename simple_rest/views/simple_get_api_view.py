from abc import ABC, abstractmethod

from django.http import HttpRequest, JsonResponse

from ..api_request import APIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class SimpleGetAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted(request, **kwargs)
        data = self.get_data(request, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    def check_permitted(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_data(cls, request: APIRequest, **kwargs) -> JSONType:
        raise NotImplementedError()
