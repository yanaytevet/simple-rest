
class BaseChoices(object):
    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(value, value) for value in cls.get_list()]

    @classmethod
    def get_list(cls) -> list[str]:
        return [getattr(cls, name) for name in cls.__dict__ if not name.startswith('__')]
