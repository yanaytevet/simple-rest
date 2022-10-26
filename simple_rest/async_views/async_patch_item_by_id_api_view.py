from abc import ABC

from .async_item_by_id_api_mixin import AsyncItemByIdAPIMixin
from .async_patch_item_api_view import AsyncPatchItemAPIView


class AsyncPatchItemByIdAPIView(AsyncItemByIdAPIMixin, AsyncPatchItemAPIView, ABC):
    pass
