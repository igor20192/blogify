from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        from . import signals

        post_save.connect(signals.create_user_profile)
