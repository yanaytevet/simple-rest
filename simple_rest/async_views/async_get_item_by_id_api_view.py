from abc import ABC

from simple_rest.async_views.async_get_item_api_view import AsyncGetItemAPIView
from simple_rest.async_views.async_item_by_id_api_mixin import AsyncItemByIdAPIMixin


class AsyncGetItemByIdAPIView(AsyncItemByIdAPIMixin, AsyncGetItemAPIView, ABC):
    pass


