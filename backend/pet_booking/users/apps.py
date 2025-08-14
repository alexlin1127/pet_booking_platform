# users/apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pet_booking.users"

    def ready(self):
        import pet_booking.users.signals

