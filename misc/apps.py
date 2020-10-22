from django.apps import AppConfig


class MiscConfig(AppConfig):
    name = 'misc'

    def ready(self):
        from entropy import lookups_and_transforms


