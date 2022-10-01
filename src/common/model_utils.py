from typing import Type, Optional, Set, TypeVar

from django.db import models
from django.forms import model_to_dict

from common.type_hints import JSONType

T = TypeVar('T')


class ModelUtils:
    @classmethod
    def create_from_json(cls, model_cls: Type[T],
                         json_data: JSONType,
                         allowed_attributes_set: Optional[Set[str]] = None) -> T:
        obj = model_cls()
        cls.update_from_json(obj, json_data, allowed_attributes_set)

        return obj

    @classmethod
    def update_from_json(cls,
                         obj: models.Model,
                         json_data: JSONType,
                         allowed_attributes_set: Optional[Set[str]] = None) -> None:
        for key, value in json_data.items():
            if allowed_attributes_set is not None and key in allowed_attributes_set:
                setattr(obj, key, value)
        obj.save()

    @classmethod
    def to_json(cls, obj: models.Model) -> JSONType:
        data = model_to_dict(obj)
        del data["id"]
        return data
