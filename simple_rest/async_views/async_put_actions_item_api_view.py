import asyncio
from abc import ABC, abstractmethod

from asgiref.sync import sync_to_async
from django.db.models import Model
from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from simple_rest.utils.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException


class AsyncPutActionsItemAPIView(AsyncAPIViewComponent, ABC):
    ACTION_FIELD = 'action'

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.PUT

    async def put(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted_before_object(request, **kwargs)
        obj = await self.get_object(request, **kwargs)
        await self.check_permitted_after_object(request, obj, **kwargs)
        await self.run_action(request, obj, **kwargs)
        data = await self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

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
    async def check_permitted_after_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    async def run_action(self, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        if self.ACTION_FIELD not in request.data:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_field_is_missing',
                message="'action' field is missing",
            )
        action = request.data[self.ACTION_FIELD]
        action_func_name = f'put_{action}'
        if not hasattr(self, action_func_name):
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_function_is_not_implemented',
                message=f"action '{action}' is not implemented",
            )
        func = getattr(self, action_func_name)
        if asyncio.iscoroutinefunction(func):
            await func(request, obj, **kwargs)
        else:
            await request.future_user
            await sync_to_async(func)(request, obj, **kwargs)

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
