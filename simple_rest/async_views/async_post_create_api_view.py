from abc import ABC, abstractmethod
from typing import Type, Optional, Set

from django.db.models import Model
from django.http import HttpRequest, JsonResponse, HttpResponse

from simple_rest.utils.model_utils import ModelUtils
from simple_rest.utils.type_hints import JSONType
from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncPostCreateAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.POST

    async def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest,  **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        await self.run_before_creation(request, **kwargs)
        obj = await self.create_obj(request, **kwargs)
        await self.run_after_post(request, obj, **kwargs)
        data = await self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest,  **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    async def run_before_creation(cls, request: AsyncAPIRequest,  **kwargs) -> None:
        pass

    @classmethod
    async def create_obj(cls, request: AsyncAPIRequest,  **kwargs) -> Optional[Model]:
        data = dict(request.data)
        if data:
            model_cls = cls.get_model_cls()
            obj = await ModelUtils.async_create_from_json(model_cls, data, cls.get_allowed_creation_fields())
            return obj
        return None

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        raise NotImplementedError()

    @classmethod
    async def run_after_post(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
