from django.contrib.auth.models import User

from ..constants.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException
from .permissions_checker import PermissionsChecker


must_be_logged_in_api_exception = RestAPIException(
    status_code=StatusCode.HTTP_401_UNAUTHORIZED,
    message='Must be logged in.',
    error_code='must_be_logged_in',
)


class LoginPermissionChecker(PermissionsChecker):
    def raise_exception_if_not_valid(self, user: User) -> None:
        if not user or user.is_anonymous:
            raise must_be_logged_in_api_exception
