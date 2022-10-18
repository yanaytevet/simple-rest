from typing import Dict, Type

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from ..constants.methods import Methods
from ..exceptions.api_view_components_conflict_exception import APIViewComponentsConflictException


def async_compose_api_views(*api_view_components: AsyncAPIViewComponent) -> Type[View]:
    @method_decorator(csrf_exempt, name='dispatch')
    class AsyncComposedAPIView(View):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.method_to_view_component: Dict[Methods, AsyncAPIViewComponent] = {}
            self.set_methods()

        def set_methods(self) -> None:
            for api_view_component in api_view_components:
                method = api_view_component.get_method()
                existing_api_view_component = self.method_to_view_component.get(method)
                if existing_api_view_component is not None:
                    raise APIViewComponentsConflictException(existing_api_view_component, method, api_view_component)

                async def func(request: HttpRequest, **kwargs) -> JsonResponse:
                    api_request = AsyncAPIRequest(request)
                    return await api_view_component.run_with_exception_handling(api_request, **kwargs)

                func.__name__ = str(method)
                setattr(self, func.__name__, func)
    return AsyncComposedAPIView
