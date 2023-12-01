from django.apps import AppConfig


class StripeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripeapp"

    def ready(self):
        import stripeapp.signals.consumer
