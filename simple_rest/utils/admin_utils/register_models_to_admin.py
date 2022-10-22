import inspect
from typing import Type, List

from django.contrib import admin
from django.db.models import ManyToOneRel, ManyToManyField, ManyToManyRel, Model


class ModelRegisterer:
    """
    models can have the following class fields:
    list_display
    list_filter
    search_fields
    raw_id_fields
    """

    def __init__(self, models, ignore_models: List[Type[Model]] = None):
        self.models = models
        self.ignore_models = ignore_models

    def register(self) -> None:
        ignore_models_set = set() if self.ignore_models is None else set(self.ignore_models)
        for name, klass in inspect.getmembers(self.models, inspect.isclass):
            if klass in ignore_models_set:
                continue
            if hasattr(klass, 'list_display'):
                list_display = getattr(klass, 'list_display')
            else:
                list_display = []
                for field in klass._meta.get_fields():
                    if isinstance(field, ManyToOneRel):
                        continue
                    if isinstance(field, ManyToManyRel):
                        continue
                    if isinstance(field, ManyToManyField):
                        continue
                    list_display.append(field.name)
            if hasattr(klass, "list_filter"):
                list_filter = getattr(klass, "list_filter")
            else:
                list_filter = list(list_display)
                if "id" in list_filter:
                    list_filter = [item for item in list_filter if item != "id"]

            if hasattr(klass, "raw_id_fields"):
                raw_id_fields = getattr(klass, "raw_id_fields")
            else:
                raw_id_fields = []

            search_fields = getattr(klass, "search_fields") if hasattr(klass, "search_fields") else []

            admin_cls = type("{}_admin".format(name), (admin.ModelAdmin,), {
                "list_display": list_display,
                "search_fields": search_fields,
                "list_filter": list_filter,
                "raw_id_fields": raw_id_fields,
            })
            admin.site.register(klass, admin_cls)
