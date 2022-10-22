import json
from typing import Optional

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest, QueryDict


class APIRequest:
    def __init__(self, original_request: HttpRequest):
        self.original_request = original_request
        self.user: Optional[User] = None
        self.data = json.loads(original_request.body) if original_request.body else {}
        self.query_params: QueryDict = original_request.GET
        self.files = original_request.FILES
        self.init_user()

    def init_user(self) -> None:
        self.user = get_user(self.original_request)

    @property
    def session(self) -> SessionBase:
        return self.original_request.session
