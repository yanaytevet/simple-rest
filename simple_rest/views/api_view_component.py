from abc import abstractmethod, ABC

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..api_request import APIRequest
from ..constants.methods import Methods
from ..exceptions.rest_api_exception import RestAPIException


@method_decorator(csrf_exempt, name='dispatch')
class APIViewComponent(View, ABC):
    @classmethod
    @abstractmethod
    def get_method(cls) -> Methods:
        raise NotImplementedError()

    @abstractmethod
    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        raise NotImplementedError()

    def run_with_exception_handling(self, request: APIRequest, **kwargs) -> JsonResponse:
        try:
            return self.run(request, **kwargs)
        except RestAPIException as e:
            return JsonResponse({
                'detail': e.message,
                'error_code': e.error_code,
            }, status=e.status_code)
