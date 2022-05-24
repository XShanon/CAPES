from django.apps import AppConfig


class FeederConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feeder"

    def ready(self):
        from articleFetcher import fetcher

        fetcher.start()
