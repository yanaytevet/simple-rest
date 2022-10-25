from typing import Dict, Type

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..api_request import APIRequest
from ..constants.methods import Methods
from ..exceptions.api_view_components_conflict_exception import APIViewComponentsConflictException
from ..views.api_view_component import APIViewComponent


def get_method_func(api_view_component: APIViewComponent):
    async def func(self, request: HttpRequest, **kwargs) -> JsonResponse:
        api_request = APIRequest(request)
        return api_view_component.run_with_exception_handling(api_request, **kwargs)
    func.__name__ = str(api_view_component.get_method())
    return func


def compose_api_views(*api_view_components: APIViewComponent) -> Type[View]:
    method_to_view_component: Dict[Methods, APIViewComponent] = {}

    @method_decorator(csrf_exempt, name='dispatch')
    class ComposedAPIView(View):
        pass

    for api_view_component in api_view_components:
        method = api_view_component.get_method()
        existing_api_view_component = method_to_view_component.get(method)
        if existing_api_view_component is not None:
            raise APIViewComponentsConflictException(existing_api_view_component, method, api_view_component)

        method_to_view_component[method] = api_view_component
        setattr(ComposedAPIView, str(api_view_component.get_method()), get_method_func(api_view_component))
    return ComposedAPIView
