from abc import ABC

from .item_by_id_api_mixin import ItemByIdAPIMixin
from .put_actions_item_api_view import PutActionsItemAPIView


class PutActionsItemByIdAPIView(ItemByIdAPIMixin, PutActionsItemAPIView, ABC):
    pass
