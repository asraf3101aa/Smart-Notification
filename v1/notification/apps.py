from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'v1.notification'

    def ready(self):
        import v1.notification.signals
