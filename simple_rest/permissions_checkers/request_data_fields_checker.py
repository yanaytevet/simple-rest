from typing import Union

from .permissions_checker import PermissionsChecker
from ..api_request import APIRequest
from ..async_api_request import AsyncAPIRequest
from ..constants.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException


class MissingDataFieldAPIException(RestAPIException):
    def __init__(self, field: str):
        super().__init__(StatusCode.HTTP_400_BAD_REQUEST,
                         f'field_{field}_is_missing',
                         f'Field "{field}" is missing')


class RequestDataFieldsAPIChecker(PermissionsChecker):
    def __init__(self, required_fields: list[str]):
        self.required_fields = required_fields

    def raise_exception_if_not_valid(self, request: Union[AsyncAPIRequest, APIRequest]) -> None:
        for field in self.required_fields:
            if field not in request.data:
                raise MissingDataFieldAPIException(field)
