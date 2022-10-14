from abc import ABC, abstractmethod

from django.db.models import Model, QuerySet
from django.http import JsonResponse, HttpRequest

from ..api_request import APIRequest
from ..constants.methods import Methods
from ..constants.status_code import StatusCode
from ..views.api_view_component import APIViewComponent


class DeleteItemAPIView(APIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.DELETE

    def delete(self, request: HttpRequest, **kwargs) -> JsonResponse:
        return self.run_with_exception_handling(APIRequest(request), **kwargs)

    def run(self, request: APIRequest, **kwargs) -> JsonResponse:
        self.check_permitted_before_object(request, **kwargs)
        obj = self.get_object(request, **kwargs)
        self.check_permitted_after_object(request, obj, **kwargs)
        self.run_before_deletion(request, obj, **kwargs)
        self.delete_item(request, obj, **kwargs)
        self.run_after_deletion(request, obj, **kwargs)
        return JsonResponse({}, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    def check_permitted_before_object(cls, request: APIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_object(cls, request: APIRequest, **kwargs) -> Model:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def check_permitted_after_object(cls, request: APIRequest, obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def delete_item(cls, request: APIRequest, obj: Model, **kwargs) -> None:
        obj.delete()

    @classmethod
    def run_before_deletion(cls, request: APIRequest, obj: Model, **kwargs) -> QuerySet:
        pass

    @classmethod
    def run_after_deletion(cls, request: APIRequest, obj: Model, **kwargs) -> QuerySet:
        pass
