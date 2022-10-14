from abc import ABC

from .get_item_api_view import GetItemAPIView
from .item_by_id_api_mixin import GetItemByIdAPIMixin


class GetItemByIdAPIView(GetItemByIdAPIMixin, GetItemAPIView, ABC):
    pass


