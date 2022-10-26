from abc import ABC

from .async_item_by_id_api_mixin import AsyncItemByIdAPIMixin
from .async_put_actions_item_api_view import AsyncPutActionsItemAPIView


class AsyncPutActionsItemByIdAPIView(AsyncItemByIdAPIMixin, AsyncPutActionsItemAPIView, ABC):
    pass
