from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'
    verbose_name = 'Indigenous Knowledge Community'

    def ready(self):
        """
        Initialize app when Django starts.
        This method is called when the app is ready.
        """
        # Import signals to register them
        import community.signals  # noqa
