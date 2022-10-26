from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Any, Dict

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from simple_rest.utils.type_hints import JSONType

T = TypeVar('T')


class Serializer(ABC, Generic[T]):

    def __init__(self, context: Dict[str, Any] = None):
        self.context = dict(context) if context else {}

    def serialize(self, obj: T) -> Optional[JSONType]:
        if obj is None:
            return None
        return self.inner_serialize(obj)

    async def async_serialize(self, obj: T) -> Optional[JSONType]:
        return await sync_to_async(self.serialize)(obj)

    @abstractmethod
    def inner_serialize(self, obj: T) -> Optional[JSONType]:
        raise NotImplementedError()

    def serialize_query(self, query: QuerySet) -> list[JSONType]:
        res = [self.serialize(obj) for obj in query]
        res = [obj for obj in res if obj]
        return res
