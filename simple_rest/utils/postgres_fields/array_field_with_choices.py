from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField


def ArrayFieldWithChoices(choices: list[tuple[str, str]], **kwargs):
    return ArrayField(CharField(max_length=100, blank=True, choices=choices),
                      default=list,
                      blank=True,
                      **kwargs)
