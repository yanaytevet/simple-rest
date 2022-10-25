from abc import ABC, abstractmethod

from asgiref.sync import sync_to_async

from ..exceptions.rest_api_exception import RestAPIException


class PermissionsChecker(ABC):
    @abstractmethod
    def raise_exception_if_not_valid(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    async def async_raise_exception_if_not_valid(self, *args, **kwargs) -> None:
        return await sync_to_async(self.raise_exception_if_not_valid)(*args, **kwargs)

    def is_valid(self, *args, **kwargs) -> bool:
        try:
            self.raise_exception_if_not_valid(*args, **kwargs)
        except RestAPIException:
            return False
        return True

