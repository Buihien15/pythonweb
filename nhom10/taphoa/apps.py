from django.apps import AppConfig


class TaphoaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "taphoa"
    
    def ready(self):
        import taphoa.signals
