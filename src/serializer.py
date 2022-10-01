from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Any, Dict

from common.type_hints import JSONType

T = TypeVar('T')


class Serializer(ABC, Generic[T]):

    def __init__(self, context: Dict[str, Any] = None):
        self.context = dict(context) if context else {}

    def serialize(self, obj: T) -> Optional[JSONType]:
        if obj is None:
            return None
        return self.inner_serialize(obj)

    @abstractmethod
    def inner_serialize(self, obj: T) -> Optional[JSONType]:
        raise NotImplementedError()
