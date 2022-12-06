from typing import Dict, Type

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from ..constants.methods import Methods
from ..exceptions.api_view_components_conflict_exception import APIViewComponentsConflictException


def get_method_async_func(api_view_component: AsyncAPIViewComponent):
    async def func(self, request: HttpRequest, **kwargs) -> HttpResponse:
        api_request = AsyncAPIRequest(request)
        return await api_view_component.run_with_exception_handling(api_request, **kwargs)
    func.__name__ = str(api_view_component.get_method())
    return func


def async_compose_api_views(*api_view_components: AsyncAPIViewComponent) -> Type[View]:
    method_to_view_component: Dict[Methods, AsyncAPIViewComponent] = {}

    @method_decorator(csrf_exempt, name='dispatch')
    class AsyncComposedAPIView(View):
        pass

    for api_view_component in api_view_components:
        method = api_view_component.get_method()
        existing_api_view_component = method_to_view_component.get(method)
        if existing_api_view_component is not None:
            raise APIViewComponentsConflictException(existing_api_view_component, method, api_view_component)

        method_to_view_component[method] = api_view_component
        setattr(AsyncComposedAPIView, str(api_view_component.get_method()), get_method_async_func(api_view_component))
    return AsyncComposedAPIView
