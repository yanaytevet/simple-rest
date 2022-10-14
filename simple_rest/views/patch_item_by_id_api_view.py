from abc import ABC

from .item_by_id_api_mixin import GetItemByIdAPIMixin
from .patch_item_api_view import PatchItemAPIView


class PatchItemByIdAPIView(GetItemByIdAPIMixin, PatchItemAPIView, ABC):
    pass
