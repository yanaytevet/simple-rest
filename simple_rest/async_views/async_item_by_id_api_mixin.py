from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model

from ..async_api_request import AsyncAPIRequest
from ..exceptions.none_object_doesnt_exist_api_exception import NoneObjectDoesntExistAPIException
from ..exceptions.object_doesnt_exist_api_exception import ObjectDoesntExistAPIException


class AsyncItemByIdAPIMixin(ABC):
    @classmethod
    async def get_object(cls, request: AsyncAPIRequest, **kwargs) -> Model:
        object_id = kwargs.get('object_id')
        if object_id is None:
            raise NoneObjectDoesntExistAPIException()
        model_cls = cls.get_model_cls()
        try:
            return await model_cls.objects.aget(id=object_id)
        except model_cls.DoesNotExist as e:
            raise ObjectDoesntExistAPIException(model_cls, object_id)

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()
