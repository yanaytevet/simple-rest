from abc import ABC, abstractmethod

from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncSimplePostAPIView(AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.POST

    async def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        data = await self.run_action(request, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        raise NotImplementedError()
