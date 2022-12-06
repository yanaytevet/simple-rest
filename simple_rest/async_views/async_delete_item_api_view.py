from abc import ABC, abstractmethod

from asgiref.sync import sync_to_async
from django.db.models import Model, QuerySet
from django.http import JsonResponse, HttpRequest, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncDeleteItemAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.DELETE

    async def delete(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted_before_object(request, **kwargs)
        obj = await self.get_object(request, **kwargs)
        await self.check_permitted_after_object(request, obj, **kwargs)
        await self.run_before_deletion(request, obj, **kwargs)
        await self.delete_item(request, obj, **kwargs)
        await self.run_after_deletion(request, obj, **kwargs)
        return JsonResponse({}, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_object(cls, request: AsyncAPIRequest, **kwargs) -> Model:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    async def delete_item(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        await sync_to_async(obj.delete)()

    @classmethod
    async def run_before_deletion(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        pass

    @classmethod
    async def run_after_deletion(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        pass
