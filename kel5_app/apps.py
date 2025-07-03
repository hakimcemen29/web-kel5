from django.apps import AppConfig


class Kel5AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kel5_app'

    def ready(self):
        import kel5_app.signals