from abc import ABC

from .delete_item_api_view import DeleteItemAPIView
from .item_by_id_api_mixin import ItemByIdAPIMixin


class DeleteItemByIdAPIView(ItemByIdAPIMixin, DeleteItemAPIView, ABC):
    pass
