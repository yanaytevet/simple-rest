from .rest_api_exception import RestAPIException
from ..constants.status_code import StatusCode


class NoneObjectDoesntExistAPIException(RestAPIException):
    def __init__(self):
        self.msg = f"object with None object id does not exist"
        super().__init__(StatusCode.HTTP_400_BAD_REQUEST, 'object_id_is_none', self.msg)
