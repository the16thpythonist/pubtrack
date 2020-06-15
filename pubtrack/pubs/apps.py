from django.apps import AppConfig


class PubsConfig(AppConfig):

    name = 'pubtrack.pubs'

    def ready(self):
        import pubtrack.pubs.signals

