import asyncio
from asyncio import Future

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.http import HttpRequest

from simple_rest.api_request import APIRequest


class AsyncAPIRequest(APIRequest):
    def __init__(self, original_request: HttpRequest):
        self.future_user: Future[User] = Future()
        super().__init__(original_request)

    def init_user(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_init_user())

    async def async_init_user(self) -> None:
        user = await sync_to_async(get_user)(self.original_request)
        self.future_user.set_result(user)
        self.user = user
