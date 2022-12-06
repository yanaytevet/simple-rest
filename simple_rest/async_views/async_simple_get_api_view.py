from abc import ABC, abstractmethod

from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncSimpleGetAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        data = await self.get_data(request, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_data(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        raise NotImplementedError()
