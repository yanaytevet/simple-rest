from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model

from ..api_request import APIRequest
from ..exceptions.none_object_doesnt_exist_api_exception import NoneObjectDoesntExistAPIException
from ..exceptions.object_doesnt_exist_api_exception import ObjectDoesntExistAPIException


class ItemByIdAPIMixin(ABC):
    @classmethod
    def get_object(cls, request: APIRequest, **kwargs) -> Model:
        object_id = kwargs.get('object_id')
        if object_id is None:
            raise NoneObjectDoesntExistAPIException()
        model_cls = cls.get_model_cls()
        try:
            return model_cls.objects.get(id=object_id)
        except model_cls.DoesNotExist as e:
            raise ObjectDoesntExistAPIException(model_cls, object_id)

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()


