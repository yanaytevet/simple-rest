from typing import List, Dict

from django.contrib.auth import get_user
from django.http import HttpRequest

from constants.methods import Methods
from views.api_view_component import APIViewComponent
from exceptions.api_view_components_conflict_exception import APIViewComponentsConflictException


class ComposedAPIView:
    def __init__(self, *args: APIViewComponent):
        self.api_view_components: List[APIViewComponent] = list(args)
        self.method_to_view_component: Dict[Methods, APIViewComponent] = {}
        self.set_methods()

    def set_methods(self) -> None:
        for api_view_component in self.api_view_components:
            method = api_view_component.get_method()
            existing_api_view_component = self.method_to_view_component.get(method)
            if existing_api_view_component is not None:
                raise APIViewComponentsConflictException(existing_api_view_component, method, api_view_component)

            def func(request: HttpRequest, *args, **kwargs):
                user = get_user(request)
                api_view_component.run(request, user, *args, **kwargs)
            func.__name__ = str(method)
            setattr(self, func.__name__, func)
