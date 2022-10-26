from abc import ABC

from .async_delete_item_api_view import AsyncDeleteItemAPIView
from .async_item_by_id_api_mixin import AsyncItemByIdAPIMixin


class AsyncDeleteItemByIdAPIView(AsyncItemByIdAPIMixin, AsyncDeleteItemAPIView, ABC):
    pass
