from typing import Union

from ..async_views.async_api_view_component import AsyncAPIViewComponent
from ..constants.methods import Methods
from ..views.api_view_component import APIViewComponent


GeneralAPIViewComponent = Union[APIViewComponent, AsyncAPIViewComponent]


class APIViewComponentsConflictException(Exception):
    def __init__(self, component1: GeneralAPIViewComponent, method: Methods, component2: GeneralAPIViewComponent):
        self.component1 = component1
        self.component2 = component2
        self.method = method
        self.msg = f'cannot set {self.component2.__class__.__name__} on {self.method}, ' \
                   f'{self.component1.__class__.__name__} is already using it.'
        super().__init__()
