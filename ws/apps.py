from django.apps import AppConfig


class WSConfig(AppConfig):
    name = "ws"

    def ready(self):
        import ws.signals  # noqa: F403, F401
